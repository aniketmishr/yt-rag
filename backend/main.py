from fastapi import FastAPI, HTTPException
from langchain_rag import YTRagBackend
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 

class QueryRequest(BaseModel):
    question: str

app = FastAPI()
# Enable CORS to allow requests from the extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now, allow all. You can limit to specific origins later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
backend = YTRagBackend()

@app.post("/index/{video_id}")
def index_video(video_id: str):
    try:
        result = backend.index_transcript(video_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def ask_question(req: QueryRequest):
    try:
        answer = backend.query(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

