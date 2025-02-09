import subprocess
import os

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class PostmanInstaller(BaseInstaller):
    INSTALL_DIR = "/opt/Postman"

    """
    /usr/local/bin: contém executáveis instalados pelo administrador do sistema que não fazem parte do sistema operacional base.
    Referência: https://news.ycombinator.com/item?id=5944334
    """
    SYMLINK_PATH = "/usr/local/bin/postman"

    DOWNLOAD_URL = "https://dl.pstmn.io/download/latest/linux64"

    TEMP_TAR = "/tmp/postman.tar.gz"

    def install(self):
        self.logger.info("Instalando Postman...")
        try:
            subprocess.run(["wget", self.DOWNLOAD_URL, "-O", self.TEMP_TAR], check=True)
            
            if not os.path.exists(self.INSTALL_DIR):
                os.makedirs(self.INSTALL_DIR, exist_ok=True)
                self.logger.debug("Diretório %s criado.", self.INSTALL_DIR)
            
            subprocess.run(["tar", "xzf", self.TEMP_TAR, "-C", self.INSTALL_DIR], check=True)
            
            # Cria um symlink para o executável do Postman
            # O executável fica em INSTALL_DIR/Postman/Postman
            executable_path = os.path.join(self.INSTALL_DIR, "Postman", "Postman")
            if os.path.exists(executable_path):
                subprocess.run(["ln", "-sf", executable_path, self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink criado: %s -> %s", self.SYMLINK_PATH, executable_path)
            else:
                self.logger.warning("Executável Postman não encontrado em %s", executable_path)
            
            self.logger.info("Postman instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Postman: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Postman...")
        try:
            self.uninstall()
            self.install()
            self.logger.info("Postman atualizado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao atualizar Postman: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Postman...")
        try:
            if os.path.exists(self.SYMLINK_PATH):
                subprocess.run(["rm", "-f", self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink %s removido.", self.SYMLINK_PATH)
            else:
                self.logger.info("Symlink %s não encontrado.", self.SYMLINK_PATH)
            
            if os.path.exists(self.INSTALL_DIR):
                subprocess.run(["rm", "-rf", self.INSTALL_DIR], check=True)
                self.logger.debug("Diretório de instalação %s removido.", self.INSTALL_DIR)
            else:
                self.logger.info("Postman não está instalado. Nenhuma ação necessária.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Postman: %s", e)
            raise
