import subprocess

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class WineInstaller(BaseInstaller):
    DEPENDENCIES = ["wine", "winetricks", "wine-mono", "wine_gecko", "bottles"]

    def install(self):
        self.logger.info("Instalando Wine e dependências...")
        try:
            # Habilita repositório multilib (caso necessário)
            subprocess.run(["sudo", "sed", "-i", "/\\[multilib\\]/,/Include/s/^#//", "/etc/pacman.conf"], check=True)
            subprocess.run([PACKAGE_MANAGER, "-Sy", "--needed"] + self.DEPENDENCIES + ["--noconfirm"], check=True)
            subprocess.run(["winecfg"], check=True)

            self.logger.info("Wine e dependências instalados com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Wine: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Wine e dependências...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Syu"] + self.DEPENDENCIES + ["--noconfirm"], check=True)
            self.logger.info("Wine e dependências atualizados com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao atualizar Wine: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Wine e dependências...")
        try:
            for pkg in self.DEPENDENCIES:
                result = subprocess.run([PACKAGE_MANAGER, "-Qi", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                if result.returncode == 0:
                    subprocess.run([PACKAGE_MANAGER, "-Rns", pkg, "--noconfirm"], check=True)
                    self.logger.info("%s desinstalado com sucesso.", pkg)
                else:
                    self.logger.info("%s não está instalado, ignorando...", pkg)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Wine e dependências: %s", e)
            raise
