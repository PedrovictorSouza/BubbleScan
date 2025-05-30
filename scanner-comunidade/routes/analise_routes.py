from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scraper import get_hn_comments
from services.reddit_scraper import coletar_comentarios_reddit
from services.analisador import analisar_comentarios, analise_sociocultural

router = APIRouter()

class AnaliseRequest(BaseModel):
    url: str

@router.post("/analise_auto")
async def analisar_auto(request: AnaliseRequest):
    url = request.url

    try:
        if "reddit.com" in url:
            comentarios = coletar_comentarios_reddit(url)
            if not comentarios:
                raise HTTPException(status_code=404, detail="Nenhum comentário encontrado")
                
            resultado = analisar_comentarios(comentarios)
            sociocultural = analise_sociocultural(comentarios)
            resultado.update(sociocultural)
            resultado["fonte"] = "reddit"
            resultado["titulo"] = "Análise de Comentários do Reddit"
            return resultado
            
        elif "news.ycombinator.com/item?id=" in url:
            resultado_scraper = get_hn_comments(url)
            comentarios = resultado_scraper["comentarios"]
            titulo = resultado_scraper["titulo"]
            if not comentarios:
                raise HTTPException(status_code=404, detail="Nenhum comentário encontrado")
            
            resultado = analisar_comentarios(comentarios)
            sociocultural = analise_sociocultural(comentarios)
            resultado.update(sociocultural)
            resultado["titulo"] = titulo
            resultado["fonte"] = "hackernews"
            return resultado
        else:
            raise HTTPException(status_code=400, detail="Fonte de URL não suportada")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 