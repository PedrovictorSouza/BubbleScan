#!/bin/bash

# Ativa o venv e instala dependências se estiverem faltando
source venv/bin/activate || exit
pip install -r requirements.txt
cd scanner-comunidade
uvicorn api:app --reload 