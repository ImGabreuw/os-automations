import abc
import logging

class BaseInstaller(abc.ABC):
    def __init__(self, debug=False, version=None):
        self.debug = debug
        self.version = version
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configura o nível do log: DEBUG se o flag for True, senão INFO.
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    @abc.abstractmethod
    def install(self):
        """Realiza a instalação e as configurações pós-instalação."""
        pass

    @abc.abstractmethod
    def update(self):
        """Realiza a atualização do programa ou informa que não é suportado."""
        pass

    @abc.abstractmethod
    def uninstall(self):
        """
        Realiza a desinstalação completa do programa.
        Antes de executar cada etapa, verifica se o pacote, arquivos ou configurações existem.
        """
        pass
