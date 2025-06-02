import os
from dotenv import load_dotenv
import praw
from urllib.parse import urlparse
from typing import List
import time

# Carrega as variáveis de ambiente do .env
load_dotenv()

def coletar_comentarios_reddit(url: str) -> List[str]:
    """
    Coleta comentários de um post do Reddit usando a API PRAW.
    
    Args:
        url: URL do post do Reddit
        
    Returns:
        Lista de strings contendo os comentários
        
    Raises:
        ValueError: Se a URL for inválida ou as credenciais não estiverem configuradas
    """
    inicio = time.time()
    
    # Validação das credenciais
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'BubbleScan/1.0 by u/seu_usuario')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Credenciais do Reddit não configuradas. "
            "Configure as variáveis de ambiente REDDIT_CLIENT_ID e REDDIT_CLIENT_SECRET"
        )
    
    # Inicializa o cliente Reddit com autenticação completa
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        check_for_async=False  # Evita o warning "async environment"
    )
    reddit.read_only = True
    
    try:
        # Extrai o id do post a partir da URL
        path = urlparse(url).path
        # Exemplo de path: /r/python/comments/abc123/titulo_do_post/
        partes = path.strip('/').split('/')
        
        if 'comments' not in partes:
            raise ValueError('URL do Reddit inválida: não encontrou o ID do post')
            
        idx = partes.index('comments')
        if idx + 1 >= len(partes):
            raise ValueError('URL do Reddit inválida: ID do post não encontrado')
            
        post_id = partes[idx+1]
        
        # Busca o post e seus comentários
        submission = reddit.submission(id=post_id)
        print(f"📝 Post encontrado: {submission.title}")
        print(f"📊 Total de comentários: {submission.num_comments}")
        
        submission.comments.replace_more(limit=0)  # Remove comentários aninhados muito profundos
        
        # Coleta apenas os comentários (ignorando título e corpo do post)
        comentarios = [comment.body for comment in submission.comments.list()]
        
        if not comentarios:
            print("⚠️ Nenhum comentário encontrado para este post")
        else:
            print(f"✅ {len(comentarios)} comentários coletados")
            print(f"⏱️ Tempo de coleta: {time.time() - inicio:.2f}s")
            
        return comentarios
        
    except praw.exceptions.PRAWException as e:
        raise ValueError(f"Erro ao acessar o Reddit: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erro ao processar a URL do Reddit: {str(e)}") 