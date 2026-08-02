from database.connection import DatabaseConnection
from repositories.animal_repository import AnimalRepository
from repositories.consulta_repository import ConsultaRepository
from repositories.tutor_repository import TutorRepository
from repositories.veterinario_repository import (
    VeterinarioRepository,
)
from services.animal_service import AnimalService
from services.consulta_service import ConsultaService
from services.tutor_service import TutorService
from services.veterinario_service import VeterinarioService
from ui.menu import Menu


def main() -> None:
    database = DatabaseConnection()

    try:
        connection = database.connect()

        tutor_repository = TutorRepository(connection)
        veterinario_repository = VeterinarioRepository(
            connection
        )
        animal_repository = AnimalRepository(connection)
        consulta_repository = ConsultaRepository(connection)

        tutor_service = TutorService(tutor_repository)

        veterinario_service = VeterinarioService(
            veterinario_repository
        )

        animal_service = AnimalService(
            animal_repository=animal_repository,
            tutor_repository=tutor_repository,
        )

        consulta_service = ConsultaService(
            consulta_repository=consulta_repository,
            animal_repository=animal_repository,
            veterinario_repository=veterinario_repository,
        )

        menu = Menu(
            tutor_service=tutor_service,
            veterinario_service=veterinario_service,
            animal_service=animal_service,
            consulta_service=consulta_service,
        )

        menu.executar()

    except (ConnectionError, RuntimeError) as erro:
        print(f"\nErro ao iniciar o sistema: {erro}")

    except KeyboardInterrupt:
        print("\nSistema encerrado pelo usuário.")

    finally:
        database.disconnect()


if __name__ == "__main__":
    main()