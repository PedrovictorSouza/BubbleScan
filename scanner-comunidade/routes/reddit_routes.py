from fastapi import APIRouter
from pydantic import BaseModel
from services.reddit_scraper import coletar_comentarios_reddit
from services.analisador import analisar_comentarios

router = APIRouter(prefix="/api")

class RedditRequest(BaseModel):
    url: str

@router.post("/analise_reddit")
def analisar_reddit(request: RedditRequest):
    comentarios = coletar_comentarios_reddit(request.url)
    sentimento = analisar_comentarios(comentarios)["sentimento"]
    return {"sentimento": sentimento} 