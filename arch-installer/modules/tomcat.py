import os
import subprocess

from base_installer import BaseInstaller


class TomcatInstaller(BaseInstaller):
    AVAILABLE_VERSIONS = ["9.0.102", "10.1.39"]

    INSTALL_DIR = "~/Programs"

    def install(self):

        format_version_list = "\n".join([f"{i + 1}. Tomcat {v}" for i, v in enumerate(self.AVAILABLE_VERSIONS)])
        print(format_version_list)

        try:
            version = int(input("Selecione uma versão: ").strip());

            if not (1 < version <= len(self.AVAILABLE_VERSIONS)):
                raise ValueError

            version = self.AVAILABLE_VERSIONS[version - 1]

        except (ValueError, IndexError):
            self.logger.error("Versão inválida.")
            return

        if version not in self.AVAILABLE_VERSIONS:
            self.logger.error("Versão não suportada: %s", version)
            return

        self.logger.info("Instalando Apache Tomcat versão %s...", version)

        try:
            major_version = version.split(".")[0]
            download_url = f"https://dlcdn.apache.org/tomcat/tomcat-{major_version}/v{version}/bin/apache-tomcat-{version}.tar.gz"
            subprocess.run(["wget", download_url, "-O", f"/tmp/tomcat-{version}.tar.gz"], check=True)

            full_install_dir = os.path.expanduser(self.INSTALL_DIR)
            if not os.path.exists(full_install_dir):
                os.makedirs(full_install_dir, exist_ok=True)
                self.logger.info("Diretório %s criado.", full_install_dir)

            subprocess.run(["tar", "xzf", f"/tmp/tomcat-{version}.tar.gz", "-C", full_install_dir], check=True)

            self.logger.info("Apache Tomcat versão %s instalado com sucesso em %s.", version,
                             f"{full_install_dir}/tomcat-{version}")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Apache Tomcat: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualização não suportada para Apache Tomcat.")

    def uninstall(self):
        self.logger.info("Desinstalando Apache Tomcat...")

        full_install_dir = os.path.expanduser(self.INSTALL_DIR)
        tomcat_dir = f"{full_install_dir}/tomcat-{self.version}"

        if os.path.exists(tomcat_dir):
            try:
                subprocess.run(["rm", "-rf", tomcat_dir], check=True)
                self.logger.info(f"Apache Tomcat v{self.version} desinstalado com sucesso.")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Erro ao desinstalar Apache Tomcat v{self.version}: %s", e)
                raise
        else:
            self.logger.info("Apache Tomcat não encontrado. Nenhuma ação de desinstalação necessária.")
