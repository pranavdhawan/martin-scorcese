import os
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
import json
from dotenv import load_dotenv

load_dotenv()


class StoreToDB:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        self.index_name = "scorcese-knowledge"

        if self.index_name not in pc.list_indexes():
            pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        self.index = pc.Index(self.index_name)
        print("all ok")

    def chunk_text(self, text: str, chunk_size: int = 512) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1  # +1 for space
            if current_length > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def process_file(self, filepath: str) -> List[dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = self.chunk_text(content)
        filename = os.path.basename(filepath)

        return [
            {"text": chunk, "metadata": {"source": filename, "chunk_index": i}}
            for i, chunk in enumerate(chunks)
        ]

    def index_documents(self, data_dir: str):
        all_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
        for file in all_files:
            filepath = os.path.join(data_dir, file)
            chunks = self.process_file(filepath)

            for i, chunk in enumerate(chunks):
                vector = self.encoder.encode(chunk["text"]).tolist()
                vector_id = f"{file}_{i}"
                self.index.upsert(
                    vectors=[
                        (
                            vector_id,
                            vector,
                            {
                                "text": chunk["text"],
                                "source": chunk["metadata"]["source"],
                                "chunk_index": chunk["metadata"]["chunk_index"],
                            },
                        )
                    ]
                )
                print(f"Indexed chunk {i} from{file}")


if __name__ == "__main__":
    indexer = StoreToDB()
    indexer.index_documents("data/raw")
