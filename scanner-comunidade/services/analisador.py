from typing import List, Dict, Optional
import re
from collections import Counter
import time
import json
import os
import openai

from .openai_analisador import analisar_sentimento_com_ia
from services.utils.palavras_chave import extrair_palavras_chave_filtradas
from .utils.texto import extrair_json_bruto
from src.utils.estrategias_discursivas import inferir_posicao_discursiva
from src.utils.heuristicas_simbolicas import heuristicas_discursivas

# Configurações
TECNOLOGIAS_KNOWN = {
    "react", "vue", "nextjs", "copilot", "gpt", "claude", "docker",
    "python", "java", "node", "go", "rust", "fastapi", "huggingface"
}

class AnalisadorTexto:
    """Classe responsável por análise de texto e extração de informações"""
    
    @staticmethod
    def extrair_palavras_chave(comentarios: List[str], top_n: int = 10) -> List[str]:
        """Extrai as palavras-chave mais frequentes dos comentários"""
        return extrair_palavras_chave_filtradas(comentarios, top_n)
    
    @staticmethod
    def identificar_tecnologias(comentarios: List[str]) -> List[str]:
        """Identifica tecnologias mencionadas nos comentários"""
        texto = " ".join(comentarios).lower()
        return [tech for tech in TECNOLOGIAS_KNOWN if tech in texto]

class AnalisadorSociocultural:
    """Classe responsável por análise sociocultural dos comentários"""
    
    @staticmethod
    def limitar_comentarios_por_tokens(comentarios: List[str], max_tokens: int = 14000) -> List[str]:
        """Limita comentários baseado no número de tokens"""
        total_chars = 0
        comentarios_limitados = []
        for c in comentarios:
            total_chars += len(c)
            if total_chars // 4 > max_tokens:
                break
            comentarios_limitados.append(c)
        return comentarios_limitados
    
    @staticmethod
    def _gerar_prompt_analise(comentarios: List[str]) -> str:
        """Gera o prompt para análise sociocultural"""
        return f'''
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
Escolha uma interação onde o sujeito se divide entre dizer e apagar, entre aparecer e sumir. Ex: "O usuário chama seu próprio post de 'besteira sem importância' — isso protega sua imagem ao mesmo tempo em que o posiciona como vulnerável aceitável."

📉 Caso não haja estrutura simbólica clara:
Diga: "O campo simbólico está colapsado — há gozo sem costura e ausência de pacto comum."

Retorne tudo como um JSON válido, sem explicações ou comentários. Use apenas aspas duplas.

Comentários:
{comentarios}
'''
    
    @staticmethod
    def _processar_resposta_openai(content: str) -> Dict:
        """Processa a resposta da OpenAI e extrai o JSON"""
        json_str = extrair_json_bruto(content)
        if json_str:
            try:
                return json.loads(json_str)
            except Exception as e:
                print("DEBUG: Falha ao fazer json.loads no trecho extraído.", e)
                raise
        else:
            print("DEBUG: Não foi possível extrair JSON da resposta.")
            raise ValueError("Resposta da OpenAI não contém JSON válido.")
    
    @staticmethod
    def analisar_com_openai(comentarios: List[str]) -> Dict:
        """Realiza análise sociocultural usando OpenAI"""
        comentarios_limitados = AnalisadorSociocultural.limitar_comentarios_por_tokens(comentarios)
        print("🔐 OPENAI_API_KEY capturada:", os.getenv("OPENAI_API_KEY"))
        
        prompt = AnalisadorSociocultural._gerar_prompt_analise(comentarios_limitados)
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
        
        return AnalisadorSociocultural._processar_resposta_openai(content)
    
    @staticmethod
    def _integrar_heuristicas(resultado: Dict, comentarios: List[str]) -> Dict:
        """Integra heurísticas discursivas ao resultado da análise"""
        posicoes = [inferir_posicao_discursiva(c) for c in comentarios]
        boas_praticas_estendidas = heuristicas_discursivas(posicoes)
        
        if "boas_praticas" in resultado:
            if isinstance(resultado["boas_praticas"], list):
                resultado["boas_praticas"] += boas_praticas_estendidas
            elif isinstance(resultado["boas_praticas"], str):
                resultado["boas_praticas"] = [resultado["boas_praticas"]] + boas_praticas_estendidas
            else:
                resultado["boas_praticas"] = boas_praticas_estendidas
        else:
            resultado["boas_praticas"] = boas_praticas_estendidas
        
        return resultado
    
    @staticmethod
    def analisar(comentarios: List[str]) -> Dict:
        """Realiza análise sociocultural completa"""
        try:
            print("🔍 Tentando análise com OpenAI...")
            resultado = AnalisadorSociocultural.analisar_com_openai(comentarios)
            print("✅ OpenAI retornou com sucesso.")
            
            # Integração das heurísticas discursivas e simbólicas
            resultado = AnalisadorSociocultural._integrar_heuristicas(resultado, comentarios)
            
            return resultado
        except Exception as e:
            print("❌ Falha ao usar OpenAI:", str(e))
            raise e

class AnalisadorComentarios:
    """Classe principal para análise de comentários"""
    
    def __init__(self):
        self.analisador_texto = AnalisadorTexto()
        self.analisador_sociocultural = AnalisadorSociocultural()
    
    def analisar_comentarios(self, comentarios: List[str]) -> Dict:
        """
        Analisa uma lista de comentários e retorna um dicionário com os resultados.
        """
        inicio = time.time()
        print(f"\n🔍 Iniciando análise de {len(comentarios)} comentários...")
        
        # Analisa o sentimento
        sentimento = analisar_sentimento_com_ia(comentarios)
        print(f"😊 Sentimento detectado: {sentimento}")
        
        # Extrai palavras-chave
        palavras_chave = extrair_palavras_chave_filtradas(comentarios)
        print(f"🔑 Palavras-chave extraídas: {', '.join(palavras_chave)}")
        
        # Identifica tecnologias
        tecnologias = self.analisador_texto.identificar_tecnologias(comentarios)
        print(f"💻 Tecnologias identificadas: {', '.join(tecnologias)}")
        
        print(f"⏱️ Tempo de análise: {time.time() - inicio:.2f}s")
        
        return {
            "sentimento": sentimento,
            "palavras_chave": palavras_chave,
            "tecnologias": tecnologias
        }
    
    def analise_sociocultural(self, comentarios: List[str]) -> Dict:
        """Realiza análise sociocultural dos comentários"""
        return self.analisador_sociocultural.analisar(comentarios)

# Funções de conveniência para manter compatibilidade
def analisar_comentarios(comentarios: List[str]) -> Dict:
    """Função de conveniência para análise básica de comentários"""
    analisador = AnalisadorComentarios()
    return analisador.analisar_comentarios(comentarios)

def analise_sociocultural(comentarios: List[str]) -> Dict:
    """Função de conveniência para análise sociocultural"""
    analisador = AnalisadorComentarios()
    return analisador.analise_sociocultural(comentarios)

def analise_sociocultural_openai(comentarios: List[str]) -> Dict:
    """Função de conveniência para análise sociocultural com OpenAI"""
    return AnalisadorSociocultural.analisar_com_openai(comentarios)
