# Conversões offline do Google Ads

Serve para o Google Ads saber quais conversas do WhatsApp viraram pacientes.
Esta pasta **não é publicada no site** e as planilhas com dados reais **não vão para o GitHub**.

## Toda segunda-feira

1. Copie `entrada_modelo.csv` para `entrada.csv` (só na primeira vez) e abra no Excel ou no Google Planilhas.
2. Uma linha por paciente que veio do anúncio (a mensagem chega com "(vim pelo Google)"):
   - `nome`: só para você se achar (não é enviado ao Google);
   - `telefone`: do jeito que estiver, ex.: (24) 99999-0001;
   - `data_hora`: quando agendou ou quando foi atendido, ex.: 03/11/2026 14:30;
   - `status`: `agendou` ou `compareceu`;
   - `valor`: opcional, ex.: 250,00.
3. Salve como CSV e rode, nesta pasta:

   ```
   python3 gerar_conversoes.py
   ```

   Se algum telefone estiver sem DDD, rode `python3 gerar_conversoes.py --ddd-padrao 24`.
4. O programa lista as linhas com erro (corrija e rode de novo) e as com mais de 90 dias (o Google não aceita).
5. No Google Ads: **Metas → Conversões → Uploads → +**, escolha o arquivo `saida_google_ads.csv` e envie.

Antes do primeiro envio, crie no Google Ads as ações de conversão **"Consulta agendada"** e
**"Paciente compareceu"** (origem: importação, dados fornecidos pelo usuário / conversões otimizadas para leads)
e aceite os termos de dados do cliente. Os nomes precisam ser exatamente esses.

Depois de enviar, apague o `saida_google_ads.csv` se não for mais precisar dele (ele tem telefones).
