#!/usr/bin/env python3
"""Gera dentista/resende/index.html a partir do index.html (mesmo conteúdo).

Rode sempre depois de mudar o index.html:  python3 _ferramentas/gerar_paginas.py
A pasta _ferramentas não é publicada (o GitHub Pages ignora pastas com "_").
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = '  <base href="https://doutoramarianalyrio.com.br/">\n'

# Trechos do <head> que mudam na página de Resende: (texto do index, texto da página)
TROCAS = []

html = (RAIZ / 'index.html').read_text(encoding='utf-8')
assert '<head>\n' in html
html = html.replace('<head>\n', '<head>\n' + BASE, 1)
for de, para in TROCAS:
    assert html.count(de) == 1, f'trecho não encontrado (ou repetido): {de[:60]}'
    html = html.replace(de, para)
destino = RAIZ / 'dentista' / 'resende' / 'index.html'
destino.write_text(html, encoding='utf-8')
print('gerado:', destino.relative_to(RAIZ))
