#!/bin/bash

error() {
    echo -e "\033[31m[Erro]\033[0m $1"
}

success() {
    echo -e "\033[32m[Sucesso]\033[0m $1"
}

prompt() {
    local prompt_text=$1
    local var_name=$2

    while true; do
        read -p "$prompt_text: " value
        if [ -z "$value" ]; then
            error "O campo não pode estar vazio."
        else
            break
        fi
    done

    eval $var_name=\$value
}

install_mise() {
    if curl -s https://mise.run | sh; then
        success "Mise CLI instalado com sucesso."
    else
        error "Falha ao instalar Mise CLI."
        exit 1
    fi
}

check_mise_installation() {
    if ~/.local/bin/mise --version > /dev/null 2>&1; then
        success "Mise CLI instalado e verificado com sucesso."
    else
        error "Mise CLI não foi instalado corretamente."
        exit 1
    fi
}

activate_mise() {
    local shell_rc=$1
    echo 'eval "$(~/.local/bin/mise activate zsh)"' >> "$shell_rc"
    success "Mise ativado em $shell_rc. Reinicie o terminal para aplicar as mudanças."
}

add_mise_shims() {
    local shell_profile=$1
    echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> "$shell_profile"
    success "Shims do Mise adicionados ao PATH em $shell_profile. Reinicie o terminal para aplicar as mudanças."
}

echo "Instalação e Configuração do Mise"

install_mise

check_mise_installation

echo "Escolha uma opção para configurar o Mise no seu shell:"
echo "1) Ativar Mise no shell (recomendado)"
echo "2) Adicionar Shims do Mise ao PATH"
echo "3) Sair"

prompt "Escolha a opção desejada [1/2/3]" option

case $option in
    1)
        prompt "Digite o caminho completo do seu arquivo .zshrc (por exemplo, ~/.zshrc ou ~/.bashrc)" shell_rc
        activate_mise "$shell_rc"
        ;;
    2)
        prompt "Digite o caminho completo do seu arquivo .zprofile (por exemplo, ~/.zprofile ou ~/.bash_profile)" shell_profile
        add_mise_shims "$shell_profile"
        ;;
    3)
        echo "Instalação e configuração canceladas."
        exit 0
        ;;
    *)
        error "Opção inválida."
        exit 1
        ;;
esac

success "Script finalizado com sucesso. Lembre-se de reiniciar seu terminal."
exit 0
