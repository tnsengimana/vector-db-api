import cohere
from typing import List

co = cohere.ClientV2(api_key="A1Fi5KBBNoekwBPIa833CBScs6Z2mHEtOXxr52KO")


def create_embedding_vector(text: str) -> List[float]:
    return bulk_create_embedding_vector([text])[0]


def bulk_create_embedding_vector(texts: List[str]) -> List[List[float]]:
    res = co.embed(
        texts=texts,
        model="embed-v4.0",
        input_type="search_query",
        output_dimension=1024,
        embedding_types=["float"],
    )

    return res.embeddings.float
