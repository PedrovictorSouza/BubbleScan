def heuristicas_discursivas(posicoes: list[str]) -> list[str]:
    frases = []

    if posicoes.count("autoapagamento") > 3:
        frases.append("Apague-se antes que te apaguem.")

    if posicoes.count("posicionamento de saber") > 3:
        frases.append("Use humildade como escudo para críticas.")

    if posicoes.count("cinismo") > 2:
        frases.append("Finja desdém para mascarar entusiasmo.")

    if not frases:
        frases.append("Fale como quem não quer nada, para poder querer tudo.")

    return frases 