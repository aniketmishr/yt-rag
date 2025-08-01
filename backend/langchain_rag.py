from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from chromadb import Client
from chromadb.config import Settings

load_dotenv()

class YTRagBackend: 
    def __init__(self): 
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
        self.vector_store = None
        self.retriever = None
        self.persist_directory_name = "./chroma_data"

        self.prompt = PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is insufficient, just say you don't know.

            {context}
            Question : {question}
            """,
            input_variables = ['context',"question"] 
        )

        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.0-flash", 
            temperature = 0.5, 
            max_tokens = None, 
            timeout = None, 
            max_retries = 2, 
        ) 

    def index_transcript(self, video_id: str): 
        if not(self.chroma_collection_exists(collection_name=video_id, persist_directory=self.persist_directory_name)): 
            try:
                # if you don't care which language, this resturns the best one
                transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en'])
                # Flatten it to plain text
                transcript = " ".join(chunk.text for chunk in transcript_list)
            except TranscriptsDisabled:
                print("No captions available for this video")
            # Initializing the vector store
            self.vector_store = Chroma(
                collection_name=video_id,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory_name
            )
            chunks = self.splitter.create_documents([transcript])
            self.vector_store.add_documents(chunks)
            print("Indexing completed")
        else : 
            self.vector_store = Chroma(
                collection_name=video_id,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory_name
            )
        return {"message": "Indexing completed successfully."}
   
    def query(self, question: str) -> str: 
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs = {"k":4})
        relevant_docs = self.retriever.invoke(question)
        context = self.format_docs(relevant_docs)
        final_prompt = self.prompt.invoke({"context": context, "question" : question})
        response = self.llm.invoke(final_prompt)
        return response.content
    
    def format_docs(self,retrieved_docs):
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text
    
    @staticmethod
    def chroma_collection_exists(
        collection_name: str,
        persist_directory: str
    ) -> bool:
        client = Client(Settings(is_persistent=True,persist_directory= persist_directory ))
        collections = client.list_collections()
        return any(c.name == collection_name for c in collections)


if __name__ == "__main__": 

    obj = YTRagBackend()
    # obj.index_transcript('Z_c4byLrNBU')
    # print(obj.query('what is DFS?'))