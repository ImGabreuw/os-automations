import subprocess
import os

from base_installer import BaseInstaller

class GduInstaller(BaseInstaller):
    GDU_BINARY_PATH = "/usr/bin/gdu"
    DOWNLOAD_URL = "https://github.com/dundee/gdu/releases/latest/download/gdu_linux_amd64.tgz"

    def is_installed(self):
        return os.path.exists(self.GDU_BINARY_PATH)

    def install(self):
        if self.is_installed():
            self.logger.info("GDU já está instalado.")
            return
        
        self.logger.info("Instalando GDU (ferramenta para uso de disco)...")
        try:
            subprocess.run(f"curl -L {self.DOWNLOAD_URL} | tar xz", shell=True, check=True)
            subprocess.run(["chmod", "+x", "gdu_linux_amd64"], check=True)
            subprocess.run(["sudo", "mv", "gdu_linux_amd64", self.GDU_BINARY_PATH], check=True)
            self.logger.info("GDU instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar GDU: %s", e)
            raise

    def uninstall(self):
        """Desinstala o GDU, se estiver instalado."""
        if not self.is_installed():
            self.logger.info("GDU não está instalado.")
            return

        self.logger.info("Desinstalando GDU...")
        try:
            subprocess.run(["sudo", "rm", "-f", self.GDU_BINARY_PATH], check=True)
            self.logger.info("GDU desinstalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar GDU: %s", e)
            raise
