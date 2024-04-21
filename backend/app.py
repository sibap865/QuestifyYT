from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma  # chroma for storing vector store locally
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings # for converting text to embedings
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')
load_dotenv()

# create & add a .env file with the google api key
api =os.getenv("GOOGLE_API_KEY") #uncomment this during locally
os.environ["LANGCHAIN_TRACING_V2"] ="true"
os.environ["LANGCHAIN_API_KEY"] =os.getenv('LANGCHAIN_API_KEY')
genai.configure(api_key=api)  
app = FastAPI()
url_val =True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# load your vector  embeddings
model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

print(f"embending Model loaded")
class URLCheckRequest(BaseModel):
    url: str
    textInput: str
class CheckURL(BaseModel):
    url: str
class CheckSearchInput(BaseModel):
    textInput: str

def get_transcript(url:str):
     """
     Try to get the transcription of the yt video
     input: url
     output: yt_transcription
     """
     try:
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=False,
        language=["en", "hi"],
        translation="en",
        )
        doc = loader.load()
        return doc
     except:
        return "not able to get transcript"
@app.post("/val_url")
async def val_url(request:CheckURL):
    """
    validate if transcription is available.If available convert the transcript to embendings
    and store it in croma vector store
    input: url
    output: response
    """
    print("url validating")
    doc = get_transcript(request.url)
    if doc!="not able to get transcript":
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
        texts = text_splitter.split_documents(documents=doc)
        # vector_store = Chroma.from_documents(texts, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="stores/yt_cosine")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
        texts = text_splitter.split_documents(documents=doc)
        global vector_index
        vector_index = FAISS.from_documents(documents=texts,embedding=embeddings)

        content ="video is ready to search"
    else:
        content ="not able to get transcript"
    print(content)
    return {"results": content}

@app.post("/yt_search")
async def yt_search(request:CheckSearchInput):
    """
    get the generation output using vecotr and llm
    input: text
    output: response
    """
    prompt_template = """Use the following  text transcript to answer the user's question in detail.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the  answer below and nothing else.
    Detailed answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    # load_vector_store = Chroma(persist_directory="stores/yt_cosine", embedding_function=embeddings)
    # retriever = vector_index
    
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                            temperature=0.2,convert_system_message_to_human=True)
    
    chain_type_kwargs = {"prompt": prompt}
    qa = RetrievalQA.from_chain_type(
    llm=model,
    chain_type="stuff",
        retriever=vector_index.as_retriever(search_kwargs={"k":2}),
        return_source_documents = True,
        chain_type_kwargs= chain_type_kwargs,
        verbose=True
    )

    response = qa(request.textInput)

    print(response["query"])
    return {"result":response["result"]}