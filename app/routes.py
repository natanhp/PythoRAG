from fastapi import APIRouter, Response, status

from app.llm import construct_prompt, request_answer
from app.models import ErrorResponse, Query, NormalResponse
from fastapi import Request

router = APIRouter()


@router.post(
    "/chats/",
    tags=["chats"],
    status_code=status.HTTP_200_OK,
)
async def ask(query: Query, response: Response, request: Request) -> NormalResponse | ErrorResponse:
    results = request.app.state.vector_store.similarity_search(query.prompt, k=5)
    constructed_prompt = construct_prompt(results, query.prompt)

    try:
        answer = await request_answer(constructed_prompt)
        reasoning, answer = answer.split("<think>")[1].split("</think>")

        return NormalResponse(
            reasoning=reasoning.strip(),
            answer=answer.strip(),
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponse(
            message=str(e),
        )
