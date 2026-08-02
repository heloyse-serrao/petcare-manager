CREATE TABLE tutores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE veterinarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crmv VARCHAR(30) NOT NULL UNIQUE,
    especialidade VARCHAR(100),
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE animais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(100),
    idade INTEGER CHECK (idade >= 0),
    peso NUMERIC(6,2) CHECK (peso > 0),
    tutor_id INTEGER NOT NULL,

    CONSTRAINT fk_animal_tutor
        FOREIGN KEY (tutor_id)
        REFERENCES tutores(id)
        ON DELETE RESTRICT
);

CREATE TABLE consultas (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'AGENDADA',
    animal_id INTEGER NOT NULL,
    veterinario_id INTEGER NOT NULL,

    CREATE UNIQUE INDEX consulta_horario_ativo_unico
    ON consultas (data, horario, veterinario_id)
    WHERE status <> 'CANCELADA';

    CONSTRAINT chk_status_consulta
        CHECK (status IN ('AGENDADA', 'CONCLUÍDA', 'CANCELADA')),

    CONSTRAINT fk_consulta_animal
        FOREIGN KEY (animal_id)
        REFERENCES animais(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_consulta_veterinario
        FOREIGN KEY (veterinario_id)
        REFERENCES veterinarios(id)
        ON DELETE RESTRICT,

);

CREATE UNIQUE INDEX consulta_horario_ativo_unico
ON consultas (data, horario, veterinario_id)
WHERE status <> 'CANCELADA';