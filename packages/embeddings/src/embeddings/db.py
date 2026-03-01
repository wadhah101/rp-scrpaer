import logging
from enum import Enum

import chromadb

logger = logging.getLogger(__name__)


class ClientMode(Enum):
    MEMORY = "memory"
    PERSISTENT = "persistent"
    HTTP = "http"


def create_client(
    mode: ClientMode = ClientMode.MEMORY,
    path: str = "./chroma_data",
    host: str = "localhost",
    port: int = 8000,
) -> chromadb.ClientAPI:
    match mode:
        case ClientMode.MEMORY:
            logger.info("Initializing in-memory ChromaDB client")
            return chromadb.Client()
        case ClientMode.PERSISTENT:
            logger.info(
                "Initializing persistent ChromaDB client at %s",
                path,
            )
            return chromadb.PersistentClient(path=path)
        case ClientMode.HTTP:
            logger.info(
                "Initializing HTTP ChromaDB client at %s:%d",
                host,
                port,
            )
            return chromadb.HttpClient(host=host, port=port)


def create_collection(
    client: chromadb.ClientAPI,
    name: str,
    space: str = "cosine",
) -> chromadb.Collection:
    logger.debug("Creating collection: %s (space=%s)", name, space)
    collection = client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": space},
    )
    logger.debug("%s collection ready, count: %d", name, collection.count())
    return collection
