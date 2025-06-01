# services/openai_analisador.py
import os
from dotenv import load_dotenv
import openai
from typing import List

# Carrega as variáveis de ambiente do .env
load_dotenv()

def analisar_sentimento_com_ia(comentarios: List[str]) -> str:
    """
    Usa a API da OpenAI para classificar o sentimento predominante de um conjunto de comentários.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "erro: OPENAI_API_KEY não configurada"
    
    # Garante que comentarios é uma lista e tem elementos
    if not isinstance(comentarios, list) or not comentarios:
        return "erro: lista de comentários inválida"

    # Limita a 30 comentários de forma segura
    comentarios_limitados = comentarios[:min(30, len(comentarios))]

    prompt = (
        "Você é um analista simbólico orientado pela psicanálise lacaniana. "
    "Sua tarefa é escutar um conjunto de comentários online e identificar, para cada um, a **posição discursiva do sujeito** — "
    "ou seja, o modo como ele se posiciona diante do outro, do saber, do desejo e da fala.\n\n"
    "⚠️ Não analise o conteúdo da opinião, nem julgue se está certa ou errada.\n"
    "Seu foco é o gesto simbólico da fala, ou seja:\n"
    "– O que ela tenta apagar?\n"
    "– O que ela denuncia sem assumir?\n"
    "– O que ela repete como gozo?\n"
    "– O que ela posiciona como desejo e como defesa?\n\n"
    "Para cada comentário, retorne apenas uma das seguintes posições discursivas (sem explicações):\n"
    "- autodepreciação performada\n"
    "- cinismo afetivo\n"
    "- autoapagamento\n"
    "- gozo por saber\n"
    "- antecipação de crítica\n"
    "- falso moralismo\n"
    "- vulnerabilidade estratégica\n"
    "- apagamento do desejo\n"
    "- cinismo frio\n"
    "- ironia com retorno de culpa\n"
    "- ambivalência visível\n"
    "- neutro\n\n"
    "Comentários:\n"
    f"{chr(10).join(comentarios_limitados)}\n\n"
    "Retorne um JSON com o índice do comentário e a posição discursiva correspondente, como no exemplo:\n"
    '[\n  {"comentario": 1, "posicao": "cinismo afetivo"},\n  {"comentario": 2, "posicao": "gozo por saber"}\n]'
)

    try:
        client = openai.OpenAI(api_key=api_key)
        resposta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um analista de sentimentos objetivo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=10
        )

        return resposta.choices[0].message.content.strip().lower()
    except Exception as e:
        return f"erro: {str(e)}" 