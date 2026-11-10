#!/usr/bin/env python3
"""Gera o arquivo de importação de conversões offline do Google Ads.

Lê a planilha de pacientes (nome, telefone, data_hora, status, valor) e grava
saida_google_ads.csv no formato "dados fornecidos pelo usuário" do Google Ads.

Uso (dentro desta pasta):
    python3 gerar_conversoes.py                      # lê entrada.csv
    python3 gerar_conversoes.py minha_planilha.csv   # lê outro arquivo
    python3 gerar_conversoes.py entrada.csv --ddd-padrao 24   # completa telefones sem DDD

Só usa a biblioteca padrão do Python. O nome do paciente NÃO vai para o arquivo de saída.
"""
import argparse
import csv
import re
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

PASTA = Path(__file__).resolve().parent
NOMES_CONVERSAO = {'agendou': 'Consulta agendada', 'compareceu': 'Paciente compareceu'}
DIAS_MAXIMOS = 90
DDDS_VALIDOS = {
    11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 28, 31, 32, 33, 34, 35, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69,
    71, 73, 74, 75, 77, 79, 81, 82, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99,
}
FORMATOS_DATA = [
    ('%d/%m/%Y %H:%M:%S', True), ('%d/%m/%Y %H:%M', True), ('%d/%m/%Y', False),
    ('%d/%m/%y %H:%M', True), ('%d/%m/%y', False),
    ('%Y-%m-%d %H:%M:%S', True), ('%Y-%m-%d %H:%M', True), ('%Y-%m-%dT%H:%M:%S', True),
    ('%Y-%m-%dT%H:%M', True), ('%Y-%m-%d', False),
]


