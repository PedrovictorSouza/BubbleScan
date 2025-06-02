import re

def inferir_posicao_discursiva(comentario: str) -> str:
    if re.search(r"(?i)\bi know this is stupid\b|\bprobably wrong\b|\bdon't attack me\b", comentario):
        return "autoapagamento"
    elif "as a dev" in comentario or "we all know" in comentario:
        return "posicionamento de saber"
    elif re.match(r"(?i)^lol|haha|lmao", comentario.strip()):
        return "cinismo"
    else:
        return "neutro" 