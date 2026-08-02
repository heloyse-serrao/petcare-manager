from datetime import date, time


class Consulta:
    """
    Representa uma consulta veterinária.
    """

    STATUS_VALIDOS = {
        "AGENDADA",
        "CONCLUÍDA",
        "CANCELADA"
    }

    def __init__(
        self,
        data: date,
        horario: time,
        motivo: str,
        animal_id: int,
        veterinario_id: int,
        status: str = "AGENDADA",
        id_consulta: int | None = None,
    ) -> None:

        self.id = id_consulta
        self.data = data
        self.horario = horario
        self.motivo = motivo

        self.status = status

        self.animal_id = animal_id
        self.veterinario_id = veterinario_id

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, valor: str) -> None:

        valor = valor.upper()

        if valor not in self.STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido. Utilize: {', '.join(self.STATUS_VALIDOS)}"
            )

        self.__status = valor

    def __str__(self) -> str:
        return (
            f"Consulta\n"
            f"Data: {self.data}\n"
            f"Horário: {self.horario}\n"
            f"Motivo: {self.motivo}\n"
            f"Status: {self.status}"
        )