import re
from collections import Counter
from typing import List, Set
import spacy

from services.utils.texto import extrair_palavras_validas
from services.utils.stopwords import STOPWORDS

# Carregar modelo spaCy para análise gramatical
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except OSError:
    print("⚠️ spaCy model não encontrado. Instalando...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True

REJEITAR_TECNICISMOS_REDDIT = {
    "post", "posts", "thread", "comment", "comments", "upvote", "downvote",
    "reddit", "sub", "subreddit", "op", "nsfw", "flair"
}

REJEITAR_JARGÕES_GENÉRICOS = {
    "game", "games", "dev", "devs", "play", "player", "players", "release",
    "update", "patch", "fps", "bug", "glitch", "system", "beat", "levels", "hard", "long",
}

REJEITAR_PALAVRAS_CURTAS = {"t", "s", "is", "are", "was", "i'm", "they", "we", "it"}

MIN_LETRAS = 4

# Classes gramaticais que queremos manter (substantivos, verbos, etc.)
POS_DESEJADOS = {"NOUN", "VERB", "PROPN"}  # Substantivos, Verbos, Nomes Próprios


def filtrar_por_pos(palavras: List[str]) -> List[str]:
    """
    Filtra palavras baseado na classe gramatical usando spaCy.
    Remove adjetivos e mantém apenas substantivos, verbos e nomes próprios.
    """
    if not SPACY_AVAILABLE or not palavras:
        return palavras
    
    try:
        # Junta as palavras em um texto para análise
        texto = " ".join(palavras)
        doc = nlp(texto)
        
        # Filtra apenas palavras com classes gramaticais desejadas
        palavras_filtradas = [
            token.text.lower() for token in doc 
            if token.pos_ in POS_DESEJADOS and not token.is_stop
        ]
        
        return palavras_filtradas
    except Exception as e:
        print(f"⚠️ Erro ao filtrar por POS: {e}")
        return palavras


def extrair_palavras_chave_filtradas(
    comentarios: List[str], top_n: int = 10, stopwords: Set[str] = STOPWORDS
) -> List[str]:
    texto_completo = " ".join(comentarios).lower()
    palavras = extrair_palavras_validas(texto_completo)

    # Primeiro filtro: stopwords, tamanho mínimo e palavras específicas
    palavras_filtradas = [
        p for p in palavras
        if p not in stopwords
        and len(p) >= MIN_LETRAS
        and p not in REJEITAR_TECNICISMOS_REDDIT
        and p not in REJEITAR_JARGÕES_GENÉRICOS
        and p not in REJEITAR_PALAVRAS_CURTAS
    ]

    # Segundo filtro: análise gramatical com spaCy
    palavras_filtradas = filtrar_por_pos(palavras_filtradas)

    contador = Counter(palavras_filtradas)
    return [palavra for palavra, _ in contador.most_common(top_n)]
