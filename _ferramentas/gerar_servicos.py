#!/usr/bin/env python3
"""Gera as páginas de tratamento a partir do conteúdo abaixo (mesmo modelo para todas).

Rode depois de mudar este arquivo:  python3 _ferramentas/gerar_servicos.py
Páginas geradas: /limpeza-dental-resende/, /clareamento-dental-resende/, /alinhadores-transparentes-resende/
Regras do conteúdo: nada de preço, promessa de resultado ou "antes e depois" (use INÍCIO e FIM),
nada que o consultório não ofereça. Medição (GTM + /js/medicao.js) obrigatória em toda página.
"""
import html as H
import json
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = 'https://doutoramarianalyrio.com.br'
VERSAO_MEDICAO = 4  # mesmo ?v= do /js/medicao.js nas outras páginas
WHATS = '5524998424278'
FONTES = 'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&amp;family=Outfit:wght@300;400;500;600&amp;family=Great+Vibes&amp;display=swap'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Rua+Dr+Raphaela+Maria+Bruno+70+Jardim+Jalisco+Resende+RJ'

ICO_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.524 5.855L.057 23.882l6.19-1.438A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.007-1.371l-.36-.214-3.732.867.936-3.423-.234-.373A9.818 9.818 0 1112 21.818z"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'
SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

