from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scraper import get_hn_comments
from services.reddit_scraper import coletar_comentarios_reddit
from services.analisador import analisar_comentarios, analise_sociocultural
import traceback

router = APIRouter()

class AnaliseRequest(BaseModel):
    url: str

@router.post("/analise_auto")
async def analisar_auto(request: AnaliseRequest):
    url = request.url
    print(f"\n🔍 Analisando URL: {url}")

    if "reddit.com" in url:
        print("📱 Detectado: Reddit")
        comentarios = coletar_comentarios_reddit(url)
        if not comentarios:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado")
            
        print(f"✅ {len(comentarios)} comentários coletados")
        resultado = analisar_comentarios(comentarios)
        print("✅ Análise básica concluída")
        
        sociocultural = analise_sociocultural(comentarios)
        print("✅ Análise sociocultural concluída")
        
        resultado.update(sociocultural)
        resultado["fonte"] = "reddit"
        resultado["titulo"] = "Análise de Comentários do Reddit"
        return resultado
        
    elif "news.ycombinator.com/item?id=" in url:
        print("📱 Detectado: Hacker News")
        resultado_scraper = get_hn_comments(url)
        comentarios = resultado_scraper["comentarios"]
        titulo = resultado_scraper["titulo"]
        if not comentarios:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado")
        
        print(f"✅ {len(comentarios)} comentários coletados")
        resultado = analisar_comentarios(comentarios)
        print("✅ Análise básica concluída")
        
        sociocultural = analise_sociocultural(comentarios)
        print("✅ Análise sociocultural concluída")
        
        resultado.update(sociocultural)
        resultado["titulo"] = titulo
        resultado["fonte"] = "hackernews"
        return resultado
    else:
        raise HTTPException(status_code=400, detail="Fonte de URL não suportada") 