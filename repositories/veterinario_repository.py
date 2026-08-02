import psycopg2
from psycopg2.extensions import connection

from models.veterinario import Veterinario


class VeterinarioRepository:
    """Responsável pelas operações de banco da entidade Veterinario."""

    def __init__(self, database_connection: connection) -> None:
        self.connection = database_connection

    def cadastrar(self, veterinario: Veterinario) -> Veterinario:
        query = """
            INSERT INTO veterinarios (
                nome,
                crmv,
                especialidade,
                telefone,
                email
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        veterinario.nome,
                        veterinario.crmv,
                        veterinario.especialidade,
                        veterinario.telefone,
                        veterinario.email,
                    ),
                )
                resultado = cursor.fetchone()

            self.connection.commit()

            if resultado is None:
                raise RuntimeError(
                    "O banco não retornou o ID do veterinário."
                )

            veterinario.id = resultado[0]
            return veterinario

        except psycopg2.errors.UniqueViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "Já existe um veterinário com esse CRMV ou e-mail."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível cadastrar o veterinário: {erro}"
            ) from erro

    def listar(self) -> list[Veterinario]:
        query = """
            SELECT id, nome, crmv, especialidade, telefone, email
            FROM veterinarios
            ORDER BY nome;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                registros = cursor.fetchall()

            return [
                Veterinario(
                    id_veterinario=registro[0],
                    nome=registro[1],
                    crmv=registro[2],
                    especialidade=registro[3],
                    telefone=registro[4],
                    email=registro[5],
                )
                for registro in registros
            ]

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível listar os veterinários: {erro}"
            ) from erro

    def buscar_por_id(
        self,
        veterinario_id: int,
    ) -> Veterinario | None:
        query = """
            SELECT id, nome, crmv, especialidade, telefone, email
            FROM veterinarios
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (veterinario_id,))
                registro = cursor.fetchone()

            if registro is None:
                return None

            return Veterinario(
                id_veterinario=registro[0],
                nome=registro[1],
                crmv=registro[2],
                especialidade=registro[3],
                telefone=registro[4],
                email=registro[5],
            )

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível buscar o veterinário: {erro}"
            ) from erro

    def atualizar(self, veterinario: Veterinario) -> bool:
        if veterinario.id is None:
            raise ValueError(
                "O veterinário precisa ter um ID para ser atualizado."
            )

        query = """
            UPDATE veterinarios
            SET nome = %s,
                crmv = %s,
                especialidade = %s,
                telefone = %s,
                email = %s
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        veterinario.nome,
                        veterinario.crmv,
                        veterinario.especialidade,
                        veterinario.telefone,
                        veterinario.email,
                        veterinario.id,
                    ),
                )
                atualizado = cursor.rowcount > 0

            self.connection.commit()
            return atualizado

        except psycopg2.errors.UniqueViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "Já existe um veterinário com esse CRMV ou e-mail."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível atualizar o veterinário: {erro}"
            ) from erro

    def excluir(self, veterinario_id: int) -> bool:
        query = """
            DELETE FROM veterinarios
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (veterinario_id,))
                excluido = cursor.rowcount > 0

            self.connection.commit()
            return excluido

        except psycopg2.errors.ForeignKeyViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "Não é possível excluir um veterinário com consultas."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível excluir o veterinário: {erro}"
            ) from erro