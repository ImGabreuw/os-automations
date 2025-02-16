import shutil

def get_archlinux_package_manager():
    for pm in ["paru", "yay", "pacman"]:
        if shutil.which(pm):
            return pm
    raise EnvironmentError("Nenhum gerenciador de pacotes suportado encontrado!")

PACKAGE_MANAGER = get_archlinux_package_manager()
