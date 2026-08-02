class Animal:
    """Representa um animal atendido pela clínica."""

    def __init__(
        self,
        nome: str,
        especie: str,
        raca: str,
        idade: int,
        peso: float,
        tutor_id: int,
        id_animal: int | None = None,
    ) -> None:
        self.id = id_animal
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.peso = peso
        self.tutor_id = tutor_id

    @property
    def peso(self) -> float:
        return self.__peso

    @peso.setter
    def peso(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError(
                "O peso do animal deve ser maior que zero."
            )

        self.__peso = valor

    def __str__(self) -> str:
        return (
            f"Animal: {self.nome}\n"
            f"Espécie: {self.especie}\n"
            f"Raça: {self.raca}\n"
            f"Idade: {self.idade} anos\n"
            f"Peso: {self.peso:.2f} kg"
        )