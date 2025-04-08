# Martin Scorsese AI 

Chatbot that channels the voice, wit, and encyclopedic film knowledge of Martin Scorsese. Built on a RAG stack, it thinks like him (well, almost).

## Stack

### Vector Store – Pinecone  
Scorsese’s interviews, essays, and scripts—embedded, indexed, and ready to rip. Fast similarity search.
Index name: ‎`scorcese-knowledge`


### Embeddings – Sentence Transformers  
Model: ‎`all-MiniLM-L6-v2`.
Turns text into dense little brain blobs. Light, fast, doesn’t need a GPU.


### Language Model – Google Gemini Pro  
Talks like Marty. Thinks like Marty. Doesn’t hallucinate (much).
(Doesn't keep the thread going without losing the plot tho, lol)


### API Layer – Flask  
REST endpoints, CORS on, no drama.
Just enough glue to keep the whole thing humming.


### 🔐 Environment Variables  

```env
PINECONE_API_KEY=your_pinecone_key
GEMINI_API_KEY=your_gemini_key
