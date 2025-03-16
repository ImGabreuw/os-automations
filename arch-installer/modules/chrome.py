import subprocess

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER


class ChromeInstaller(BaseInstaller):
    DEPENDENCIES = ["google-chrome", "noto-fonts-emoji"]

    def install(self):
        self.logger.info("Instalando Google Chrome...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Sy", "--needed"] + self.DEPENDENCIES + ["--noconfirm"], check=True)
            self.logger.info("Google Chrome instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Google Chrome: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Google Chrome...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Syu"] + self.DEPENDENCIES + ["--noconfirm"], check=True)
            self.logger.info("Google Chrome atualizado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao atualizar Google Chrome: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Google Chrome...")
        try:
            for pkg in self.DEPENDENCIES:
                result = subprocess.run([PACKAGE_MANAGER, "-Qi", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                if result.returncode == 0:
                    subprocess.run([PACKAGE_MANAGER, "-Rns", pkg, "--noconfirm"], check=True)
                    self.logger.info("%s desinstalado com sucesso.", pkg)
                else:
                    self.logger.info("%s não está instalado, ignorando...", pkg)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Google Chrome: %s", e)
            raise
