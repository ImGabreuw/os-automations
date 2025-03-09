import subprocess
import os

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class TomcatInstaller(BaseInstaller):
    INSTALL_DIR = "~/Programs"
    AVAILABLE_VERSIONS = ["9.0.98", "10.1.34"]

    def install(self):
        # Por padrão instalar a versão mais recente
        version = self.version if self.version else self.version[-1]

        if version not in self.AVAILABLE_VERSIONS:
            self.logger.error("Versão não suportada: %s", version)
            return

        self.logger.info("Instalando Apache Tomcat versão %s...", version)

        try:
            download_url = f"https://dlcdn.apache.org/tomcat/tomcat-{version[0]}/v{version}/bin/apache-tomcat-{version}.tar.gz"

            subprocess.run(["wget", download_url, "-O", f"/tmp/tomcat-{version}.tar.gz"], check=True)
            subprocess.run(["tar", "xzf", f"/tmp/tomcat-{version}.tar.gz", "-C", INSTALL_DIR], check=True)

            self.logger.info("Apache Tomcat versão %s instalado com sucesso em %s.", version, f"/opt/tomcat-{version}")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Apache Tomcat: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualização não suportada para Apache Tomcat.")

    def uninstall(self):
        self.logger.info("Desinstalando Apache Tomcat...")
        tomcat_dir = f"{INSTALL_DIR}/tomcat-{self.version}"

        if os.path.exists(tomcat_dir):
            try:
                subprocess.run(["rm", "-rf", tomcat_dir], check=True)
                self.logger.info("Apache Tomcat v%s desinstalado com sucesso.", self.version)
            except subprocess.CalledProcessError as e:
                self.logger.error("Erro ao desinstalar Apache Tomcat v%s: %s", self.version, e)
                raise
        else:
            self.logger.info("Apache Tomcat não encontrado. Nenhuma ação de desinstalação necessária.")
