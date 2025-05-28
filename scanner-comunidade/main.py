from services.scraper import get_hn_comments
from services.analisador import analisar_comentarios
import json

def main():
    # URL de exemplo (pode ser passada como argumento depois)
    url = "https://news.ycombinator.com/item?id=44085920"
    
    print("🔍 Coletando comentários...")
    comentarios = get_hn_comments(url)
    
    print("📊 Analisando comentários...")
    resultado = analisar_comentarios(comentarios)
    
    # Formata o resultado para exibição
    print("\n📝 Resultado da Análise:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 