import subprocess
import os

from base_installer import BaseInstaller
from config import PACKAGE_MANAGER

class DockerInstaller(BaseInstaller):
    DOCKER_COMPOSE_URL = "https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-linux-x86_64"
    DOCKER_COMPOSE_PATH = "$HOME/.docker/cli-plugins/docker-compose"
    
    def install(self):
        self.logger.info("Instalando Docker e dependências...")
        try:
            # Instalar Docker e Buildx
            subprocess.run([PACKAGE_MANAGER, "-S", "docker"], check=True)
            subprocess.run([PACKAGE_MANAGER, "-S", "docker-buildx"], check=True)
            
            # Adicionar usuário ao grupo docker
            subprocess.run(["sudo", "usermod", "-aG", "docker", os.getenv("USER")], check=True)
            
            # Iniciar e habilitar o serviço do Docker
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "docker"], check=True)
            
            # Criar diretório para plugins do Docker
            docker_cli_plugins = os.path.expanduser("$HOME/.docker/cli-plugins")
            os.makedirs(docker_cli_plugins, exist_ok=True)
            
            # Baixar Docker Compose
            subprocess.run(["curl", "-SL", self.DOCKER_COMPOSE_URL, "-o", self.DOCKER_COMPOSE_PATH], check=True)
            subprocess.run(["chmod", "+x", self.DOCKER_COMPOSE_PATH], check=True)
            
            self.logger.info("Docker instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro durante a instalação do Docker: %s", e)
            self.uninstall()
            raise

    def update(self):
        self.logger.info("Atualizando Docker...")
        try:
            self.uninstall()
            self.install()
            self.logger.info("Docker atualizado com sucesso!")
        except Exception as e:
            self.logger.error("Erro ao atualizar o Docker: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Docker...")
        try:
            subprocess.run([PACKAGE_MANAGER, "-Rns", "docker"], check=True)
            subprocess.run([PACKAGE_MANAGER, "-Rns", "docker-buildx"], check=True)
            subprocess.run(["rm", "-rf", os.path.expanduser("$HOME/.docker")], check=True)
            self.logger.info("Docker removido com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar o Docker: %s", e)
            raise
