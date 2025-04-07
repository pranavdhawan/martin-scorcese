import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


def query(index, pc, encoder):
    q = "Tell me something about Adam Driver as an actor."
    print(q)
    # pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    # embedding = pc.inference.embed(
    #     model="multilingual-e5-large",
    #     inputs=[q],
    #     parameters={"input_type": "query"},
    # )

    query_embedding = encoder.encode(q).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=1,
        include_metadata=True,
    )

    print("\nRelevant passages:")
    for match in results["matches"]:
        print(f"\nSource: {match['metadata']['source']}")
        print(f"Text: {match['metadata']['text']}")
        print(f"Score: {match['score']:.4f}")


def init_index():
    load_dotenv()
    encoder = SentenceTransformer("all-MiniLM-L6-v2")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "scorcese-knowledge"

    index = pc.Index(index_name)
    print("all ok")
    # print(index.describe_index_stats())

    query(index, pc, encoder)
    return encoder, index


if __name__ == "__main__":
    encoder, index = init_index()
