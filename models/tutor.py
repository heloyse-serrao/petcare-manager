from models.pessoa import Pessoa


class Tutor(Pessoa):
    """
    Representa o tutor responsável por um ou mais animais.
    """

    def __init__(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
        id_tutor: int | None = None,
    ) -> None:
        super().__init__(nome, telefone, email, id_tutor)

        self.cpf = cpf

    def exibir_dados(self) -> str:
        return (
            f"Tutor: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.telefone}\n"
            f"E-mail: {self.email}"
        )