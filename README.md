# PetCare Manager 🐾

Sistema de gerenciamento de clínica veterinária desenvolvido em Python, aplicando conceitos de Programação Orientada a Objetos e integração com banco de dados PostgreSQL.

## Sobre o projeto

O PetCare Manager permite gerenciar tutores, animais, veterinários e consultas por meio de uma interface de terminal.

## Funcionalidades

### Tutores

- Cadastrar tutor
- Listar tutores
- Buscar tutor por ID
- Atualizar tutor
- Excluir tutor
- Impedir CPF ou e-mail duplicado

### Veterinários

- Cadastrar veterinário
- Listar veterinários
- Buscar veterinário por ID
- Atualizar veterinário
- Excluir veterinário
- Impedir CRMV ou e-mail duplicado

### Animais

- Cadastrar animal
- Listar animais
- Buscar animal por ID
- Listar animais por tutor
- Atualizar animal
- Excluir animal
- Validar a existência do tutor

### Consultas

- Agendar consulta
- Listar consultas
- Buscar consulta por ID
- Atualizar consulta
- Alterar status
- Excluir consulta
- Impedir conflitos de horário
- Impedir agendamentos em datas passadas

## Conceitos de POO aplicados

- Classes e objetos
- Encapsulamento
- Herança
- Abstração
- Polimorfismo
- Métodos especiais, como `__str__`
- Tratamento de exceções

### Hierarquia de classes

```text
Pessoa (classe abstrata)
├── Tutor
└── Veterinario

Animal
Consulta
```

O método `exibir_dados()` é definido como abstrato em `Pessoa` e implementado de maneira diferente por `Tutor` e `Veterinario`, demonstrando polimorfismo.

O atributo `peso` da classe `Animal` utiliza encapsulamento com `@property` e setter.

## Arquitetura

O projeto está organizado em camadas:

```text
Interface
    ↓
Services
    ↓
Repositories
    ↓
PostgreSQL
```

- `models/`: classes de domínio
- `repositories/`: operações de acesso ao banco
- `services/`: validações e regras de negócio
- `ui/`: interface de terminal
- `database/`: conexão e script SQL

## Estrutura do projeto

```text
petcare-manager/
├── database/
│   ├── connection.py
│   └── schema.sql
├── models/
│   ├── pessoa.py
│   ├── tutor.py
│   ├── veterinario.py
│   ├── animal.py
│   └── consulta.py
├── repositories/
│   ├── tutor_repository.py
│   ├── veterinario_repository.py
│   ├── animal_repository.py
│   └── consulta_repository.py
├── services/
│   ├── tutor_service.py
│   ├── veterinario_service.py
│   ├── animal_service.py
│   └── consulta_service.py
├── ui/
│   └── menu.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Banco de dados

O sistema utiliza quatro tabelas:

```text
tutores
    1
    │
    N
animais
    1
    │
    N
consultas
    N
    │
    1
veterinarios
```

## Desenvolvido por

Heloyse Heloá Serrão Viana

Curso: Engenharia de Software – UFAM (ICET)
