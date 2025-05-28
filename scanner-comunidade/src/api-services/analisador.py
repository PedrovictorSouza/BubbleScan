from collections import Counter
import re
from typing import List, Dict

# Lista de tecnologias conhecidas
TECNOLOGIAS = {
    "python", "javascript", "java", "typescript", "react", "vue", "angular",
    "node", "docker", "kubernetes", "aws", "azure", "gcp", "spring",
    "django", "flask", "fastapi", "postgresql", "mongodb", "redis",
    "tensorflow", "pytorch", "machine learning", "ai", "blockchain"
}

# Palavras comuns para ignorar
STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also"
}

def extrair_palavras_chave(comentarios: List[str], top_n: int = 10) -> List[str]:
    """
    Extrai as palavras-chave mais frequentes dos comentários.
    """
    # Junta todos os comentários em um único texto
    texto_completo = " ".join(comentarios).lower()
    
    # Remove caracteres especiais e números
    palavras = re.findall(r'\b[a-z]{3,}\b', texto_completo)
    
    # Remove stopwords e conta frequência
    palavras_filtradas = [p for p in palavras if p not in STOPWORDS]
    contador = Counter(palavras_filtradas)
    
    # Retorna as top_n palavras mais frequentes
    return [palavra for palavra, _ in contador.most_common(top_n)]

def identificar_tecnologias(comentarios: List[str]) -> List[str]:
    """
    Identifica tecnologias mencionadas nos comentários.
    """
    # Junta todos os comentários em um único texto
    texto_completo = " ".join(comentarios).lower()
    
    # Encontra tecnologias mencionadas
    tecnologias_encontradas = set()
    for tech in TECNOLOGIAS:
        if tech.lower() in texto_completo:
            tecnologias_encontradas.add(tech)
    
    return list(tecnologias_encontradas)

def analisar_sentimento(comentarios: List[str]) -> str:
    """
    Analisa o sentimento predominante nos comentários.
    Simplificado para MVP: retorna sentimento fixo.
    """
    # TODO: Implementar análise de sentimento real
    return "estresse coletivo"

def analisar_comentarios(comentarios: List[str]) -> Dict:
    """
    Função principal que coordena a análise dos comentários.
    """
    return {
        "palavras_chave": extrair_palavras_chave(comentarios),
        "tecnologias": identificar_tecnologias(comentarios),
        "sentimento": analisar_sentimento(comentarios)
    } 