PAGINAS = [
    {
        'slug': 'limpeza-dental-resende', 'chave': 'limpeza', 'pasta': 'limpeza', 'fotos': 8,
        'nome': 'Limpeza dental profissional',
        'titulo': 'Limpeza Dental em Resende-RJ | Dra. Mariana Lyrio Odontologia',
        'descricao': 'Limpeza dental profissional em Resende-RJ com a Dra. Mariana Lyrio: remoção de tártaro e placa, avaliação da gengiva e orientação de higiene. Agende pelo WhatsApp.',
        'h1': 'Limpeza dental profissional em <em>Resende‑RJ</em>',
        'intro': 'Mesmo com uma boa escovação, a placa bacteriana se acumula em pontos difíceis e, com o tempo, endurece e vira tártaro. A limpeza profissional remove esse acúmulo e deixa os dentes lisos e a gengiva mais saudável.',
        'mensagem': 'Olá! Vi o site e gostaria de agendar uma avaliação para limpeza dental.',
        'passos_titulo': 'Como é a <em>limpeza</em>',
        'passos': [
            ('Avaliação', 'Antes de começar, a Dra. Mariana examina dentes e gengiva. A câmera intraoral mostra na tela o que está acontecendo na sua boca.'),
            ('Remoção de tártaro e placa', 'O tártaro é retirado com instrumentos próprios, inclusive nas regiões perto da gengiva, onde a escova não alcança.'),
            ('Polimento', 'O polimento deixa a superfície dos dentes lisa, o que dificulta o acúmulo de placa nova.'),
            ('Orientação', 'Você sai com orientações de escovação e fio dental pensadas para o seu caso.'),
        ],
        'vantagens_titulo': 'Por que fazer a <em>limpeza</em>',
        'vantagens': [
            'Ajuda a prevenir cáries e doenças da gengiva.',
            'Reduz a inflamação e o sangramento da gengiva causados pela placa.',
            'Remove parte das manchas superficiais de café, chá e cigarro.',
            'É uma chance de identificar problemas no começo, quando o tratamento é mais simples.',
        ],
        'faq': [
            ('A limpeza dói?', 'Em geral, a limpeza é tranquila. Quem tem a gengiva inflamada ou muito tártaro pode sentir um pouco de sensibilidade. O atendimento é feito com calma, com cada etapa explicada antes.'),
            ('De quanto em quanto tempo devo fazer?', 'O intervalo é definido na consulta, conforme a saúde da sua gengiva e a facilidade com que o tártaro se forma na sua boca. Para muitas pessoas, uma revisão a cada seis meses funciona bem.'),
            ('A limpeza deixa os dentes mais brancos?', 'A limpeza remove placa, tártaro e parte das manchas superficiais, então o sorriso costuma ficar mais claro. Ela não muda a cor natural do dente; para isso existe o clareamento dental.'),
            ('Vocês parcelam?', 'Sim, no cartão de crédito. As condições são explicadas na consulta, com transparência.'),
        ],
    },
    {
        'slug': 'clareamento-dental-resende', 'chave': 'clareamento', 'pasta': 'clareamento', 'fotos': 7,
        'nome': 'Clareamento dental',
        'titulo': 'Clareamento Dental em Resende-RJ | Dra. Mariana Lyrio Odontologia',
        'descricao': 'Clareamento dental em Resende-RJ com acompanhamento da Dra. Mariana Lyrio. Avaliação da saúde dos dentes antes de começar e orientação em cada etapa. Agende sua avaliação.',
        'h1': 'Clareamento dental em <em>Resende‑RJ</em>',
        'intro': 'O clareamento deixa os dentes mais brancos com produtos clareadores usados sob acompanhamento profissional. Antes de começar, dentes e gengiva precisam ser avaliados, porque cáries, restaurações e sensibilidade mudam a forma de conduzir o tratamento.',
        'mensagem': 'Olá! Vi o site e gostaria de agendar uma avaliação para clareamento dental.',
        'passos_titulo': 'Como é o <em>clareamento</em>',
        'passos': [
            ('Avaliação', 'A Dra. Mariana confere se há cáries, problemas na gengiva ou restaurações que precisem de atenção, e registra a cor inicial dos seus dentes.'),
            ('Limpeza, se necessário', 'Se houver tártaro ou placa, a limpeza vem antes, para o clareador agir de forma uniforme.'),
            ('Clareamento', 'A técnica é escolhida na avaliação, de acordo com o seu caso e a sua rotina. Você recebe orientações claras sobre como fazer e quais cuidados ter.'),
            ('Acompanhamento', 'A evolução da cor e a sensibilidade são acompanhadas até chegar ao resultado combinado com você.'),
        ],
        'vantagens_titulo': 'O que é bom <em>saber</em>',
        'vantagens': [
            'Restaurações, facetas e coroas não mudam de cor com o clareamento. Isso é avaliado antes.',
            'Pode haver sensibilidade durante o tratamento. Ela costuma passar e é acompanhada pela dentista.',
            'Café, vinho, chá e cigarro merecem atenção durante o tratamento e depois dele.',
            'Com acompanhamento profissional, você sabe exatamente o que está usando nos seus dentes.',
        ],
        'faq': [
            ('Clareamento estraga os dentes?', 'Feito com indicação e acompanhamento profissional, o clareamento é considerado seguro. Por isso a avaliação antes de começar é indispensável.'),
            ('Quanto tempo dura o resultado?', 'Depende dos hábitos de cada pessoa, como o consumo de café, vinho e cigarro. Na consulta, você recebe orientações para manter a cor por mais tempo.'),
            ('O clareamento dá sensibilidade?', 'Algumas pessoas sentem sensibilidade durante o tratamento. Ela costuma ser passageira, e a dentista pode ajustar o tratamento quando necessário.'),
            ('Quem tem restauração pode clarear?', 'Pode, mas as restaurações não mudam de cor. Em alguns casos, elas precisam ser trocadas depois, para acompanhar a nova cor dos dentes. Isso é explicado na avaliação.'),
        ],
    },
    {
        'slug': 'alinhadores-transparentes-resende', 'chave': 'alinhadores', 'pasta': 'sousmile', 'fotos': 7,
        'nome': 'Alinhadores transparentes',
        'titulo': 'Alinhadores Transparentes em Resende-RJ | Dra. Mariana Lyrio',
        'descricao': 'Alinhadores transparentes SouSmile em Resende-RJ com a Dra. Mariana Lyrio, certificada pela SouSmile Academy. Veja a simulação do sorriso antes de começar. Agende sua avaliação.',
        'h1': 'Alinhadores transparentes em <em>Resende‑RJ</em>',
        'intro': 'Os alinhadores são placas transparentes e removíveis, feitas sob medida, que movimentam os dentes aos poucos, sem bráquetes. A Dra. Mariana é certificada pela SouSmile Academy e acompanha o tratamento do planejamento até o fim.',
        'mensagem': 'Olá! Vi o site e gostaria de agendar uma avaliação para alinhadores transparentes.',
        'passos_titulo': 'Como funciona o <em>tratamento</em>',
        'passos': [
            ('Avaliação', 'A dentista entende o que incomoda você no sorriso, examina dentes e gengiva e indica se o seu caso é para alinhadores.'),
            ('Planejamento e simulação', 'Com o planejamento digital da SouSmile, você vê uma simulação do resultado antes de começar.'),
            ('Uso dos alinhadores', 'Você troca de alinhador conforme o planejamento e usa as placas na maior parte do dia, tirando para comer e escovar os dentes.'),
            ('Acompanhamento', 'Nas consultas de acompanhamento, a dentista confere se os dentes estão se movendo como o planejado.'),
        ],
        'vantagens_titulo': 'Vantagens dos <em>alinhadores</em>',
        'vantagens': [
            'São transparentes e discretos no dia a dia.',
            'Saem da boca para comer e para escovar os dentes.',
            'Não têm bráquetes nem fios que costumam machucar a boca.',
            'Você vê a simulação do resultado antes de começar.',
        ],
        'faq': [
            ('Quanto tempo dura o tratamento?', 'Depende de cada caso. Em média, de 6 a 18 meses. Alguns casos simples terminam em menos de 6 meses. O tempo do seu caso é avaliado na consulta.'),
            ('O alinhador dói?', 'É muito mais confortável do que o aparelho fixo. Nos primeiros dias de cada alinhador novo, você pode sentir uma leve pressão, que é sinal de que ele está funcionando.'),
            ('Vocês parcelam?', 'Sim. Além do cartão de crédito, os alinhadores SouSmile podem ser parcelados em até 18 vezes para clientes Nubank. As condições são explicadas na consulta.'),
            ('Qualquer pessoa pode usar alinhador?', 'Muitos casos podem ser tratados com alinhadores, mas não todos. Na avaliação, a dentista indica se o seu caso é para alinhador ou para outro tipo de aparelho.'),
        ],
    },
]


