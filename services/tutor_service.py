from models.tutor import Tutor
from repositories.tutor_repository import TutorRepository
import re

class TutorService:
    """Aplica as regras de negócio relacionadas aos tutores."""

    def __init__(self, tutor_repository: TutorRepository) -> None:
        self.tutor_repository = tutor_repository

    def cadastrar(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
    ) -> Tutor:
        nome = nome.strip()
        cpf = cpf.strip()
        telefone = telefone.strip()
        email = email.strip().lower()

        self._validar_dados(nome, cpf, email)

        tutor = Tutor(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
        )

        return self.tutor_repository.cadastrar(tutor)

    def listar(self) -> list[Tutor]:
        return self.tutor_repository.listar()

    def buscar_por_id(self, tutor_id: int) -> Tutor:
        if tutor_id <= 0:
            raise ValueError("O ID do tutor deve ser maior que zero.")

        tutor = self.tutor_repository.buscar_por_id(tutor_id)

        if tutor is None:
            raise ValueError("Tutor não encontrado.")

        return tutor

    def atualizar(
        self,
        tutor_id: int,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
    ) -> Tutor:
        tutor = self.buscar_por_id(tutor_id)

        nome = nome.strip()
        cpf = cpf.strip()
        telefone = telefone.strip()
        email = email.strip().lower()

        self._validar_dados(nome, cpf, email)

        tutor.nome = nome
        tutor.cpf = cpf
        tutor.telefone = telefone
        tutor.email = email

        atualizado = self.tutor_repository.atualizar(tutor)

        if not atualizado:
            raise RuntimeError("Não foi possível atualizar o tutor.")

        return tutor

    def excluir(self, tutor_id: int) -> None:
        self.buscar_por_id(tutor_id)

        excluido = self.tutor_repository.excluir(tutor_id)

        if not excluido:
            raise RuntimeError("Não foi possível excluir o tutor.")

    @staticmethod
    def _validar_dados(nome: str, cpf: str, email: str) -> None:
        if not nome:
            raise ValueError("O nome do tutor é obrigatório.")

        if len(nome) < 3:
            raise ValueError("O nome deve possuir pelo menos 3 caracteres.")

        if not cpf:
            raise ValueError("O CPF do tutor é obrigatório.")

        padrao_cpf = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"

        if not re.fullmatch(padrao_cpf, cpf):
            raise ValueError("Informe o CPF no formato 000.000.000-00.")

        if not email:
            raise ValueError("O e-mail do tutor é obrigatório.")

        if "@" not in email or "." not in email:
            raise ValueError("Informe um e-mail válido.")