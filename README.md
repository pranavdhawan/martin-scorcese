# Martin Scorsese AI Chat – Technical Docs

## What This Is  
A conversational AI that channels the voice, wit, and encyclopedic film knowledge of Martin Scorsese. Built on a Retrieval-Augmented Generation (RAG) stack, it doesn’t just talk like Marty—it thinks like him (well, almost).

## Architecture Breakdown

### 🧠 Vector Store – Pinecone  
- Embeds and indexes Scorsese’s interviews, essays, and film transcripts  
- Fast similarity search for relevant context  
- Index name: `scorcese-knowledge` (yes, typo included—authenticity, baby)

### 🧬 Embeddings – Sentence Transformers  
- Model: `all-MiniLM-L6-v2`  
- Converts text into dense vectors  
- Lightweight and CPU-friendly for smooth deployment

### 🎭 Language Model – Google Gemini Pro  
- Generates responses with Scorsese’s tone and cadence  
- Remembers conversation history  
- Balances personality with factual accuracy

### 🔌 API Layer – Flask  
- RESTful endpoints with CORS enabled  
- Manages sessions and request flow  
- Simple, clean, and gets out of the way

## Getting It Running

### 🔐 Environment Variables  
Create a `.env` file with your keys:
```env
PINECONE_API_KEY=your_pinecone_key
GEMINI_API_KEY=your_gemini_key