def wa(msg):
    return f'https://wa.me/{WHATS}?text=' + urllib.parse.quote(msg, safe='!')


CABECA_MEDICAO = open(RAIZ / 'politica-de-privacidade' / 'index.html', encoding='utf-8').read()
CABECA_MEDICAO = CABECA_MEDICAO[CABECA_MEDICAO.index('  <!-- Consentimento de cookies'):CABECA_MEDICAO.index('  <!-- End Google Tag Manager -->') + len('  <!-- End Google Tag Manager -->')]
assert 'GTM-W5JPZZMC' in CABECA_MEDICAO and "gtag('consent', 'default'" in CABECA_MEDICAO


def pagina(p):
    url = f"{SITE}/{p['slug']}/"
    outros = [o for o in PAGINAS if o is not p]
    dados = [
        {
            '@context': 'https://schema.org', '@type': 'MedicalWebPage', '@id': url + '#pagina', 'url': url,
            'name': p['titulo'], 'description': p['descricao'], 'inLanguage': 'pt-BR',
            'about': {'@type': 'MedicalProcedure', 'name': p['nome']},
            'publisher': {'@id': f'{SITE}/#consultorio'},
            'isPartOf': {'@type': 'WebSite', 'url': f'{SITE}/', 'name': 'Mariana Lyrio Odontologia'},
        },
        {
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': p['nome'], 'item': url},
            ],
        },
        {
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in p['faq']],
        },
    ]
    passos = '\n'.join(f'        <li><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></li>' for t, d in p['passos'])
    vantagens = '\n'.join(f'        <li>{CHECK}<span>{H.escape(v)}</span></li>' for v in p['vantagens'])
    faq = '\n'.join(f'        <details><summary>{H.escape(q)}</summary><p>{H.escape(r)}</p></details>' for q, r in p['faq'])
    fotos = '\n'.join(
        f'        <figure><img src="/img/casos/{p["pasta"]}/{i}.webp?v=7" width="800" height="1000" loading="lazy" decoding="async" '
        f'alt="Início e fim de {p["nome"].lower()}, caso {i} de {p["fotos"]}, atendido pela Dra. Mariana Lyrio em Resende-RJ"></figure>'
        for i in range(1, p['fotos'] + 1))
    links = '\n'.join(f'        <a href="/{o["slug"]}/" data-botao="link_{o["chave"]}">{H.escape(o["nome"])} em Resende {SETA}</a>' for o in outros)
    links += f'\n        <a href="/#tratamentos" data-botao="link_todos">Todos os tratamentos {SETA}</a>'
    nome_minusculo = p['nome'].lower()
    return f'''<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="UTF-8">
{CABECA_MEDICAO}
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Página gerada por _ferramentas/gerar_servicos.py: edite lá, não aqui. -->
  <title>{H.escape(p['titulo'])}</title>
  <meta name="description" content="{H.escape(p['descricao'])}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{H.escape(p['titulo'])}">
  <meta property="og:description" content="{H.escape(p['descricao'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/img/compartilhar-dra-mariana.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="1200">
  <meta property="og:image:alt" content="Dra. Mariana Lyrio, dentista em Resende-RJ">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(dados, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="{FONTES}">
  <link rel="stylesheet" href="{FONTES}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTES}"></noscript>
  <link rel="stylesheet" href="/css/servico.css?v=1">
</head>

<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W5JPZZMC"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <header class="topo">
    <a class="topo-logo" href="/" aria-label="Mariana Lyrio Odontologia, página inicial"><img src="/img/logo-160.webp" width="160" height="160" alt="Mariana Lyrio Odontologia"></a>
    <a class="topo-voltar" href="/">← Voltar para o site</a>
  </header>

  <main>
    <section class="capa">
      <nav class="trilha" aria-label="Você está em"><a href="/">Início</a> / {H.escape(p['nome'])}</nav>
      <p class="capa-nome">Dra. Mariana Lyrio</p>
      <h1>{p['h1']}</h1>
      <p class="capa-intro">{H.escape(p['intro'])}</p>
      <div class="capa-acoes">
        <a class="btn" href="{wa(p['mensagem'])}" target="_blank" rel="noopener" data-wa-contexto data-tratamento="{p['chave']}" data-botao="pagina_{p['chave']}_topo">{ICO_WA}Agendar minha avaliação</a>
        <div class="capa-prova"><span class="estrelas" aria-hidden="true">★★★★★</span><span>Avaliações no Google Maps</span></div>
      </div>
    </section>

    <section class="secao">
      <p class="etiqueta">Passo a passo</p>
      <h2>{p['passos_titulo']}</h2>
      <ol class="passos">
{passos}
      </ol>
    </section>

    <section class="secao creme">
      <p class="etiqueta">Casos reais</p>
      <h2>Início e fim de casos do <em>consultório</em></h2>
      <p class="texto">Fotos de pacientes atendidos pela Dra. Mariana. Cada caso é diferente; o seu plano é definido na avaliação.</p>
      <div class="casos" tabindex="0" aria-label="Casos de {H.escape(nome_minusculo)}">
{fotos}
      </div>
      <p class="casos-dica">Arraste para o lado para ver mais casos.</p>
    </section>

    <section class="secao">
      <p class="etiqueta">Benefícios</p>
      <h2>{p['vantagens_titulo']}</h2>
      <ul class="vantagens">
{vantagens}
      </ul>
    </section>

    <section class="secao creme">
      <p class="etiqueta">Dúvidas frequentes</p>
      <h2>Perguntas sobre <em>{H.escape(nome_minusculo)}</em></h2>
      <div class="faq">
{faq}
      </div>
    </section>

    <section class="secao">
      <p class="etiqueta">Outros tratamentos</p>
      <h2>Conheça também</h2>
      <div class="outros">
{links}
      </div>
    </section>

    <section class="final">
      <h2>Vamos cuidar do seu sorriso?</h2>
      <p>Agende sua avaliação e conheça um atendimento odontológico pensado para você.</p>
      <a class="btn" href="{wa(p['mensagem'])}" target="_blank" rel="noopener" data-wa-contexto data-tratamento="{p['chave']}" data-botao="pagina_{p['chave']}_final">{ICO_WA}Agendar pelo WhatsApp</a>
      <br><a class="mapa" href="{MAPS}" target="_blank" rel="noopener">Ver como chegar no Google Maps {SETA}</a>
      <div class="final-dados">
        <span>Rua Dr. Raphaela Maria Bruno, 70, Sala 102 · Jardim Jalisco · Resende-RJ · CEP 27510-096</span>
        <span>Segunda a sexta, das 8h às 18h · Sábado mediante agendamento</span>
        <span>WhatsApp: <a href="{wa('Olá! Vi o site e gostaria de agendar uma avaliação.')}" target="_blank" rel="noopener" data-botao="pagina_{p['chave']}_numero">(24) 99842-4278</a></span>
      </div>
    </section>
  </main>

  <footer class="rodape">
    <p>© 2026 Mariana Lyrio Odontologia · Dra. Mariana Lyrio · CRO-RJ 054800</p>
    <p><a href="/politica-de-privacidade/">Política de Privacidade</a> · <a href="#preferencias-cookies" data-cookie-prefs>Preferências de cookies</a></p>
  </footer>

  <a class="wa-float" href="{wa(p['mensagem'])}" target="_blank" rel="noopener" data-wa-contexto data-tratamento="{p['chave']}" data-botao="pagina_{p['chave']}_bolinha" aria-label="Agendar pelo WhatsApp">{ICO_WA}</a>

  <!-- Medição (Google Tag Manager) e texto do WhatsApp conforme a origem da visita -->
  <script src="/js/medicao.js?v={VERSAO_MEDICAO}" defer></script>
</body>

</html>
'''


for p in PAGINAS:
    destino = RAIZ / p['slug'] / 'index.html'
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(pagina(p), encoding='utf-8')
    print('gerado:', destino.relative_to(RAIZ))
