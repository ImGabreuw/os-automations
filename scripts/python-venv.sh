#!/bin/bash

# ==============================================================================
# FUNÇÕES UTILITÁRIAS
# ==============================================================================

function log_info() {
    echo -e "\e[32m[INFO]\e[0m $1"
}

function log_warn() {
    echo -e "\e[33m[WARN]\e[0m $1"
}

function log_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# ==============================================================================
# INÍCIO DO SCRIPT
# ==============================================================================

VENV_PATH="$(pwd)/venv"

log_info "Configurando ambiente virtual na versão $(python3 --version)"
python -m venv "$VENV_PATH"

chmod +x "$VENV_PATH/bin/activate"
source "$VENV_PATH/bin/activate"

log_info "Sucesso. Ambiente virtual ativado."
