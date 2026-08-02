from datetime import date, time

from models.consulta import Consulta
from repositories.animal_repository import AnimalRepository
from repositories.consulta_repository import ConsultaRepository
from repositories.veterinario_repository import (
    VeterinarioRepository,
)


class ConsultaService:
    """Aplica as regras de negócio relacionadas às consultas."""

    def __init__(
        self,
        consulta_repository: ConsultaRepository,
        animal_repository: AnimalRepository,
        veterinario_repository: VeterinarioRepository,
    ) -> None:
        self.consulta_repository = consulta_repository
        self.animal_repository = animal_repository
        self.veterinario_repository = veterinario_repository

    def cadastrar(
        self,
        data_consulta: date,
        horario: time,
        motivo: str,
        animal_id: int,
        veterinario_id: int,
    ) -> Consulta:
        motivo = motivo.strip()

        self._validar_dados(
            data_consulta=data_consulta,
            motivo=motivo,
            animal_id=animal_id,
            veterinario_id=veterinario_id,
        )

        self._validar_relacionamentos(
            animal_id,
            veterinario_id,
        )

        if self.consulta_repository.existe_conflito(
            data_consulta=data_consulta,
            horario=horario,
            veterinario_id=veterinario_id,
        ):
            raise ValueError(
                "O veterinário já possui uma consulta nesse horário."
            )

        consulta = Consulta(
            data=data_consulta,
            horario=horario,
            motivo=motivo,
            animal_id=animal_id,
            veterinario_id=veterinario_id,
        )

        return self.consulta_repository.cadastrar(consulta)

    def listar(self) -> list[Consulta]:
        return self.consulta_repository.listar()

    def buscar_por_id(self, consulta_id: int) -> Consulta:
        if consulta_id <= 0:
            raise ValueError(
                "O ID da consulta deve ser maior que zero."
            )

        consulta = self.consulta_repository.buscar_por_id(
            consulta_id
        )

        if consulta is None:
            raise ValueError("Consulta não encontrada.")

        return consulta

    def atualizar(
        self,
        consulta_id: int,
        data_consulta: date,
        horario: time,
        motivo: str,
        status: str,
        animal_id: int,
        veterinario_id: int,
    ) -> Consulta:
        consulta = self.buscar_por_id(consulta_id)
        motivo = motivo.strip()
        status = status.strip().upper()

        self._validar_dados(
            data_consulta=data_consulta,
            motivo=motivo,
            animal_id=animal_id,
            veterinario_id=veterinario_id,
        )

        self._validar_relacionamentos(
            animal_id,
            veterinario_id,
        )

        if self.consulta_repository.existe_conflito(
            data_consulta=data_consulta,
            horario=horario,
            veterinario_id=veterinario_id,
            consulta_id_ignorada=consulta_id,
        ):
            raise ValueError(
                "O veterinário já possui uma consulta nesse horário."
            )

        consulta.data = data_consulta
        consulta.horario = horario
        consulta.motivo = motivo
        consulta.status = status
        consulta.animal_id = animal_id
        consulta.veterinario_id = veterinario_id

        atualizado = self.consulta_repository.atualizar(
            consulta
        )

        if not atualizado:
            raise RuntimeError(
                "Não foi possível atualizar a consulta."
            )

        return consulta

    def excluir(self, consulta_id: int) -> None:
        self.buscar_por_id(consulta_id)

        excluido = self.consulta_repository.excluir(
            consulta_id
        )

        if not excluido:
            raise RuntimeError(
                "Não foi possível excluir a consulta."
            )

    def alterar_status(
        self,
        consulta_id: int,
        novo_status: str,
    ) -> Consulta:
        consulta = self.buscar_por_id(consulta_id)
        consulta.status = novo_status

        atualizado = self.consulta_repository.atualizar(
            consulta
        )

        if not atualizado:
            raise RuntimeError(
                "Não foi possível alterar o status da consulta."
            )

        return consulta

    def _validar_relacionamentos(
        self,
        animal_id: int,
        veterinario_id: int,
    ) -> None:
        animal = self.animal_repository.buscar_por_id(animal_id)

        if animal is None:
            raise ValueError(
                "O animal informado não está cadastrado."
            )

        veterinario = (
            self.veterinario_repository.buscar_por_id(
                veterinario_id
            )
        )

        if veterinario is None:
            raise ValueError(
                "O veterinário informado não está cadastrado."
            )

    @staticmethod
    def _validar_dados(
        data_consulta: date,
        motivo: str,
        animal_id: int,
        veterinario_id: int,
    ) -> None:
        if data_consulta < date.today():
            raise ValueError(
                "Não é possível agendar uma consulta em data passada."
            )

        if len(motivo) < 3:
            raise ValueError(
                "O motivo deve possuir pelo menos 3 caracteres."
            )

        if animal_id <= 0:
            raise ValueError(
                "O ID do animal deve ser maior que zero."
            )

        if veterinario_id <= 0:
            raise ValueError(
                "O ID do veterinário deve ser maior que zero."
            )