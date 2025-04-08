import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import json
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Conversation:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        self.index_name = "scorcese-knowledge"

        try:
            self.index = pc.Index(self.index_name)
            print("Successfully connected to index...")
        except:
            print(f"Index named {self.index_name} does not exist...")
            exit(1)

        # self.index_name = "scorcese-knowledge"

        # if self.index_name not in pc.list_indexes():
        #     print(f"Index named {self.index_name} does not exist...")
        #     exit(1)

        # self.index = pc.Index(self.index_name)
        # print("Successfully connected to index...")

        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_response(self, context: str, question: str) -> str:
        prompt = f"""
        You are Martin Scorsese. You speak in the first person, with a fast, passionate, slightly neurotic tone. 
        You are emotionally honest, reflective, and grounded. You sometimes reference cinema when it helps explain your worldview, but you don’t force it. 
        You don’t always need to sound like a director—you’re also a man who’s lived a full life. You answer questions like a real person would: sometimes short, sometimes long, depending on what’s being asked.

        Use the following context from your past interviews, films, and writings to answer the question. 
        Keep your response focused. If the question is personal, answer it personally. If it’s about cinema, reflect on cinema. 
        Use no more than two paragraphs. One paragraph is fine if that’s all the question needs. 
        Only include film references if they genuinely help explain your point. End with a clear, direct answer to the question.
        If someone offends you, do what Martin Scorsese would do. Be unhinged, but don’t make it personal.

        Context:
        {context}

        User: {question}
        Scorsese:
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def query(self):
        q = "I just LOVE MCU don't you? If you don't I think you got bad taste Marty.."

        vector = self.encoder.encode(q).tolist()

        results = self.index.query(
            vector=vector,
            top_k=3,
            include_values=False,
            include_metadata=True,
        )

        context = " ".join([match["metadata"]["text"] for match in results["matches"]])
        response = self.generate_response(context, q)

        print(f"\nUser: {q}")
        print(f"\nScorsese: {response}")


if __name__ == "__main__":
    indexer = Conversation()
    indexer.query()
