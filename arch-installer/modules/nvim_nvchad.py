import subprocess
import os
import requests
import json
import re

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class NvChadInstaller(BaseInstaller):
    INSTALL_DIR = "~/.config/nvim"

    DEPENDENCIES = ["ripgrep"]

    DOWNLOAD_URL = "https://github.com/NvChad/starter"

    def install(self):
        self.logger.info("Instalando NvChad...")
        try:
            self.logger.info("Instalando dependências...")
            subprocess.run([PACKAGE_MANAGER, "-Sy", "--needed"] + self.DEPENDENCIES + ["--noconfirm"], check=True)

            full_install_dir = os.path.expanduser(self.INSTALL_DIR)
            subprocess.run(["git", "clone", self.DOWNLOAD_URL, full_install_dir], check=True)
            
            if not os.path.exists(full_install_dir):
                self.logger.error("Download falhou. Diretório %s não encontrado.", full_install_dir)
                return
            
            self.logger.info("NvChad instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar NvChad: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Para atualizar o NvChad, basta digital 'Lazy sync' dentro do Nvim.")

    def uninstall(self):
        self.logger.info("Desinstalando NvChad...")
        try:
            dirs = [self.INSTALL_DIR, "~/.local/state/nvim", "~/.local/share/nvim"]

            for path in paths:
                full_path = os.path.expanduser(path)

                if os.path.exists(full_path):
                    subprocess.run(["rm", "-rf", full_path], check=True)
                    self.logger.debug("Diretório de instalação %s removido.", full_path)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar NvChad: %s", e)
            raise
