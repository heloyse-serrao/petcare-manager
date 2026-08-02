from models.pessoa import Pessoa


class Veterinario(Pessoa):
    """
    Representa um veterinário da clínica.
    """

    def __init__(
        self,
        nome: str,
        crmv: str,
        especialidade: str,
        telefone: str,
        email: str,
        id_veterinario: int | None = None,
    ) -> None:
        super().__init__(nome, telefone, email, id_veterinario)

        self.crmv = crmv
        self.especialidade = especialidade

    def exibir_dados(self) -> str:
        return (
            f"Veterinário: {self.nome}\n"
            f"CRMV: {self.crmv}\n"
            f"Especialidade: {self.especialidade}\n"
            f"Telefone: {self.telefone}\n"
            f"E-mail: {self.email}"
        )