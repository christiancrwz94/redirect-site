#!/usr/bin/env python3
"""Gera dentista/resende/index.html a partir do index.html (mesmo conteúdo).

Rode sempre depois de mudar o index.html:  python3 _ferramentas/gerar_paginas.py
A pasta _ferramentas não é publicada (o GitHub Pages ignora pastas com "_").
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = '  <base href="https://doutoramarianalyrio.com.br/">\n'

# Trechos do <head> que mudam na página de Resende: (texto do index, texto da página)
TROCAS = [
    ('<title>Dentista em Resende-RJ · Clareamento, Limpeza e Alinhadores | Dra. Mariana Lyrio</title>',
     '<title>Dentista em Resende-RJ · Atendimento de Urgência e Avaliação | Dra. Mariana Lyrio</title>'),
    ('<meta property="og:title" content="Dentista em Resende-RJ · Clareamento, Limpeza e Alinhadores | Dra. Mariana Lyrio">',
     '<meta property="og:title" content="Dentista em Resende-RJ · Atendimento de Urgência e Avaliação | Dra. Mariana Lyrio">'),
    ('content="Dentista em Resende-RJ: clareamento dental, limpeza, alinhador invisível SouSmile e restaurações estéticas. Atendimento de urgência. CRO-RJ 054800.">',
     'content="Dentista em Resende-RJ no Jardim Jalisco: atendimento de urgência, limpeza, clareamento, restaurações e alinhadores SouSmile. Agende pelo WhatsApp. CRO-RJ 054800.">'),
    ('<meta property="og:description" content="Dentista em Resende-RJ: clareamento dental, limpeza, alinhador invisível SouSmile e restaurações estéticas. Agende pelo WhatsApp.">',
     '<meta property="og:description" content="Dentista em Resende-RJ: atendimento de urgência, limpeza, clareamento, restaurações e alinhadores SouSmile. Agende pelo WhatsApp.">'),
    ('<link rel="canonical" href="https://doutoramarianalyrio.com.br/">',
     '<link rel="canonical" href="https://doutoramarianalyrio.com.br/dentista/resende/">'),
    ('<meta property="og:url" content="https://doutoramarianalyrio.com.br/">',
     '<meta property="og:url" content="https://doutoramarianalyrio.com.br/dentista/resende/">'),
]

html = (RAIZ / 'index.html').read_text(encoding='utf-8')
assert '<head>\n' in html
html = html.replace('<head>\n', '<head>\n' + BASE, 1)
for de, para in TROCAS:
    assert html.count(de) == 1, f'trecho não encontrado (ou repetido): {de[:60]}'
    html = html.replace(de, para)
destino = RAIZ / 'dentista' / 'resende' / 'index.html'
destino.write_text(html, encoding='utf-8')
print('gerado:', destino.relative_to(RAIZ))
