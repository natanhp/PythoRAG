import aiohttp
from typing import List, Any


def construct_prompt(search_results: List[Any], prompt: str) -> str:
    context = (
        "No contex found."
        if len(search_results) == 0
        else [
            {"content": x.page_content, "source": x.metadata.get("source", "Uknown")}
            for x in search_results
        ]
    )
    return f"""
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {prompt}

Provide an accurate response with the help of the provided context above.
"""


async def request_answer(constructed_prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11434/api/generate",
            json={
                "prompt": constructed_prompt,
                "model": "deepseek-r1:1.5b",
                "stream": False,
            },
        ) as response:
            if response.status != 200:
                raise Exception(
                    f"Failed to get response from LLM. Status code: {response.status}"
                )

            return (await response.json())["response"]
