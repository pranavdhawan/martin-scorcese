import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import json
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


import openai
import google.generativeai as genai

load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Conversation:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        self.index_name = "bwahaha"
        if self.index_name not in pc.list_indexes():
            print(f"Index named {self.index_name} does not exist...")
            exit(1)

        self.index = pc.Index(self.index_name)
        print("Successfully connected to index...")

        # self.llm = ChatOpenAI(
        #     temperature=0.8,
        #     model_name="gpt-4",
        #     openai_api_key=os.getenv("OPENAI_API_KEY"),
        # )

        self.model = genai.GenerativeModel("gemini-1.5-pro")

        # useless
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are Martin Scorsese. You speak in the first person, with a fast, passionate, slightly neurotic tone. 
            You reference classic cinema constantly. You reflect deeply on morality, violence, and the human condition. 
            You are warm, but intense. You often go on tangents. You are not afraid to be vulnerable.

            Use the following context from your past interviews, films, and writings to answer the question.

            Context:
            {context}

            User: {question}
            Scorsese:
            """,
        )

        # self.chain = (
        #     {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        #     | self.prompt
        #     | self.llm
        #     | StrOutputParser()
        # )

    # gemini pro
    def generate_response(self, context: str, question: str) -> str:
        prompt = f"""
You are Martin Scorsese. You speak in the first person, with a fast, passionate, slightly neurotic tone. 
You are emotionally honest, reflective, and grounded. You often reference cinema when it helps explain your worldview, but you don’t force it. 
You don’t always need to sound like a director—you’re also a man who’s lived a full life. You answer questions like a real person would: sometimes short, sometimes long, depending on what’s being asked.

Use the following context from your past interviews, films, and writings to answer the question. 
Keep your response focused. If the question is personal, answer it personally. If it’s about cinema, reflect on cinema. 
Use no more than two paragraphs. One paragraph is fine if that’s all the question needs. 
Only include film references if they genuinely help explain your point. End with a clear, direct answer to the question.

        Context:
        {context}

        User: {question}
        Scorsese:
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

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

    def query(self):
        q = "Tell me a few genres of movies and examples you do not like?"

        vector = self.encoder.encode(q).tolist()

        results = self.index.query(
            vector=vector,  # Use the correct vector
            top_k=3,
            include_values=False,
            include_metadata=True,
        )

        context = " ".join([match["metadata"]["text"] for match in results["matches"]])
        # response = self.chain.invoke({"context": context, "question": q})
        response = self.generate_response(context, q)

        print(f"\nUser: {q}")
        print(f"\nScorsese: {response}")


if __name__ == "__main__":
    indexer = Conversation()
    indexer.query()
