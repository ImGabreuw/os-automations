import os
import re
import sys
import errno
import argparse
import subprocess
import urllib.parse
import time
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_json(url, token, session):
    """
    Gera páginas em JSON a partir da API do GitHub,
    tratando o rate limit.
    """
    headers = {"Authorization": f"token {token}"}

    while url:
        response = session.get(url, headers=headers)
        if response.status_code == 403:
            if response.headers.get("X-RateLimit-Remaining") == "0":
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                sleep_time = max(reset_time - int(time.time()), 0) + 5
                logging.warning(f"Limite de requisições atingido. Aguardando {sleep_time} segundos...")
                time.sleep(sleep_time)
                continue
        response.raise_for_status()
        yield response.json()
        links = response.links
        url = links["next"]["url"] if "next" in links else None

def check_name(name):
    """
    Valida o nome do repositório ou usuário. 
    Permite apenas letras não acentuadas, pontos (.), hífens (-) e números (desde que não inicie com um número), sem caracteres especiais ou acentos.
    """
    if not re.match(r"^(?!\d)[A-Za-z0-9.-]+$", name):
        raise RuntimeError(f"Nome inválido: '{name}'")
    return name


def mkdir(path):
    """
    Cria o diretório, se não existir, com permissões 770.
    """
    try:
        os.makedirs(path, mode=0o770, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Erro ao criar diretório '{path}': {e}")
        raise


def clone(repo_name, ssh_url, to_path):
    """
    Clona o repositório via SSH ou, se já existir, realiza um 'git pull'
    para atualizar as alterações do repositório remoto.
    
    As saídas dos comandos do Git são redirecionadas para evitar que sejam
    exibidas no terminal, ficando disponíveis apenas nos logs do programa.
    """
    repo_path = os.path.join(to_path, repo_name)
    if not os.path.exists(repo_path):
        logging.info(f"Iniciando clone do repositório: {ssh_url}")
        try:
            subprocess.run(
                ["git", "clone", ssh_url, repo_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logging.info(f"Repositório '{repo_name}': SUCESSO")
        except subprocess.CalledProcessError as e:
            logging.error(f"Repositório '{repo_name}': ERRO\n{e}")
            raise
    else:
        logging.info(f"Iniciando atualização do repositório: {repo_name}")
        try:
            subprocess.run(
                ["git", "pull"],
                cwd=repo_path,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logging.info(f"Repositório '{repo_name}': SUCESSO")
        except subprocess.CalledProcessError as e:
            logging.error(f"Repositório '{repo_name}': ERRO\n{e}")


def main():
    parser = argparse.ArgumentParser(description="Backup de repositórios do GitHub via SSH")
    parser.add_argument("username", metavar="USERNAME", help="Seu usuário do GitHub")
    parser.add_argument("directory", metavar="DIRECTORY", help="Diretório para salvar o backup")
    parser.add_argument("token", metavar="TOKEN", help="Seu token de acesso pessoal")
    args = parser.parse_args()

    username = args.username
    token = args.token
    backup_dir = os.path.expanduser(args.directory)

    if mkdir(backup_dir):
        logging.info(f"Diretório criado: {backup_dir}")

    session = requests.Session()
    base_url = "https://api.github.com/user/repos?per_page=100"
    for page in get_json(base_url, token, session):
        for repo in page:
            try:
                name = check_name(repo["name"])
                owner = check_name(repo["owner"]["login"])
            except RuntimeError as e:
                logging.error(e)
                continue

            if username and owner.lower() != username.lower():
                continue

            owner_path = os.path.join(backup_dir, owner)
            mkdir(owner_path)
            try:
                ssh_url = repo.get("ssh_url")
                if not ssh_url:
                    logging.error(f"Repositório {owner}/{name} não possui URL SSH")
                    continue

                clone(name, ssh_url, owner_path)
            except subprocess.CalledProcessError as e:
                logging.error(f"Erro ao atualizar {owner}/{name}: {e}")


if __name__ == "__main__":
    main()
