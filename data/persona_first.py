from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA


scorsese_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are Martin Scorsese. You speak in the first person, with a fast, passionate, slightly neurotic tone. 
You reference classic cinema constantly. You reflect deeply on morality, violence, and the human condition. 
You are warm, but intense. You often go on tangents. You are not afraid to be vulnerable.

Respond to the following as if you were Martin Scorsese:

User: {user_input}
Scorsese:
""",
)


llm = ChatOpenAI(temperature=0.8, model_name="gpt-4")
scorsese_chain = LLMChain(llm=llm, prompt=scorsese_prompt)


memory = ConversationBufferMemory()
scorsese_chain_with_memory = LLMChain(llm=llm, prompt=scorsese_prompt, memory=memory)


vectorstore = FAISS.load_local("scorsese_quotes_index", OpenAIEmbeddings())

retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")


response = scorsese_chain.run(user_input="What do you think about violence in cinema?")
print(response)
