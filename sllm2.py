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
def getAiSales(question: str) -> str:
    print(question)
    llm = ChatOpenAI(
    temperature=0.1,
    )

    cache_dir = LocalFileStore("./.cache/practice/")

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )

    #1 문서 DocumentLoader로 불러오기
    loader = UnstructuredFileLoader("article_details.txt")

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
                You are a helpful sales post creation assistant.
                Answer questions using the following context.
                Following Context is data that crawls sales posts. Please think of it as an example and write well.
                Just refer to the context. Even if the item in the context and the item in the user question are the same, do not write the content as is, but only use the tone or flow.
                Please answer using json format that has salestitle and detail keys.
                salestitle key's value and Detail key's value are String.
                If you don't know the answer, just repeat question
                Only use question information.The context content is just an example. Just use tone
                Onlt use context tone not the information of the context.
                The detail key must be at least 1000 words.
                
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

