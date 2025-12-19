#!/bin/bash

# --- CONFIGURAÇÕES ---
PASTA_RAW="../data_raw"
PASTA_PROCESSED="../data_processed"
ARQUIVO_LOG="../logs/pipeline.log"

# Função para facilitar o log (escreve na tela e no arquivo ao mesmo tempo)
log_msg() {
    local mensagem="$1"
    local data_hora=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$data_hora] $mensagem" >> "$ARQUIVO_LOG"
    echo "[$data_hora] $mensagem"
}

# --- INÍCIO DO PROCESSO ---
log_msg "========================================"
log_msg "Iniciando Pipeline de Vendas..."

# Verifica se existem arquivos CSV na pasta RAW
# O 'ls' joga erros no lixo (/dev/null) para não sujar a tela se estiver vazia
qtd_arquivos=$(ls "$PASTA_RAW"/*.csv 2> /dev/null | wc -l)

if [ "$qtd_arquivos" -eq 0 ]; then
    log_msg "Nenhum arquivo novo para processar."
    exit 0
fi

log_msg "Encontrados $qtd_arquivos arquivos para processar."

# Loop para processar cada arquivo
for arquivo in "$PASTA_RAW"/*.csv
do
    filename=$(basename "$arquivo")
    log_msg "--> Processando: $filename"

    # 1. AQUI VAI ENTRAR O SCRIPT PYTHON DE BANCO DE DADOS (EM BREVE)
    # Por enquanto, vamos simular um processamento de 1 segundo
	filename=$(basename "$arquivo")
    log_msg "--> Processando: $filename"

    # --- A MÁGICA ACONTECE AQUI ---
    # Chama o Python passando o arquivo atual como argumento ($arquivo)
    python processar_dados.py "$arquivo"

    # Captura o resultado do Python (0 = Sucesso, Outro número = Erro)
    STATUS_PYTHON=$?

    if [ $STATUS_PYTHON -eq 0 ]; then
        # Se o Python deu ok, movemos o arquivo
        mv "$arquivo" "$PASTA_PROCESSED/"
        log_msg "Sucesso: Dados inseridos e arquivo movido para processados."
    else
        # Se o Python falhou, NÃO movemos e avisamos no log
        log_msg "ERRO CRÍTICO: O Python falhou ao ler $filename. O arquivo permanecerá na pasta RAW."
    fi

    # 2. Mover para a pasta de processados (Arquivo Morto)
    mv "$arquivo" "$PASTA_PROCESSED/"

    # Verifica se o comando 'mv' deu certo ($? == 0)
    if [ $? -eq 0 ]; then
        log_msg "Sucesso: $filename movido para processados."
    else
        log_msg "ERRO CRÍTICO: Falha ao mover $filename."
    fi
done

log_msg "Pipeline finalizado com sucesso."
log_msg "========================================"
