import logging

import chromadb

logger = logging.getLogger(__name__)

logger.info("Initializing in-memory ChromaDB client")
client = chromadb.Client()

logger.debug("Creating collection: hevy_exercises (space=cosine)")
hevy_collection = client.get_or_create_collection(
    name="hevy_exercises",
    metadata={"hnsw:space": "cosine"},
)
logger.debug(
    "hevy_exercises collection ready, count: %d",
    hevy_collection.count(),
)

logger.debug("Creating collection: rp_exercises (space=cosine)")
rp_collection = client.get_or_create_collection(
    name="rp_exercises",
    metadata={"hnsw:space": "cosine"},
)
logger.debug(
    "rp_exercises collection ready, count: %d",
    rp_collection.count(),
)
