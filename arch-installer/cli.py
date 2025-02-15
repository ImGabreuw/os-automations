import argparse
import logging

from modules.chrome import ChromeInstaller
from modules.jetbrains import JetbrainsInstaller  
from modules.filezilla import FilezillaInstaller  
from modules.tomcat import TomcatInstaller
from modules.wine import WineInstaller
from modules.postman import PostmanInstaller      
from modules.nvim import NvimInstaller      

def main():
    parser = argparse.ArgumentParser(
        description="CLI para gerenciamento da instalação de programas no Arch Linux"
    )
    parser.add_argument(
        "-p", "--program",
        required=True,
        choices=["chrome", "jetbrains", "filezilla", "tomcat", "wine", "postman", "nvim"],
        help="Programa a ser gerenciado"
    )
    parser.add_argument(
        "-a", "--action",
        required=True,
        choices=["install", "update", "uninstall"],
        help="Ação a ser executada"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Habilitar modo debug (logs detalhados)"
    )
    parser.add_argument(
        "-v", "--version",
        help="Versão do programa (quando aplicável, por exemplo, para Tomcat)"
    )
    args = parser.parse_args()

    logging.basicConfig(
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        level=logging.DEBUG if args.debug else logging.INFO
    )

    installers = {
        "chrome": ChromeInstaller,
        "jetbrains": JetbrainsInstaller,
        "filezilla": FilezillaInstaller,
        "tomcat": TomcatInstaller,
        "wine": WineInstaller,
        "postman": PostmanInstaller,
        "nvim": NvimInstaller
    }

    installer_class = installers.get(args.program)
    if installer_class is None:
        print("Programa não encontrado.")
        return

    installer = installer_class(debug=args.debug, version=args.version)

    if args.action == "install":
        installer.install()
    elif args.action == "update":
        installer.update()
    elif args.action == "uninstall":
        installer.uninstall()
    else:
        print("Ação inválida.")

if __name__ == "__main__":
    main()
