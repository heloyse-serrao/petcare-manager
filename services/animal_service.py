from models.animal import Animal
from repositories.animal_repository import AnimalRepository
from repositories.tutor_repository import TutorRepository


class AnimalService:
    """Aplica as regras de negócio relacionadas aos animais."""

    def __init__(
        self,
        animal_repository: AnimalRepository,
        tutor_repository: TutorRepository,
    ) -> None:
        self.animal_repository = animal_repository
        self.tutor_repository = tutor_repository

    def cadastrar(
        self,
        nome: str,
        especie: str,
        raca: str,
        idade: int,
        peso: float,
        tutor_id: int,
    ) -> Animal:
        nome = nome.strip()
        especie = especie.strip()
        raca = raca.strip()

        self._validar_dados(
            nome=nome,
            especie=especie,
            idade=idade,
            peso=peso,
            tutor_id=tutor_id,
        )

        self._validar_tutor(tutor_id)

        animal = Animal(
            nome=nome,
            especie=especie,
            raca=raca,
            idade=idade,
            peso=peso,
            tutor_id=tutor_id,
        )

        return self.animal_repository.cadastrar(animal)

    def listar(self) -> list[Animal]:
        return self.animal_repository.listar()

    def buscar_por_id(self, animal_id: int) -> Animal:
        if animal_id <= 0:
            raise ValueError(
                "O ID do animal deve ser maior que zero."
            )

        animal = self.animal_repository.buscar_por_id(animal_id)

        if animal is None:
            raise ValueError("Animal não encontrado.")

        return animal

    def listar_por_tutor(self, tutor_id: int) -> list[Animal]:
        self._validar_tutor(tutor_id)
        return self.animal_repository.listar_por_tutor(tutor_id)

    def atualizar(
        self,
        animal_id: int,
        nome: str,
        especie: str,
        raca: str,
        idade: int,
        peso: float,
        tutor_id: int,
    ) -> Animal:
        animal = self.buscar_por_id(animal_id)

        nome = nome.strip()
        especie = especie.strip()
        raca = raca.strip()

        self._validar_dados(
            nome=nome,
            especie=especie,
            idade=idade,
            peso=peso,
            tutor_id=tutor_id,
        )

        self._validar_tutor(tutor_id)

        animal.nome = nome
        animal.especie = especie
        animal.raca = raca
        animal.idade = idade
        animal.peso = peso
        animal.tutor_id = tutor_id

        atualizado = self.animal_repository.atualizar(animal)

        if not atualizado:
            raise RuntimeError(
                "Não foi possível atualizar o animal."
            )

        return animal

    def excluir(self, animal_id: int) -> None:
        self.buscar_por_id(animal_id)

        excluido = self.animal_repository.excluir(animal_id)

        if not excluido:
            raise RuntimeError(
                "Não foi possível excluir o animal."
            )

    def _validar_tutor(self, tutor_id: int) -> None:
        if tutor_id <= 0:
            raise ValueError(
                "O ID do tutor deve ser maior que zero."
            )

        tutor = self.tutor_repository.buscar_por_id(tutor_id)

        if tutor is None:
            raise ValueError(
                "O tutor informado não está cadastrado."
            )

    @staticmethod
    def _validar_dados(
        nome: str,
        especie: str,
        idade: int,
        peso: float,
        tutor_id: int,
    ) -> None:
        if len(nome) < 2:
            raise ValueError(
                "O nome do animal deve possuir pelo menos 2 caracteres."
            )

        if not especie:
            raise ValueError(
                "A espécie do animal é obrigatória."
            )

        if idade < 0:
            raise ValueError(
                "A idade do animal não pode ser negativa."
            )

        if peso <= 0:
            raise ValueError(
                "O peso do animal deve ser maior que zero."
            )

        if tutor_id <= 0:
            raise ValueError(
                "O ID do tutor deve ser maior que zero."
            )