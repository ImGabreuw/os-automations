import subprocess
import os
import requests
import json
import re

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class JetbrainsInstaller(BaseInstaller):
    INSTALL_DIR = "/opt/jetbrains-toolbox"

    """
    /usr/local/bin: contém executáveis instalados pelo administrador do sistema que não fazem parte do sistema operacional base.
    Referência: https://news.ycombinator.com/item?id=5944334
    """
    SYMLINK_PATH = "/usr/local/bin/jetbrains-toolbox"

    TEMP_TAR = "/tmp/jetbrains-toolbox.tar.gz"

    def install(self):
        self.logger.info("Instalando JetBrains Toolbox...")
        try:
            self.get_latest_toolbox_linux_info()

            subprocess.run(["wget", self.download_url, "-O", self.TEMP_TAR], check=True)
            
            if not os.path.exists(self.INSTALL_DIR):
                os.makedirs(self.INSTALL_DIR, exist_ok=True)
                self.logger.debug("Diretório %s criado.", self.INSTALL_DIR)
            
            subprocess.run(["tar", "xzf", self.TEMP_TAR, "-C", self.INSTALL_DIR], check=True)
            
            # Cria o link simbólico para o executável
            # Após a extração o executável estará em INSTALL_DIR/jetbrains-toolbox.
            executable_path = os.path.join(self.INSTALL_DIR, "jetbrains-toolbox")
            if os.path.exists(executable_path):
                subprocess.run(["ln", "-sf", executable_path, self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink criado: %s -> %s", self.SYMLINK_PATH, executable_path)
            else:
                self.logger.warning("Executável JetBrains Toolbox não encontrado em %s", executable_path)
                return
            
            self.logger.info("JetBrains Toolbox instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar JetBrains Toolbox: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando JetBrains Toolbox...")
        try:
            self.uninstall()
            self.install()
            self.logger.info("JetBrains Toolbox atualizado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao atualizar JetBrains Toolbox: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando JetBrains Toolbox...")
        try:
            if os.path.islink(self.SYMLINK_PATH) or os.path.exists(self.SYMLINK_PATH):
                subprocess.run(["rm", "-f", self.SYMLINK_PATH], check=True)
                self.logger.debug("Symlink %s removido.", self.SYMLINK_PATH)
            else:
                self.logger.debug("Symlink %s não encontrado.", self.SYMLINK_PATH)
            
            if os.path.exists(self.INSTALL_DIR):
                subprocess.run(["rm", "-rf", self.INSTALL_DIR], check=True)
                self.logger.debug("Diretório de instalação %s removido.", self.INSTALL_DIR)
            else:
                self.logger.info("JetBrains Toolbox não está instalado. Nenhuma ação necessária.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar JetBrains Toolbox: %s", e)
            raise

    def get_latest_toolbox_linux_info(self):
        """
        Busca as informações de lançamento mais recentes do aplicativo JetBrains Toolbox para Linux,
        extrai o link e o tamanho do download e os imprime.

        Referência: https://github.com/nagygergo/jetbrains-toolbox-install/blob/master/jetbrains-toolbox.sh
        """

        url = 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança HTTPError para status 4xx ou 5xx
            data = response.json()

            if 'TBA' in data and len(data['TBA']) > 0:
                linux_data = data['TBA'][0]['downloads']['linux']
                download_link = linux_data['link']
                file_size = linux_data['size']

                self.download_url = download_link
            else:
                self.logger.warning("Nenhuma informação de release foi encontrada para o Linux.")

        except requests.exceptions.RequestException as e:
            self.logger.error("Ocorreu um erro durante o envio da requisição para 'Jetbrains Data Service': %s", e)
        except json.JSONDecodeError as e:
            self.logger.error("Erro ao decodificar a resposta JSON: %s", e)
        except KeyError as e:
            self.logger.error("A chave esperada não foi encontrada dentro do JSON: %s", e)
