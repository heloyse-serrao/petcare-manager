import psycopg2
from psycopg2.extensions import connection

from models.tutor import Tutor


class TutorRepository:
    """Responsável pelas operações de banco da entidade Tutor."""

    def __init__(self, database_connection: connection) -> None:
        self.connection = database_connection

    def cadastrar(self, tutor: Tutor) -> Tutor:
        query = """
            INSERT INTO tutores (nome, cpf, telefone, email)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        tutor.nome,
                        tutor.cpf,
                        tutor.telefone,
                        tutor.email,
                    ),
                )

                resultado = cursor.fetchone()

            self.connection.commit()

            if resultado is None:
                raise RuntimeError("O banco não retornou o ID do tutor.")

            tutor.id = resultado[0]
            return tutor
        except psycopg2.errors.UniqueViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "Já existe um tutor cadastrado com esse CPF ou e-mail."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível cadastrar o tutor: {erro}"
            ) from erro
        

    def listar(self) -> list[Tutor]:
        query = """
            SELECT id, nome, cpf, telefone, email
            FROM tutores
            ORDER BY nome;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                registros = cursor.fetchall()

            return [
                Tutor(
                    id_tutor=registro[0],
                    nome=registro[1],
                    cpf=registro[2],
                    telefone=registro[3],
                    email=registro[4],
                )
                for registro in registros
            ]

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível listar os tutores: {erro}"
            ) from erro

    def buscar_por_id(self, tutor_id: int) -> Tutor | None:
        query = """
            SELECT id, nome, cpf, telefone, email
            FROM tutores
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (tutor_id,))
                registro = cursor.fetchone()

            if registro is None:
                return None

            return Tutor(
                id_tutor=registro[0],
                nome=registro[1],
                cpf=registro[2],
                telefone=registro[3],
                email=registro[4],
            )

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível buscar o tutor: {erro}"
            ) from erro

    def atualizar(self, tutor: Tutor) -> bool:
        if tutor.id is None:
            raise ValueError("O tutor precisa ter um ID para ser atualizado.")

        query = """
            UPDATE tutores
            SET nome = %s,
                cpf = %s,
                telefone = %s,
                email = %s
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        tutor.nome,
                        tutor.cpf,
                        tutor.telefone,
                        tutor.email,
                        tutor.id,
                    ),
                )

                atualizado = cursor.rowcount > 0

            self.connection.commit()
            return atualizado

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível atualizar o tutor: {erro}"
            ) from erro

    def excluir(self, tutor_id: int) -> bool:
        query = """
            DELETE FROM tutores
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (tutor_id,))
                excluido = cursor.rowcount > 0

            self.connection.commit()
            return excluido

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível excluir o tutor: {erro}"
            ) from erro