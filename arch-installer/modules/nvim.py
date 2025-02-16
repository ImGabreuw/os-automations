import subprocess
import os
import requests
import json
import re
import shutil

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class NvimInstaller(BaseInstaller):
    INSTALL_DIR = "/opt/nvim-linux-x86_64"

    """
    /usr/local/bin: contém executáveis instalados pelo administrador do sistema que não fazem parte do sistema operacional base.
    Referência: https://news.ycombinator.com/item?id=5944334
    """
    SYMLINK_PATH = "/usr/local/bin/nvim"

    """
    Tutorial de instalação: https://github.com/neovim/neovim/blob/master/INSTALL.md#install-from-package
    """
    DOWNLOAD_URL = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz"

    TEMP_TAR = "/tmp/nvim-linux-x86_64.tar.gz"

    def is_installed(self):
        return shutil.which("nvim")

    def install(self):
        self.logger.info("Instalando Nvim...")

        try:
            if self.is_installed():
                self.logger.info("Nvim já está instalado.")
                return

            subprocess.run(["curl", "-L", "-o", self.TEMP_TAR, self.DOWNLOAD_URL], check=True)
            
            if not os.path.exists(self.TEMP_TAR):
                self.logger.error("Download falhou. Arquivo %s não encontrado.", self.TEMP_TAR)
                return

            if not os.path.exists(self.INSTALL_DIR):
                subprocess.run(["sudo", "mkdir", "-p", self.INSTALL_DIR], check=True)
                subprocess.run(["sudo", "chown", os.getlogin(), self.INSTALL_DIR], check=True)
                self.logger.debug("Diretório %s criado.", self.INSTALL_DIR)
            
            # --strip-components=1 remove o primeiro nível do caminho dos arquivos extraídos.
            # Exemplo: ao invés de "/opt/nvim-linux-x86_64/nvim-linux-x86_64/bin" -> "/opt/nvim-linux-x86_64/bin"
            subprocess.run(["tar", "xzf", self.TEMP_TAR, "-C", self.INSTALL_DIR, "--strip-components=1"], check=True)
            
            # Cria o link simbólico para o executável
            # Após a extração o executável estará em INSTALL_DIR/bin/nvim.
            executable_path = os.path.join(self.INSTALL_DIR, "bin", "nvim")
            if os.path.exists(executable_path):
                subprocess.run(["sudo", "ln", "-sf", executable_path, self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink criado: %s -> %s", self.SYMLINK_PATH, executable_path)
            else:
                self.logger.warning("Executável Nvim não encontrado em %s", executable_path)
                return
            
            self.logger.info("Nvim instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Nvim: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Nvim...")
        try:
            self.uninstall()
            self.install()
            self.logger.info("Nvim atualizado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao atualizar Nvim: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Nvim...")

        if not self.is_installed():
            self.logger.info("Nvim não está instalado.")
            return

        try:
            if os.path.islink(self.SYMLINK_PATH) or os.path.exists(self.SYMLINK_PATH):
                subprocess.run(["sudo", "rm", "-f", self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink %s removido.", self.SYMLINK_PATH)
            else:
                self.logger.debug("Symlink %s não encontrado.", self.SYMLINK_PATH)
            
            if os.path.exists(self.INSTALL_DIR):
                subprocess.run(["sudo", "rm", "-rf", self.INSTALL_DIR], check=True)
                self.logger.debug("Diretório de instalação %s removido.", self.INSTALL_DIR)
            else:
                self.logger.info("Nvim não está instalado. Nenhuma ação necessária.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Nvim: %s", e)
            raise
