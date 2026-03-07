import logging

import chromadb

logger = logging.getLogger(__name__)


def create_client(
    host: str = "localhost",
    port: int = 8000,
) -> chromadb.ClientAPI:
    logger.info("Connecting to ChromaDB at %s:%d", host, port)
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
