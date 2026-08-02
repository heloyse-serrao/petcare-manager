import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

load_dotenv()


class DatabaseConnection:
    """Gerencia a conexão da aplicação com o PostgreSQL."""

    def __init__(self) -> None:
        self.connection: connection | None = None

    def connect(self) -> connection:
        """Abre e retorna uma conexão com o banco de dados."""

        if self.connection is not None and not self.connection.closed:
            return self.connection

        required_variables = (
            "DB_HOST",
            "DB_PORT",
            "DB_NAME",
            "DB_USER",
            "DB_PASSWORD",
        )

        missing_variables = [
            variable
            for variable in required_variables
            if not os.getenv(variable)
        ]

        if missing_variables:
            raise RuntimeError(
                "Variáveis ausentes no arquivo .env: "
                + ", ".join(missing_variables)
            )

        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )

            return self.connection

        except psycopg2.Error as error:
            raise ConnectionError(
                f"Não foi possível conectar ao PostgreSQL: {error}"
            ) from error

    def disconnect(self) -> None:
        """Fecha a conexão, caso esteja aberta."""

        if self.connection is not None and not self.connection.closed:
            self.connection.close()

        self.connection = None