def sem_acento(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')


def telefone_e164(bruto, ddd_padrao=None):
    """Devolve (telefone em +55DDDNUMERO, None) ou (None, motivo)."""
    d = re.sub(r'\D', '', bruto or '')
    if not d:
        return None, 'telefone vazio'
    if d.startswith('00'):          # 0055... (discagem internacional)
        d = d[2:]
    if d.startswith('55') and len(d) in (12, 13):
        d = d[2:]
    if d.startswith('0'):           # 0 + DDD (024...) ou 0 + operadora + DDD (01524...)
        d = d[1:]
        if len(d) in (12, 13):
            d = d[2:]
    if len(d) in (8, 9):
        if not ddd_padrao:
            return None, 'telefone sem DDD (use --ddd-padrao 24 para completar)'
        d = str(ddd_padrao) + d
    if len(d) not in (10, 11):
        return None, 'telefone com quantidade de números inválida'
    ddd, numero = int(d[:2]), d[2:]
    if ddd not in DDDS_VALIDOS:
        return None, f'DDD {ddd} não existe'
    if len(numero) == 8 and numero[0] in '6789':
        numero = '9' + numero        # celular antigo, sem o 9 na frente
    if len(numero) == 9 and numero[0] != '9':
        return None, 'celular com 9 dígitos precisa começar com 9'
    if len(numero) == 8 and numero[0] not in '2345':
        return None, 'telefone fixo inválido'
    return f'+55{ddd}{numero}', None


def data_hora(bruto):
    texto = (bruto or '').strip()
    for fmt, tem_hora in FORMATOS_DATA:
        try:
            dt = datetime.strptime(texto, fmt)
        except ValueError:
            continue
        return dt if tem_hora else dt.replace(hour=12), None
    return None, 'data/hora em formato desconhecido (use 03/11/2026 14:30)'


def valor(bruto):
    texto = re.sub(r'[^\d,.-]', '', bruto or '')
    if not texto:
        return '', None
    if ',' in texto:                 # formato brasileiro: 1.200,50
        texto = texto.replace('.', '').replace(',', '.')
    try:
        v = float(texto)
    except ValueError:
        return None, 'valor inválido'
    if v < 0:
        return None, 'valor negativo'
    return f'{v:.2f}', None


def ler_planilha(caminho):
    for codificacao in ('utf-8-sig', 'cp1252'):
        try:
            texto = caminho.read_text(encoding=codificacao)
            break
        except UnicodeDecodeError:
            continue
    else:
        sys.exit(f'Não consegui ler {caminho.name}: salve a planilha como CSV UTF-8.')
    primeira = texto.splitlines()[0] if texto else ''
    separador = ';' if primeira.count(';') > primeira.count(',') else ','
    leitor = csv.DictReader(texto.splitlines(), delimiter=separador)
    leitor.fieldnames = [sem_acento(c or '').strip().lower() for c in (leitor.fieldnames or [])]
    faltando = {'telefone', 'data_hora', 'status'} - set(leitor.fieldnames)
    if faltando:
        sys.exit(f'Faltam colunas na planilha: {", ".join(sorted(faltando))}. Use o entrada_modelo.csv.')
    return list(leitor)


def main():
    ap = argparse.ArgumentParser(description='Gera saida_google_ads.csv para importar conversões offline no Google Ads.')
    ap.add_argument('entrada', nargs='?', default=str(PASTA / 'entrada.csv'))
    ap.add_argument('--saida', default=str(PASTA / 'saida_google_ads.csv'))
    ap.add_argument('--ddd-padrao', type=int, help='DDD para telefones escritos sem DDD (ex.: 24)')
    args = ap.parse_args()

    entrada = Path(args.entrada)
    if not entrada.exists():
        sys.exit(f'Arquivo não encontrado: {entrada}\nCopie entrada_modelo.csv para entrada.csv e preencha.')
    agora = datetime.now()
    limite = agora - timedelta(days=DIAS_MAXIMOS)

    linhas_ok, invalidas, antigas, vistas = [], [], [], set()
    for n, linha in enumerate(ler_planilha(entrada), start=2):  # linha 1 é o cabeçalho
        if not any((v or '').strip() for v in linha.values()):
            continue
        nome = (linha.get('nome') or '').strip() or '(sem nome)'
        status = sem_acento((linha.get('status') or '').strip().lower())
        motivo = None
        if status not in NOMES_CONVERSAO:
            motivo = f'status "{linha.get("status", "")}" (use agendou ou compareceu)'
        tel, m = telefone_e164(linha.get('telefone'), args.ddd_padrao)
        motivo = motivo or m
        dt, m = data_hora(linha.get('data_hora'))
        motivo = motivo or m
        val, m = valor(linha.get('valor'))
        motivo = motivo or m
        if not motivo and dt > agora + timedelta(minutes=5):
            motivo = 'data no futuro'
        if motivo:
            invalidas.append((n, nome, motivo))
            continue
        if dt < limite:
            antigas.append((n, nome))
            continue
        chave = (tel, status, dt)
        if chave in vistas:
            continue
        vistas.add(chave)
        linhas_ok.append([tel, NOMES_CONVERSAO[status], dt.strftime('%Y-%m-%d %H:%M:%S'), val, 'BRL'])

    with open(args.saida, 'w', encoding='utf-8', newline='') as f:
        f.write('Parameters:TimeZone=America/Sao_Paulo\n')
        w = csv.writer(f)
        w.writerow(['Phone Number', 'Conversion Name', 'Conversion Time', 'Conversion Value', 'Conversion Currency'])
        w.writerows(linhas_ok)

    print(f'Pronto: {len(linhas_ok)} conversões gravadas em {Path(args.saida).name}.')
    if antigas:
        print(f'\nIgnoradas por terem mais de {DIAS_MAXIMOS} dias ({len(antigas)}):')
        for n, nome in antigas:
            print(f'  linha {n}: {nome}')
    if invalidas:
        print(f'\nDescartadas por erro ({len(invalidas)}) — corrija na planilha e rode de novo:')
        for n, nome, motivo in invalidas:
            print(f'  linha {n}: {nome} — {motivo}')


if __name__ == '__main__':
    main()
