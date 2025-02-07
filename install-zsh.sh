#!/bin/bash

# ==============================================================================
# Script para instalação e configuração automatizada do Zsh.
# - Oh My Zsh
# - Powerlevel10k
# - Plugins (para linguagens, Docker, pass, asdf)
# - Fontes MesloLGS NF (utilizando "powerline fonts")
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

# Verifica se o sistema é Ubuntu
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" != "ubuntu" ]; then
        log_error "Este script foi desenvolvido para Ubuntu."
        exit 1
    fi
else
    log_error "Não foi possível determinar o sistema operacional."
    exit 1
fi

# Verifica privilégios sudo
if [ "$EUID" -ne 0 ]; then
    sudo -v || {
        log_error "Este script necessita de privilégios sudo. Execute-o com um usuário que possua sudo."
        exit 1
    }
fi

# Evitar prompts interativos (como confirmação -y durante a execução de comandos)
export DEBIAN_FRONTEND=noninteractive

log_info "Atualizando os repositórios..."
sudo apt update

# Instalação de dependências essenciais / pré-requisitos
DEPENDENCIES=(curl wget git zsh fonts-powerline)
for pkg in "${DEPENDENCIES[@]}"; do
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        log_info "Instalando pacote: $pkg"
        sudo apt install -y "$pkg"
    else
        log_info "Pacote $pkg já está instalado."
    fi
done

# Instalação do Oh My Zsh
OH_MY_ZSH_DIR="$HOME/.oh-my-zsh"
if [ ! -d "$OH_MY_ZSH_DIR" ]; then
    log_info "Instalando Oh My Zsh..."
    # Faz backup do .zshrc existente, se houver
    if [ -f "$HOME/.zshrc" ]; then
        log_info "Realizando backup do arquivo .zshrc existente..."
        cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%s)"
    fi
    RUNZSH=no KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
else
    log_info "Oh My Zsh já está instalado."
fi

# Configura o Zsh como shell padrão, se ainda não for
if [ "$SHELL" != "$(which zsh)" ]; then
    log_info "Alterando o shell padrão para Zsh..."
    chsh -s "$(which zsh)"
fi

# Instalação do tema Powerlevel10k
POWERLEVEL10K_DIR="${OH_MY_ZSH_DIR}/custom/themes/powerlevel10k"
if [ ! -d "$POWERLEVEL10K_DIR" ]; then
    log_info "Instalando o tema Powerlevel10k..."
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$POWERLEVEL10K_DIR"
else
    log_info "Tema Powerlevel10k já está instalado."
fi

# Download e instalação das fontes MesloLGS NF (necessária para Powerlevel10k)
FONT_DIR="$HOME/.local/share/fonts"
mkdir -p "$FONT_DIR"
declare -A fonts
fonts["MesloLGS NF Regular.ttf"]="https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf"
fonts["MesloLGS NF Bold.ttf"]="https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf"
fonts["MesloLGS NF Italic.ttf"]="https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf"
fonts["MesloLGS NF Bold Italic.ttf"]="https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf"

for font in "${!fonts[@]}"; do
    if [ ! -f "$FONT_DIR/$font" ]; then
        log_info "Baixando fonte $font..."
        wget -q -O "$FONT_DIR/$font" "${fonts[$font]}"
    else
        log_info "Fonte $font já existe."
    fi
done

log_info "Atualizando cache de fontes..."
fc-cache -f -v

# Configuração dos plugins no .zshrc
# Plugins: docker, pass, asdf (e outros para suporte a linguagens)
ZSHRC_FILE="$HOME/.zshrc"
if grep -q "plugins=(" "$ZSHRC_FILE"; then
    log_info "Configurando plugins no .zshrc..."
    # Backup do arquivo .zshrc
    cp "$ZSHRC_FILE" "${ZSHRC_FILE}.backup.$(date +%s)"
    # Define a lista de plugins
    PLUGINS="git docker pass asdf"

    # Instalação do plugin zsh-syntax-highlighting
    SYNTAX_DIR="${OH_MY_ZSH_DIR}/custom/plugins/zsh-syntax-highlighting"
    if [ ! -d "$SYNTAX_DIR" ]; then
        log_info "Instalando plugin zsh-syntax-highlighting..."
        git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$SYNTAX_DIR"
        PLUGINS="$PLUGINS zsh-syntax-highlighting"
    fi

    # Instalação do plugin zsh-autosuggestions
    AUTOSUGGESTIONS_DIR="${OH_MY_ZSH_DIR}/custom/plugins/zsh-autosuggestions"
    if [ ! -d "$AUTOSUGGESTIONS_DIR" ]; then
        log_info "Instalando plugin zsh-autosuggestions..."
        git clone https://github.com/zsh-users/zsh-autosuggestions "$AUTOSUGGESTIONS_DIR"
        PLUGINS="$PLUGINS zsh-autosuggestions"
    fi

    # Atualiza o tema para Powerlevel10k no .zshrc
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="powerlevel10k\/powerlevel10k"/' "$ZSHRC_FILE"
    # Atualiza a linha de plugins
    sed -i "s/^plugins=(.*)/plugins=($PLUGINS)/" "$ZSHRC_FILE"
else
    log_warn "Arquivo .zshrc não contém configuração de plugins. Pulando atualização de plugins."
fi

unset DEBIAN_FRONTEND

log_info "Instalação e configuração concluídas!"
log_info "Por favor, reinicie o terminal ou execute 'exec zsh' para aplicar as novas configurações."
