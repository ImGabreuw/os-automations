import subprocess

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class ChromeInstaller(BaseInstaller):
    def install(self):
        self.logger.info("Instalando Google Chrome...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-S", "google-chrome", "--noconfirm"], check=True)
            self.logger.info("Google Chrome instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Google Chrome: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Google Chrome...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Syu", "google-chrome", "--noconfirm"], check=True)
            self.logger.info("Google Chrome atualizado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao atualizar Google Chrome: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Google Chrome...")
        try:
            result = subprocess.run([PACKAGE_MANAGER, "-Qi", "google-chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                subprocess.run([PACKAGE_MANAGER, "-Rns", "google-chrome", "--noconfirm"], check=True)
                self.logger.info("Google Chrome desinstalado com sucesso.")
            else:
                self.logger.info("Google Chrome não está instalado. Nenhuma ação de desinstalação necessária.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Google Chrome: %s", e)
            raise
