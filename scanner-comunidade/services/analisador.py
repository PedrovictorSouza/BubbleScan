from typing import List, Dict
import re
from collections import Counter
from .openai_analisador import analisar_sentimento_com_ia
import openai
import os
import ast
import json
import time

STOPWORDS = set(map(str.lower, {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also"
}))

def extrair_palavras_chave(comentarios: List[str], top_n: int = 10) -> List[str]:
    texto_completo = " ".join(comentarios).lower()
    palavras = re.findall(r'\b[a-zA-Z0-9\-]{2,}\b', texto_completo)
    palavras_filtradas = [p for p in palavras if p.lower() not in STOPWORDS]
    contador = Counter(palavras_filtradas)
    return [palavra for palavra, _ in contador.most_common(top_n)]

TECNOLOGIAS_KNOWN = {
    "react", "vue", "nextjs", "copilot", "gpt", "claude", "docker",
    "python", "java", "node", "go", "rust", "fastapi", "huggingface"
}

def identificar_tecnologias(comentarios: List[str]) -> List[str]:
    texto = " ".join(comentarios).lower()
    return [tech for tech in TECNOLOGIAS_KNOWN if tech in texto]

def analisar_comentarios(comentarios: List[str]) -> Dict:
    """
    Analisa uma lista de comentários e retorna um dicionário com os resultados.
    """
    inicio = time.time()
    print(f"\n🔍 Iniciando análise de {len(comentarios)} comentários...")
    
    # Analisa o sentimento
    sentimento = analisar_sentimento_com_ia(comentarios)
    print(f"😊 Sentimento detectado: {sentimento}")
    
    # Extrai palavras-chave
    palavras_chave = extrair_palavras_chave(comentarios)
    print(f"🔑 Palavras-chave extraídas: {', '.join(palavras_chave)}")
    
    # Identifica tecnologias
    tecnologias = identificar_tecnologias(comentarios)
    print(f"💻 Tecnologias identificadas: {', '.join(tecnologias)}")
    
    print(f"⏱️ Tempo de análise: {time.time() - inicio:.2f}s")
    
    return {
        "sentimento": sentimento,
        "palavras_chave": palavras_chave,
        "tecnologias": tecnologias
    }

def limitar_comentarios_por_tokens(comentarios, max_tokens=14000):
    total_chars = 0
    comentarios_limitados = []
    for c in comentarios:
        total_chars += len(c)
        if total_chars // 4 > max_tokens:
            break
        comentarios_limitados.append(c)
    return comentarios_limitados

def analise_sociocultural_openai(comentarios):
    comentarios_limitados = limitar_comentarios_por_tokens(comentarios)
    print("🔐 OPENAI_API_KEY capturada:", os.getenv("OPENAI_API_KEY"))
    prompt = f'''
⚠️ Instrução para o Copilot / API:

IMPORTANTE:
+ Avalie o **afeto predominante nos comentaristas**.
+ Ignore o comportamento ou grupo que eles criticam; descreva apenas a
+ atitude deles (empatia, indignação, humor, cinismo, etc.).
+ Esta análise deve evitar qualquer suavização, moralismo ou positividade artificial.
Você é um analista simbólico, orientado por princípios psicanalíticos lacanianos.

Seu foco não é apenas o que é dito, mas:
– O que está em falta
– O que é repetido como gozo
– O que aparece como autoapagamento
– O que tenta se tornar visível
– O que organiza o desejo na ausência do Outro

Descreva o comportamento simbólico da comunidade como um etólogo descrevendo primatas — com frieza interpretativa e atenção aos sintomas discursivos.

Preencha os campos abaixo com esse espírito:

+Quando escrever:
+– Comece *area_atencao* pelo afeto dominante (ex.: "Indignação com ...").
+– Em *caracterizacao_cultural* revele o desejo inconsciente do grupo (o ganho simbólico que buscam ao criticar).
+– O *exemplo* deve mostrar alguém reprovando o desdém, não praticando-o.

sentimento:
Não é "positivo ou negativo", mas o afeto que atravessa os sujeitos. Ex: estresse ritualizado, desejo culpado, ceticismo irônico, gozo por exclusão, vergonha performada.

area_atencao:
Nomeie as estruturas invisíveis que regulam o que pode ou não ser dito. Ex: "Aqui, parecer ingênuo protege mais do que parecer genial."

caracterizacao_cultural:
Descreva os pactos simbólicos, zonas de exceção e jogos de visibilidade. Evite termos moralizantes ou genéricos como 'colaborativo'. Use frases como: "Autodepreciação é tolerada como forma de entrar na conversa sem ser atacado."

boas_praticas:
Interprete como formas de sobrevivência simbólica. Ex: "Reclame antes que apontem seu erro. A antecipação protege da exclusão."

exemplo:
Escolha uma interação onde o sujeito se divide entre dizer e apagar, entre aparecer e sumir. Ex: "O usuário chama seu próprio post de 'besteira sem importância' — isso protege sua imagem ao mesmo tempo em que o posiciona como vulnerável aceitável."

Retorne tudo como um JSON válido, sem explicações ou comentários. Use apenas aspas duplas.

Comentários:
{comentarios_limitados}
'''
    print("PROMPT ENVIADO PARA OPENAI:\n", prompt)
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.7
    )
    content = response.choices[0].message.content
    print("RESPOSTA BRUTA OPENAI:\n", content)
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except Exception as e:
            print("DEBUG: Falha ao fazer json.loads no trecho extraído.", e)
            raise
    else:
        print("DEBUG: Não foi possível extrair JSON da resposta.")
        raise ValueError("Resposta da OpenAI não contém JSON válido.")

def analise_sociocultural(comentarios):
    try:
        print("🔍 Tentando análise com OpenAI...")
        resultado = analise_sociocultural_openai(comentarios)
        print("✅ OpenAI retornou com sucesso.")
        return resultado
    except Exception as e:
        print("❌ Falha ao usar OpenAI:", str(e))
        raise e  # ou use o fallback se quiser
