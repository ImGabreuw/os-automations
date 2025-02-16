import subprocess
import os

from base_installer import BaseInstaller
from modules.mise import MiseInstaller

class LanguageInstaller(BaseInstaller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mise_installer = MiseInstaller()
    
    def is_installed(self, language, version = None):
        """
        Verifica se a linguagem e a versão especificada já estão instaladas.
        Utiliza o comando 'mise list --global' para obter as linguagens instaladas e
        checa se a string '<linguagem>@<versão>' está presente na saída.
        
        Retorna:
            bool: True se estiver instalada, False caso contrário.
        """
        if not self.mise_installer.is_installed():
            return False

        try:
            result = subprocess.run(
                ["mise", "list", "--global"],
                capture_output=True,
                text=True,
                check=True
            )

            if version:
                lines = result.stdout.splitlines()
                for line in lines:
                    if f"{language}" in line and version and f"{version}" in line:
                        installed  = True
                        break
                installed  = False
            else:
                installed = f"{language}" in result.stdout
        
            return installed
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao verificar instalação de %s: %s", language, e)
            return False


    def install(self, language, version):
        """
        Instala a linguagem especificada utilizando o 'mise'.

        Atributos:
        language (str): Nome da linguagem a ser instalada (ex: "node", "python").
        version (str): Versão da linguagem a ser instalada (ex: "22.14.0").

        Exemplo de comando: mise use --global node@22.14.0
        """

        if not self.mise_installer.is_installed():
            self.mise_installer.install()

        self.logger.info("Instalando %s versão %s...", language, version)
        try:
            subprocess.run(
                ["mise", "use", "--global", f"{language}@{version}"],
                check=True
            )
            self.logger.info("%s versão %s instalada com sucesso.", language, version)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar %s: %s", language, e)
            raise

    def update(self):
        """
        Método para atualização da linguagem. 
        Neste exemplo, a atualização não foi implementada, mas pode ser adaptada conforme necessário.
        """
        self.logger.info("Atualização não suportada para %s.", self.language)

    def uninstall(self, language, version):
        """
        Desinstala a linguagem utilizando o 'mise uninstall'.
        Exemplo de comando: mise uninstall -- --global node@22.14.0
        """
        self.logger.info("Desinstalando %s versão %s...", language, version)

        try:
            subprocess.run(
                ["mise", "uninstall", "--", "--global", f"{language}@{version}"],
                check=True
            )
            self.logger.info("%s versão %s desinstalada com sucesso.", language, version)
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar %s: %s", language, e)
            raise
