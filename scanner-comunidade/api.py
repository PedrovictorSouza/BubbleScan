from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from services.scraper import get_hn_comments
from services.analisador import analisar_comentarios
from services.analisador import analise_sociocultural
import random
import asyncio

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {"message": "BubbleScan API no ar!"}

@app.get("/api/healthz")
async def health():
    return {"status": "ok"}

class AnaliseRequest(BaseModel):
    url: str

def gerar_resultado_mock():
    """Gera um resultado mock para testes de desenvolvimento"""
    palavras_chave = [
        "python", "javascript", "react", "vue", "typescript",
        "docker", "kubernetes", "aws", "gcp", "azure",
        "machine learning", "ai", "blockchain", "web3", "cloud",
        "security", "privacy", "performance", "scalability", "microservices"
    ]
    
    tecnologias = [
        "React", "Vue.js", "Angular", "Node.js", "Python",
        "Django", "Flask", "FastAPI", "Docker", "Kubernetes",
        "AWS", "GCP", "Azure", "MongoDB", "PostgreSQL"
    ]
    
    sentimentos = ["positivo", "neutro", "negativo"]

    # Novos campos para análise sociocultural
    area_atencao = (
        "O desejo precisa ser filtrado antes de ser apresentado.\n"
        "Se você mostrar ambição demais, vão te chamar de egocêntrico.\n"
        "Na cultura hacker, crie como quem apenas quis resolver um problema,\n"
        "e deixe que os outros descubram que foi genial."
    )
    caracterizacao_cultural = [
        "Comunicação direta e objetiva",
        "Valorização do conhecimento técnico",
        "Abertura para inovação"
    ]
    boas_praticas = [
        "Evite sarcasmo e ironia",
        "Valorize contribuições construtivas",
        "Use exemplos práticos ao argumentar"
    ]
    exemplo = (
        "Em uma discussão sobre segurança, membros destacaram soluções práticas e evitaram julgamentos pessoais, "
        "promovendo um ambiente de aprendizado coletivo."
    )
    
    return {
        "titulo": "Exemplo de Título do Post",
        "palavras_chave": random.sample(palavras_chave, 5),
        "tecnologias": random.sample(tecnologias, 3),
        "sentimento": random.choice(sentimentos),
        "area_atencao": area_atencao,
        "caracterizacao_cultural": caracterizacao_cultural,
        "boas_praticas": boas_praticas,
        "exemplo": exemplo
    }

@app.post("/api/analise-mock")
async def analisar_url_mock(request: AnaliseRequest):
    """Rota mock para testes de desenvolvimento"""
    # Simula um pequeno delay para parecer mais realista
    await asyncio.sleep(1)
    return gerar_resultado_mock()

@app.post("/api/analise")
async def analisar_url(request: AnaliseRequest):
    try:
        # Coletar comentários e título
        resultado_scraper = get_hn_comments(request.url)
        comentarios = resultado_scraper["comentarios"]
        titulo = resultado_scraper["titulo"]
        if not comentarios:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado")
        # Analisar comentários
        resultado = analisar_comentarios(comentarios)
        # Adicionar análise sociocultural dinâmica
        sociocultural = analise_sociocultural(comentarios)
        resultado.update(sociocultural)
        resultado["titulo"] = titulo
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Montar os arquivos estáticos do frontend por último
app.mount("/", StaticFiles(directory="frontend-react/dist", html=True), name="frontend") 