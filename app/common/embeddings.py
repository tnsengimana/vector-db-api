import numpy as np
import cohere
from typing import List

DIMENSION_SIZE = 1024

cohere_client = cohere.ClientV2(api_key="A1Fi5KBBNoekwBPIa833CBScs6Z2mHEtOXxr52KO")


def create_embedding_vector(text: str) -> np.ndarray:
    return bulk_create_embedding_vector([text])[0]


def bulk_create_embedding_vector(texts: List[str]) -> List[np.ndarray]:
    res = cohere_client.embed(
        texts=texts,
        model="embed-v4.0",
        input_type="search_query",
        output_dimension=DIMENSION_SIZE,
        embedding_types=["float"],
    )

    return [np.array(vector) for vector in res.embeddings.float]

