import subprocess
import os
from base_installer import BaseInstaller

class MiseInstaller(BaseInstaller):

    def install(self):
        self.logger.info("Instalando Mise CLI...")
        try:
            subprocess.run("curl https://mise.run | sh", shell=True, check=True)
            
            mise_path = os.path.expanduser("~/.local/bin/mise")
            if os.path.exists(mise_path):
                self.activate()
                self.logger.info("Mise CLI instalado com sucesso em %s.", mise_path)
            else:
                self.logger.error("Falha na instalação: o binário do Mise não foi encontrado em %s.", mise_path)
                return

            self.logger.info("Mise instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao instalar Mise CLI: %s", e)
            self.uninstall()
            raise

    def activate(self, shell_type=None):
        """
        Configura a ativação do Mise no shell.
        
        Detecta o shell em uso (ou utiliza o valor de `shell_type` se fornecido)
        e adiciona a linha de ativação ao arquivo de configuração correspondente.
        
        Exemplo para zsh:
            echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
        """
        # Detecta o shell se não for informado
        if shell_type is None:
            shell_env = os.environ.get("SHELL", "")
            if "zsh" in shell_env:
                shell_type = "zsh"
                rc_file = os.path.expanduser("~/.zshrc")
            elif "bash" in shell_env:
                shell_type = "bash"
                rc_file = os.path.expanduser("~/.bashrc")
            elif "fish" in shell_env:
                shell_type = "fish"
                rc_file = os.path.expanduser("~/.config/fish/config.fish")
            else:
                shell_type = "bash"
                rc_file = os.path.expanduser("~/.bashrc")
        else:
            if shell_type == "zsh":
                rc_file = os.path.expanduser("~/.zshrc")
            elif shell_type == "bash":
                rc_file = os.path.expanduser("~/.bashrc")
            elif shell_type == "fish":
                rc_file = os.path.expanduser("~/.config/fish/config.fish")
            else:
                rc_file = os.path.expanduser("~/.bashrc")
        
        # Define a linha de ativação; utiliza o caminho completo para o binário do mise.
        mise_path = os.path.expanduser("~/.local/bin/mise")
        activation_line = f'eval "$({mise_path} activate {shell_type})"'
        
        try:
            # Se o arquivo de configuração já existir, verifica se a linha está presente.
            if os.path.exists(rc_file):
                with open(rc_file, "r") as f:
                    content = f.read()
                if activation_line in content:
                    self.logger.info("Linha de ativação já existe em %s.", rc_file)
                else:
                    with open(rc_file, "a") as f:
                        f.write("\n" + activation_line + "\n")
                    self.logger.info("Linha de ativação adicionada ao %s.", rc_file)
            else:
                # Se o arquivo não existir, cria-o e adiciona a linha.
                with open(rc_file, "w") as f:
                    f.write(activation_line + "\n")
                self.logger.info("Arquivo %s criado com a linha de ativação.", rc_file)
            
            self.logger.info("Ativação do Mise configurada para o shell '%s'. Reinicie sua sessão para que as mudanças tenham efeito.", shell_type)
        except Exception as e:
            self.logger.error("Erro ao configurar a ativação do Mise: %s", e)
            raise

    def update(self):
        self.logger.info("Atualizando Mise...")
        try:
            self.uninstall()
            self.install()
            self.logger.info("Mise atualizado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao atualizar Mise: %s", e)
            raise

    def uninstall(self):
        self.logger.info("Desinstalando Mise...")
        try:
            mise_path = os.path.expanduser("~/.local/bin/mise")
            if os.path.exists(mise_path):
                subprocess.run([mise_path, "implode", "--yes"], check=True)
                self.logger.info("Mise desinstalado via 'mise implode' com sucesso.")
            else:
                self.logger.info("Mise não encontrado em %s.", mise_path)
            
            # Lista de diretórios residuais a serem removidos, se existirem
            directories = [
                "~/.local/share/mise",
                "~/.local/state/mise",
                "~/.config/mise",
                "~/.cache/mise"
            ]

            for dir_path in directories:
                full_path = os.path.expanduser(dir_path)
                if os.path.exists(full_path):
                    subprocess.run(["rm", "-rf", full_path], check=True)
                    self.logger.debug("Diretório %s removido.", full_path)
                else:
                    self.logger.debug("Diretório %s não existe, ignorando...", full_path)
            
            self.logger.info("Desinstalação do Mise concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao desinstalar Mise: %s", e)
            raise
