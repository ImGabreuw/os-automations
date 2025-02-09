import subprocess

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class FilezillaInstaller(BaseInstaller):
    def install(self):
        self.logger.info("Instalando Filezilla...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-S", "filezilla", "--noconfirm"], check=True)
            self.logger.info("Filezilla instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Filezilla: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Filezilla...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Syu", "filezilla", "--noconfirm"], check=True)
            self.logger.info("Filezilla atualizado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao atualizar Filezilla: %s", e)
            self.uninstall()
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Filezilla...")
        try:
            result = subprocess.run([PACKAGE_MANAGER, "-Qi", "filezilla"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                subprocess.run([PACKAGE_MANAGER, "-Rns", "filezilla", "--noconfirm"], check=True)
                self.logger.info("Filezilla desinstalado com sucesso.")
            else:
                self.logger.info("Filezilla não está instalado. Nenhuma ação necessária.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Filezilla: %s", e)
            raise
