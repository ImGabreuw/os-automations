import subprocess
import os
import requests
import json
import re
import shutil

from base_installer import BaseInstaller
from modules.nvim import NvimInstaller
from modules.mise_language import LanguageInstaller
from config import PACKAGE_MANAGER

class AstroVimInstaller(BaseInstaller):
    INSTALL_DIR = "~/.config/nvim"

    DEPENDENCIES = ["ripgrep", "lazygit", "bottom"]

    DOWNLOAD_URL = "https://github.com/AstroNvim/template.git"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nvim_installer = NvimInstaller()
        self.mise_language_installer = LanguageInstaller()

    def install(self):
        self.logger.info("Iniciando a instalação do AstroVim...")
        try:
            self.logger.info("Instalando dependências ...")

            if not self.nvim_installer.is_installed():
                self.nvim_installer.install()

            self.mise_language_installer.install("node", "22.14.0") # Lastest LTS
            self.mise_language_installer.install("python", "3.13.2") # Lastest stable version

            subprocess.run(
                [PACKAGE_MANAGER, "-Sy", "--needed"] + self.DEPENDENCIES + ["--noconfirm"],
                check=True
            )

            # Instalação do GDU (ferramenta de uso de disco)
            self.install_gdu()

            # Realiza backup dos diretórios existentes do Neovim
            self.logger.info("Realizando backup dos diretórios existentes...")
            backup_dirs = [
                "~/.config/nvim",
                "~/.local/share/nvim",
                "~/.local/state/nvim",
                "~/.cache/nvim"
            ]
            for directory in backup_dirs:
                full_path = os.path.expanduser(directory)
                if os.path.exists(full_path):
                    backup_path = full_path + ".bak"
                    os.rename(full_path, backup_path)
                    self.logger.info("Backup de '%s' realizado para '%s'.", full_path, backup_path)

            # Clonagem do repositório do AstroVim
            full_install_dir = os.path.expanduser(self.INSTALL_DIR)
            self.logger.info("Clonando o repositório do AstroVim em %s...", full_install_dir)
            subprocess.run(
                ["git", "clone", "--depth", "1", self.DOWNLOAD_URL, full_install_dir],
                check=True
            )

            # Remoção do diretório .git para desvincular o template do repositório original
            git_dir = os.path.join(full_install_dir, ".git")
            if os.path.exists(git_dir):
                subprocess.run(["rm", "-rf", git_dir], check=True)
                self.logger.info("Diretório .git removido do template.")

            if not os.path.exists(full_install_dir):
                self.logger.error("Download falhou. Diretório %s não encontrado.", full_install_dir)
                return

            self.logger.info("AstroVim instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar AstroVim: %s", e)
            self.uninstall()
            raise

    def install_gdu(self):
        self.logger.info("Instalando GDU (ferramenta para uso de disco)...")
        try:
            subprocess.run(
                "curl -L https://github.com/dundee/gdu/releases/latest/download/gdu_linux_amd64.tgz | tar xz",
                shell=True,
                check=True
            )

            subprocess.run(["chmod", "+x", "gdu_linux_amd64"], check=True)

            # Move o binário para /usr/bin (necessário permissões de superusuário)
            subprocess.run(["sudo", "mv", "gdu_linux_amd64", "/usr/bin/gdu"], check=True)
            self.logger.info("GDU instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar GDU: %s", e)
            raise

    def update(self):
        self.logger.info("Para atualizar o AstroVim, abra o Neovim e execute o comando ':AstroUpdate'.")

    def uninstall(self):
        self.logger.info("Desinstalando AstroVim e removendo os diretórios de configuração...")
        try:
            dirs = [
                self.INSTALL_DIR,
                "~/.local/state/nvim",
                "~/.local/share/nvim",
                "~/.cache/nvim"
            ]
            for path in dirs:
                full_path = os.path.expanduser(path)
                if os.path.exists(full_path):
                    subprocess.run(["sudo", "rm", "-rf", full_path], check=True)
                    self.logger.debug("Diretório '%s' removido.", full_path)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar AstroVim: %s", e)
            raise
