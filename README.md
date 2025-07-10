# PythoRAG
![Cover](assets/cover.png)

PythoRAG is a simple, open-source project designed to facilitate Retrieval-Augmented Generation (RAG) by integrating PDF document ingestion with Qdrant for vector storage and Deepseek-R1:1.5B (running on Ollama) for context-aware text generation.

## Features
- PDF Ingestion: Ingest PDF documents to extract text content and store it to Qdrant.
- Ollama Integration: Utilize DeepSeekR1:1.5B as Ollama model to generate response enriched with context from your PDFs.

## How to Run
### Requirements
1. Python 3.12.9

### Installation
1. Clone this repository
```bash
git@github.com:natanhp/PythoRAG.git
```
2. Create `.env` file in the root directory with the following values:
```.env
COLLECTION_NAME=<Qdrant collection name>
DOCUMENTS_PATH=<PDFs path, better use absolute path>
QDRANT_URL=<QDrant URL>
```
3. Setup virtualenv (Optional). We recommend using pyenv to manage Python versions. You can find detailed instructions here: [pyenv's documentation](https://github.com/pyenv/pyenv?tab=readme-ov-file#usage)
4. Install dependencies. Ensure you are in the cloned repository's root directory where `requirements.txt` is located.
```bash
pip install -r requirements.txt
```
5. Setup Qdrant. For local installation, refer to their documentation: [Qdrant Documentation](https://qdrant.tech/documentation/quickstart/)
6. Download and install Ollama using [their documentation](https://ollama.com/download/)
7. Install deepseek-r1:1.5b on Ollama
```bash
ollama run deepseek-r1:1.5b
```
8. Place your PDFs inside the folder specified by `<PDF's path>` in you `.env` file..
9. Run PythoRAG. Ensure that everything are all set before running PythoRAG
```bash
fastapi run
```
10. Please wait for document ingestion during the initial run. This process will populate your Qdrant collection with you PDFs.
11. Once running, you can access the API documentation at `localhost:8000/docs`.

### Example
#### 1.POST /api/chats
##### Payload
```JSON
{
  "prompt": "Who is Gregory Palamas? And what is his contribution into Orthodoxy? What is the Jesus's prayer?"
}
```
##### Response
```JSON
{
  "reasoning": "Okay, let me try to figure this out. The user has given me a bunch of context pieces about Gregory Palamas and asks for specific details: who he is, his contributions to Orthodoxy, and the Jesus's prayer.\n\nFirst, I'll look through each context item. Each one seems to be related to different aspects or translations from a book. The common theme across all these contexts is that they're discussing the Orthodox tradition centered around Gregory Palamas. \n\nLooking at the first three entries: the second one talks about him as an intellectual bishop in the Orthodox Church, and the third also mentions his theological contributions. The fourth source is a translation of that work into another language, which probably reinforces the idea that he's important in Orthodoxy.\n\nThe fifth entry gives more information about his life, though it doesn't add much new beyond what's already in the first four. So, I can confidently say that all these pieces converge on him being a significant figure in Orthodox spirituality and theology, particularly as an intellectual bishop.\n\nNow, for his contributions: from the context, it seems he was a saint to Orthodoxy and discussed various theological aspects in the book. His teachings were influential in shaping the Orthodox tradition. \n\nRegarding Jesus's prayer, I know that is usually emphasized in Christian practices but not widely recognized in Eastern religions like Orthodox Christianity. The user didn't provide information on that, so maybe they're looking for something less conventional.\n\nPutting it all together, I'll summarize that Gregory Palamas was a pivotal figure in the Orthodox tradition, known for his intellectual and theological contributions, though his role in Jesus' prayer isn't as prominent.",
  "answer": "Gregory Palamas was a significant figure in the Orthodox Christian tradition, known for his intellectual and theological contributions. He is often recognized as one of the most important figures in the development of Orthodox spirituality and theology. His teachings were influential in shaping the Orthodox Church's understanding of the world and its relationship to Christ.\n\nRegarding Jesus’s prayer, it is not widely acknowledged or emphasized in traditional Orthodox Christianity."
}
```