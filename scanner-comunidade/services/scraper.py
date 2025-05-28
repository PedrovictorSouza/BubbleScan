import requests
from bs4 import BeautifulSoup

def get_hn_comments(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extrair título do post
    title_tag = soup.select_one('title')
    titulo = title_tag.get_text().replace(' | Hacker News', '').strip() if title_tag else ''
    # ✅ Corrigido: seletor real usado pelo HN para os textos dos comentários
    comments = [div.get_text() for div in soup.select('.commtext')]
    print(f"🔎 Total de comentários coletados: {len(comments)}")
    return {"titulo": titulo, "comentarios": comments} 