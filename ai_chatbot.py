from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

import os
os.environ['OPENAI_API_KEY'] = ''
def getChatbotAnswer(question: str) -> str:
    print(question)
    llm = ChatOpenAI(
    temperature=0.1,
    )

    cache_dir = LocalFileStore("./.cache/practice/")

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=5000,
        chunk_overlap=100,
    )

    #1 문서 DocumentLoader로 불러오기
    loader = UnstructuredFileLoader("운영정책.txt")

    #2 텍스트 스플릿
    docs = loader.load_and_split(text_splitter=splitter)

    #3 임베딩
    embeddings = OpenAIEmbeddings()

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

    #4 벡터스토어 저장
    vectorstore = FAISS.from_documents(docs, cached_embeddings)

    #5 검색
    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a helpful assistant. 
                Answer questions using only the following context. 
                Please answer using json format that has "answer" key.
                "answer" key's data type is string
                If you don't know the answer just say you don't know, don't make it up:
                {context}
                """,
            ),
            ("human", "{question}"),
        ]
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    result = chain.invoke(question)
    print(result.content)
    return result.content

