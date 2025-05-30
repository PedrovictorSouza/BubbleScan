from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from routes import analise_routes
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

# Registrar rotas
app.include_router(analise_routes.router, prefix="/api")

# Serve apenas os assets estáticos em /assets
app.mount(
    "/assets",
    StaticFiles(directory="frontend-react/dist/assets"),
    name="assets"
)

# favicon do Vite
@app.api_route("/vite.svg", methods=["GET", "HEAD"], include_in_schema=False)
async def favicon():
    return FileResponse("frontend-react/dist/vite.svg")

@app.get("/api")
async def root_api():
    return {"message": "BubbleScan API no ar!"}

@app.get("/api/healthz")
async def health():
    return {"status": "ok"}

# Serve index.html em GET /
@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
async def serve_index():
    return FileResponse("frontend-react/dist/index.html")

# Fallback para SPA em qualquer outra GET não-/api e não-/assets
@app.api_route("/{full_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
async def serve_spa(full_path: str, request: Request):
    # não intercepta API, nem assets, nem favicon
    if (
        request.url.path.startswith("/api")
        or request.url.path.startswith("/assets")
        or request.url.path == "/vite.svg"
    ):
        raise HTTPException(status_code=404, detail="Not Found")

    return FileResponse("frontend-react/dist/index.html") 