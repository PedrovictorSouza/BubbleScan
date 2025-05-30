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
        "Você é um analista de comunidades técnicas. Dado esse conjunto de comentários extraídos do Hacker News, "
        "retorne apenas uma palavra (sem explicações) que defina o sentimento coletivo predominante. "
        "Exemplos de sentimentos: entusiasmo, frustração, ceticismo, esperança, estresse, humor, indiferença.\n\n"
        f"Comentários:\n{chr(10).join(comentarios_limitados)}\n"
        "\nSentimento predominante:"
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