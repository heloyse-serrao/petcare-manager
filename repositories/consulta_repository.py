import psycopg2
from psycopg2.extensions import connection

from models.consulta import Consulta


class ConsultaRepository:
    """Responsável pelas operações de banco da entidade Consulta."""

    def __init__(self, database_connection: connection) -> None:
        self.connection = database_connection

    def cadastrar(self, consulta: Consulta) -> Consulta:
        query = """
            INSERT INTO consultas (
                data,
                horario,
                motivo,
                status,
                animal_id,
                veterinario_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        consulta.data,
                        consulta.horario,
                        consulta.motivo,
                        consulta.status,
                        consulta.animal_id,
                        consulta.veterinario_id,
                    ),
                )

                resultado = cursor.fetchone()

            self.connection.commit()

            if resultado is None:
                raise RuntimeError(
                    "O banco não retornou o ID da consulta."
                )

            consulta.id = resultado[0]
            return consulta

        except psycopg2.errors.UniqueViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "O veterinário já possui uma consulta nesse horário."
            ) from erro

        except psycopg2.errors.ForeignKeyViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "O animal ou veterinário informado não existe."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível cadastrar a consulta: {erro}"
            ) from erro

    def listar(self) -> list[Consulta]:
        query = """
            SELECT
                id,
                data,
                horario,
                motivo,
                status,
                animal_id,
                veterinario_id
            FROM consultas
            ORDER BY data, horario;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                registros = cursor.fetchall()

            return [
                self._converter_registro(registro)
                for registro in registros
            ]

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível listar as consultas: {erro}"
            ) from erro

    def buscar_por_id(
        self,
        consulta_id: int,
    ) -> Consulta | None:
        query = """
            SELECT
                id,
                data,
                horario,
                motivo,
                status,
                animal_id,
                veterinario_id
            FROM consultas
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (consulta_id,))
                registro = cursor.fetchone()

            if registro is None:
                return None

            return self._converter_registro(registro)

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível buscar a consulta: {erro}"
            ) from erro

    def existe_conflito(
        self,
        data_consulta,
        horario,
        veterinario_id: int,
        consulta_id_ignorada: int | None = None,
    ) -> bool:
        if consulta_id_ignorada is None:
            query = """
                SELECT 1
                FROM consultas
                WHERE data = %s
                  AND horario = %s
                  AND veterinario_id = %s
                  AND status <> 'CANCELADA'
                LIMIT 1;
            """

            parametros = (
                data_consulta,
                horario,
                veterinario_id,
            )

        else:
            query = """
                SELECT 1
                FROM consultas
                WHERE data = %s
                  AND horario = %s
                  AND veterinario_id = %s
                  AND status <> 'CANCELADA'
                  AND id <> %s
                LIMIT 1;
            """

            parametros = (
                data_consulta,
                horario,
                veterinario_id,
                consulta_id_ignorada,
            )

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, parametros)
                return cursor.fetchone() is not None

        except psycopg2.Error as erro:
            raise RuntimeError(
                f"Não foi possível verificar o horário: {erro}"
            ) from erro

    def atualizar(self, consulta: Consulta) -> bool:
        if consulta.id is None:
            raise ValueError(
                "A consulta precisa ter um ID para ser atualizada."
            )

        query = """
            UPDATE consultas
            SET data = %s,
                horario = %s,
                motivo = %s,
                status = %s,
                animal_id = %s,
                veterinario_id = %s
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        consulta.data,
                        consulta.horario,
                        consulta.motivo,
                        consulta.status,
                        consulta.animal_id,
                        consulta.veterinario_id,
                        consulta.id,
                    ),
                )

                atualizado = cursor.rowcount > 0

            self.connection.commit()
            return atualizado

        except psycopg2.errors.UniqueViolation as erro:
            self.connection.rollback()
            raise RuntimeError(
                "O veterinário já possui uma consulta nesse horário."
            ) from erro

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível atualizar a consulta: {erro}"
            ) from erro

    def excluir(self, consulta_id: int) -> bool:
        query = """
            DELETE FROM consultas
            WHERE id = %s;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (consulta_id,))
                excluido = cursor.rowcount > 0

            self.connection.commit()
            return excluido

        except psycopg2.Error as erro:
            self.connection.rollback()
            raise RuntimeError(
                f"Não foi possível excluir a consulta: {erro}"
            ) from erro

    @staticmethod
    def _converter_registro(registro) -> Consulta:
        return Consulta(
            id_consulta=registro[0],
            data=registro[1],
            horario=registro[2],
            motivo=registro[3],
            status=registro[4],
            animal_id=registro[5],
            veterinario_id=registro[6],
        )