# 🕵️‍♂️ SalesWatcher: Pipeline de Automação de Vendas

Este projeto simula um ambiente corporativo real onde arquivos de vendas diárias são recebidos, processados, validados e carregados automaticamente em um banco de dados analítico.

## 🛠 Tecnologias Utilizadas
* **Shell Script (Bash):** Orquestração, manipulação de arquivos, logs e validação de diretórios.
* **Python:** Geração de dados (faker) e interação com Banco de Dados.
* **SQLite:** Armazenamento persistente dos dados processados.
* **SQL:** Consultas analíticas para consolidação de vendas.

## ⚙️ Como funciona a Arquitetura
1.  **Geração:** O script `gerar_vendas.py` cria arquivos CSV aleatórios na pasta `data_raw`.
2.  **Orquestração:** O script `pipeline.sh`:
    * Detecta novos arquivos.
    * Aciona o processador Python.
    * Verifica o código de saída (sucesso/erro).
    * Move arquivos processados para `data_processed`.
    * Registra cada passo em `logs/pipeline.log`.
3.  **Carga:** O script `processar_dados.py` insere os dados no banco SQLite, evitando duplicidades.

## 🚀 Como rodar o projeto

### Pré-requisitos
* Git Bash (Windows) ou Terminal (Linux/Mac)
* Python 3.x

### Passo a Passo
1. Clone o repositório:
```bash
git clone [https://github.com/SEU-USUARIO/SalesWatcher.git](https://github.com/SEU-USUARIO/SalesWatcher.git)
cd SalesWatcher
## 📊 Dashboard Interativo

O projeto conta com uma interface gráfica desenvolvida em **Streamlit** para visualização dos KPIs.

Para rodar o dashboard:
```bash
cd scripts
python -m streamlit run dashboard.py
