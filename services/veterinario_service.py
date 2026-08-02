from models.veterinario import Veterinario
from repositories.veterinario_repository import VeterinarioRepository


class VeterinarioService:
    """Aplica regras de negócio relacionadas aos veterinários."""

    def __init__(
        self,
        veterinario_repository: VeterinarioRepository,
    ) -> None:
        self.veterinario_repository = veterinario_repository

    def cadastrar(
        self,
        nome: str,
        crmv: str,
        especialidade: str,
        telefone: str,
        email: str,
    ) -> Veterinario:
        nome = nome.strip()
        crmv = crmv.strip().upper()
        especialidade = especialidade.strip()
        telefone = telefone.strip()
        email = email.strip().lower()

        self._validar_dados(
            nome,
            crmv,
            especialidade,
            email,
        )

        veterinario = Veterinario(
            nome=nome,
            crmv=crmv,
            especialidade=especialidade,
            telefone=telefone,
            email=email,
        )

        return self.veterinario_repository.cadastrar(veterinario)

    def listar(self) -> list[Veterinario]:
        return self.veterinario_repository.listar()

    def buscar_por_id(self, veterinario_id: int) -> Veterinario:
        if veterinario_id <= 0:
            raise ValueError(
                "O ID do veterinário deve ser maior que zero."
            )

        veterinario = self.veterinario_repository.buscar_por_id(
            veterinario_id
        )

        if veterinario is None:
            raise ValueError("Veterinário não encontrado.")

        return veterinario

    def atualizar(
        self,
        veterinario_id: int,
        nome: str,
        crmv: str,
        especialidade: str,
        telefone: str,
        email: str,
    ) -> Veterinario:
        veterinario = self.buscar_por_id(veterinario_id)

        nome = nome.strip()
        crmv = crmv.strip().upper()
        especialidade = especialidade.strip()
        telefone = telefone.strip()
        email = email.strip().lower()

        self._validar_dados(
            nome,
            crmv,
            especialidade,
            email,
        )

        veterinario.nome = nome
        veterinario.crmv = crmv
        veterinario.especialidade = especialidade
        veterinario.telefone = telefone
        veterinario.email = email

        atualizado = self.veterinario_repository.atualizar(
            veterinario
        )

        if not atualizado:
            raise RuntimeError(
                "Não foi possível atualizar o veterinário."
            )

        return veterinario

    def excluir(self, veterinario_id: int) -> None:
        self.buscar_por_id(veterinario_id)

        excluido = self.veterinario_repository.excluir(
            veterinario_id
        )

        if not excluido:
            raise RuntimeError(
                "Não foi possível excluir o veterinário."
            )

    @staticmethod
    def _validar_dados(
        nome: str,
        crmv: str,
        especialidade: str,
        email: str,
    ) -> None:
        if len(nome) < 3:
            raise ValueError(
                "O nome deve possuir pelo menos 3 caracteres."
            )

        if not crmv:
            raise ValueError("O CRMV é obrigatório.")

        if len(crmv) < 4:
            raise ValueError("Informe um CRMV válido.")

        if not especialidade:
            raise ValueError("A especialidade é obrigatória.")

        if "@" not in email or "." not in email:
            raise ValueError("Informe um e-mail válido.")