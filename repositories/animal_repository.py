import psycopg2
from psycopg2.extensions import connection

from models.animal import Animal


class AnimalRepository:
    """Responsável pelas operações de banco da entidade Animal."""

    def __init__(self, database_connection: connection) -> None:
        self.connection = database_connection

    def cadastrar(self, animal: Animal) -> Animal:
        query = """
            INSERT INTO animais (
                nome,
                especie,
                raca,
                idade,
                peso,
                tutor_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        animal.nome,
                        animal.especie,
                        animal.raca,
                        animal.idade,
                        animal.peso,
                        animal.tutor_id,
                    ),
                )

                resultado = cursor.fetchone()

            self.connection.commit()

            if resultado is None:
                raise RuntimeError(
                    "O banco não retornou o ID do animal."
                )

            animal.id = resultado[0]
            return animal

        except psycopg2.errors.ForeignKeyViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "O tutor informado não existe."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível cadastrar o animal: {erro}"
            ) from erro

    def listar(self) -> list[Animal]:
        query = """
            SELECT id, nome, especie, raca, idade, peso, tutor_id
            FROM animais
            ORDER BY nome;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                registros = cursor.fetchall()

            return [
                Animal(
                    id_animal=registro[0],
                    nome=registro[1],
                    especie=registro[2],
                    raca=registro[3],
                    idade=registro[4],
                    peso=float(registro[5]),
                    tutor_id=registro[6],
                )
                for registro in registros
            ]

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível listar os animais: {erro}"
            ) from erro

    def buscar_por_id(self, animal_id: int) -> Animal | None:
        query = """
            SELECT id, nome, especie, raca, idade, peso, tutor_id
            FROM animais
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (animal_id,))
                registro = cursor.fetchone()

            if registro is None:
                return None

            return Animal(
                id_animal=registro[0],
                nome=registro[1],
                especie=registro[2],
                raca=registro[3],
                idade=registro[4],
                peso=float(registro[5]),
                tutor_id=registro[6],
            )

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível buscar o animal: {erro}"
            ) from erro

    def listar_por_tutor(self, tutor_id: int) -> list[Animal]:
        query = """
            SELECT id, nome, especie, raca, idade, peso, tutor_id
            FROM animais
            WHERE tutor_id = %s
            ORDER BY nome;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (tutor_id,))
                registros = cursor.fetchall()

            return [
                Animal(
                    id_animal=registro[0],
                    nome=registro[1],
                    especie=registro[2],
                    raca=registro[3],
                    idade=registro[4],
                    peso=float(registro[5]),
                    tutor_id=registro[6],
                )
                for registro in registros
            ]

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível listar os animais do tutor: {erro}"
            ) from erro

    def atualizar(self, animal: Animal) -> bool:
        if animal.id is None:
            raise ValueError(
                "O animal precisa ter um ID para ser atualizado."
            )

        query = """
            UPDATE animais
            SET nome = %s,
                especie = %s,
                raca = %s,
                idade = %s,
                peso = %s,
                tutor_id = %s
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        animal.nome,
                        animal.especie,
                        animal.raca,
                        animal.idade,
                        animal.peso,
                        animal.tutor_id,
                        animal.id,
                    ),
                )

                atualizado = cursor.rowcount > 0

            self.connection.commit()
            return atualizado

        except psycopg2.errors.ForeignKeyViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "O tutor informado não existe."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível atualizar o animal: {erro}"
            ) from erro

    def excluir(self, animal_id: int) -> bool:
        query = """
            DELETE FROM animais
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (animal_id,))
                excluido = cursor.rowcount > 0

            self.connection.commit()
            return excluido

        except psycopg2.errors.ForeignKeyViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "Não é possível excluir um animal que possui consultas."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível excluir o animal: {erro}"
            ) from erro