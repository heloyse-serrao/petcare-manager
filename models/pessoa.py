from abc import ABC, abstractmethod


class Pessoa(ABC):
    """
    Classe abstrata que representa uma pessoa da clínica.
    """

    def __init__(
        self,
        nome: str,
        telefone: str,
        email: str,
        id_pessoa: int | None = None,
    ) -> None:
        self.id = id_pessoa
        self.nome = nome
        self.telefone = telefone
        self.email = email

    @abstractmethod
    def exibir_dados(self) -> str:
        """
        Método que deve ser implementado pelas subclasses.
        """
        pass

    def __str__(self) -> str:
        return self.exibir_dados()