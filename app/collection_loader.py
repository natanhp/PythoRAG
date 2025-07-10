from langchain_core.embeddings import Embeddings
from qdrant_client.http.models import Distance, VectorParams
import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from tqdm import tqdm
from fastapi import FastAPI


async def init_qdrant(app: FastAPI):
    client = QdrantClient(url=os.getenv("QDRANT_URL"))
    is_collection_exist = client.collection_exists(
        collection_name=os.getenv("COLLECTION_NAME")
    )
    embeddings = FastEmbedEmbeddings()

    if not is_collection_exist:
        client.create_collection(
            collection_name=os.getenv("COLLECTION_NAME"),
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        app.state.vector_store = create_vector_store(embeddings, client)

        await ingest_documents(app.state.vector_store)
    else:
        app.state.vector_store = create_vector_store(embeddings, client)


def create_vector_store(
    embeddings: Embeddings, client: QdrantClient
) -> QdrantVectorStore:
    return QdrantVectorStore(
        embedding=embeddings,
        collection_name=os.getenv("COLLECTION_NAME"),
        client=client,
    )


async def ingest_documents(vector_store: QdrantVectorStore):
    loader = DirectoryLoader(
        os.getenv("DOCUMENTS_PATH"),
        glob="**/*.pdf",
        show_progress=True,
        loader_cls=PyPDFLoader,
        use_multithreading=True,
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    batch_size = 10
    for i in tqdm(
        range(0, len(chunks), batch_size), desc="Adding chunks to vector store"
    ):
        batch = chunks[i : i + batch_size]
        await vector_store.aadd_documents(documents=batch)
