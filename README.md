# Gerador de Contratos — Contrato de Arrendamento Urbano

Um gerador simples de contratos de arrendamento para fins habitacionais, construído com Streamlit e docxtpl. A aplicação preenche um modelo Word (.docx) com dados introduzidos via formulário web e gera um ficheiro DOCX (e opcionalmente PDF, se LibreOffice estiver disponível para conversão).

## Funcionalidades

- UI web (Streamlit) para introdução dos dados do senhorio e inquilino.
- Preenchimento de um modelo Word (`.docx`) usando `docxtpl` (placeholders Jinja-like).
- Geração de ficheiro DOCX pronto a assinar e, opcionalmente, conversão para PDF (via LibreOffice). 
- Validações básicas de campos obrigatórios, IBAN simples e lógica de datas.
- Scripts utilitários em `scripts/` para criar/limpar/ testar templates.

## Estrutura do projeto (resumo)

- `gerador/app.py` — Streamlit app (entrada principal).
- `contract_template.txt` — contrato original em texto (usado como fonte para gerar `.docx` se necessário).
- `contract_template.docx` — modelo `.docx` utilizado por `app.py` (o app prefere `.docx` ao `.txt` quando ambos existem).
- `test_render_clean.docx`, `contract_template_clean.docx` — arquivos gerados durante o desenvolvimento / testes.
- `requirements.txt` — dependências Python.
- `scripts/` — utilitários para converter/gerar templates e testar renderização.
- `myenv/` — (opcional) virtualenv local (não comitado).

## Requisitos

- Python 3.10+ (o ambiente de desenvolvimento usa Python 3.12)
- Recomenda-se utilizar um virtualenv (venv / virtualenv)
- Dependências listadas em `requirements.txt` (ex.: `streamlit`, `docxtpl`, `python-docx`, `num2words`)
- (Opcional) LibreOffice instalado e disponível em PATH para conversão a PDF: `libreoffice --headless --convert-to pdf`.

## Instalação e configuração (Windows / PowerShell)

1. Criar e ativar um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências

```powershell
pip install -r requirements.txt
```

3. Verifique se o template `.docx` existe em `gerador/contract_template.docx`. O `app.py` procura por `contract_template.txt` e, se existir um sibling `.docx`, usará o `.docx` automaticamente. Se preferir usar outro ficheiro, atualize a constante `TEMPLATE` em `app.py`.

4. (Opcional) Instalar LibreOffice para converter para PDF (se desejar a opção PDF no UI): baixe/instale de https://www.libreoffice.org/

## Executar a aplicação (Streamlit)

No PowerShell, a partir da pasta `gerador/`:

```powershell
cd c:\Users\ricki\Documents\Freelance\Projects\Marlene\gerador
streamlit run app.py
```

Abra o browser em `http://localhost:8501`.

## Template e placeholders

- O modelo Word utiliza placeholders no estilo Jinja, por exemplo `{{ inquilino }}`, `{{ valor_renda }}`, `{{ document_type }}`, etc.
- Certifique-se de que os nomes de placeholders no `.docx` correspondem às chaves do `context` no `app.py`. Durante o desenvolvimento as chaves foram normalizadas em snake_case (por exemplo `document_number`, `valor_renda`, `contract_date_local`).
- Se tiver um ficheiro `.txt` (como `contract_template.txt`) com o texto do contrato, há um script que converte para `.docx` e normaliza placeholders (veja `scripts/`).

## Geração de PDF

- A conversão para PDF é feita chamando o LibreOffice em modo headless. Se LibreOffice não estiver instalado ou não estiver no PATH, a app continuará a gerar apenas o DOCX e apresentará uma mensagem informativa.

## Boas práticas e personalização

- Para preservar formatação, mantenha um `contract_template.docx` com todos os parágrafos, estilos e quebras de página desejadas.
- Evite placeholders quebrados (ex.: `{{valor_renda)}`) — a sintaxe deve ser `{{ valor_renda }}`.
- Teste renderizações com dados de amostra antes de gerar contratos finais.

## Scripts úteis

- `scripts/create_clean_template.py` — cria um `contract_template.docx` limpo a partir do `.txt` e normaliza placeholders.
- `scripts/create_and_test_template.py` — cria e testa uma renderização com valores de exemplo.

## Como subir este projeto para o GitHub (passos)

1. Inicializar repositório local (a executar na pasta `gerador/`):

```powershell
cd c:\Users\ricki\Documents\Freelance\Projects\Marlene\gerador
git init
git add .
git commit -m "chore: initial import of contract generator"
```

2. Criar um repositório remoto no GitHub (via web UI ou `gh` CLI). Se usar a web UI, crie um novo repo sem README (já tem local).

3. Adicionar o remote e fazer push (exemplo):

```powershell
# substitua <your-repo-url> pelo URL do repositório GitHub (HTTPS ou SSH)
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

Se quiser usar a CLI `gh`:

```powershell
gh repo create <username>/<repo-name> --public --source=. --remote=origin --push
```

Observação: eu não posso subir automaticamente para o seu GitHub (não tenho credenciais). Siga os passos acima localmente ou diga-me se pretende que eu gere os comandos para si e eu os execute aqui (se lhe for conveniente fornecer unicamente a autorização no seu ambiente).

## Troubleshooting

- Problema: "Template file not found" — Verifique que `contract_template.docx` está no mesmo diretório que `app.py` (ou ajuste `TEMPLATE`).
- Problema: "Failed to render template" — normalmente placeholders têm nomes incorretos ou sintaxe Jinja inválida. Abra o `.docx` no Word e verifique os tokens `{{ ... }}`.
- Problema: "PDF conversion failed" — confirme que LibreOffice está instalado e acessível via `libreoffice` no PATH.

## Contribuição

Sinta-se à vontade para abrir issues e pull requests. Sugestões úteis:
- Automatizar mapeamentos de placeholders (PT → snake_case)
- Melhorar validações de IBAN (uso de bibliotecas de validação)
- Adicionar testes automatizados para renderização de templates
