import re
from typing import List, Optional

def extrair_palavras_validas(texto: str) -> List[str]:
    return re.findall(r'\b\w+\b', texto)

def extrair_json_bruto(texto: str) -> Optional[str]:
    match = re.search(r'\{.*\}', texto, re.DOTALL)
    return match.group(0) if match else None