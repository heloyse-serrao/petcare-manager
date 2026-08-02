from datetime import datetime

from services.animal_service import AnimalService
from services.consulta_service import ConsultaService
from services.tutor_service import TutorService
from services.veterinario_service import VeterinarioService


class Menu:
    """Interface de terminal do PetCare Manager."""

    def __init__(
        self,
        tutor_service: TutorService,
        veterinario_service: VeterinarioService,
        animal_service: AnimalService,
        consulta_service: ConsultaService,
    ) -> None:
        self.tutor_service = tutor_service
        self.veterinario_service = veterinario_service
        self.animal_service = animal_service
        self.consulta_service = consulta_service

    def executar(self) -> None:
        while True:
            self._mostrar_menu_principal()
            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._menu_tutores()
                elif opcao == "2":
                    self._menu_veterinarios()
                elif opcao == "3":
                    self._menu_animais()
                elif opcao == "4":
                    self._menu_consultas()
                elif opcao == "0":
                    print("\nEncerrando o PetCare Manager...")
                    break
                else:
                    print("\nOpção inválida.")

            except (ValueError, RuntimeError) as erro:
                print(f"\nErro: {erro}")

    @staticmethod
    def _mostrar_menu_principal() -> None:
        print(
            "\n====================================\n"
            "         PETCARE MANAGER\n"
            "====================================\n"
            "1 - Gerenciar tutores\n"
            "2 - Gerenciar veterinários\n"
            "3 - Gerenciar animais\n"
            "4 - Gerenciar consultas\n"
            "0 - Sair\n"
            "===================================="
        )

    # ========================= TUTORES =========================

    def _menu_tutores(self) -> None:
        while True:
            print(
                "\n====================================\n"
                "        GERENCIAR TUTORES\n"
                "====================================\n"
                "1 - Cadastrar tutor\n"
                "2 - Listar tutores\n"
                "3 - Buscar tutor por ID\n"
                "4 - Atualizar tutor\n"
                "5 - Excluir tutor\n"
                "0 - Voltar\n"
                "===================================="
            )

            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._cadastrar_tutor()
                elif opcao == "2":
                    self._listar_tutores()
                elif opcao == "3":
                    self._buscar_tutor()
                elif opcao == "4":
                    self._atualizar_tutor()
                elif opcao == "5":
                    self._excluir_tutor()
                elif opcao == "0":
                    break
                else:
                    print("\nOpção inválida.")

            except (ValueError, RuntimeError) as erro:
                print(f"\nErro: {erro}")

    def _cadastrar_tutor(self) -> None:
        print("\n--- Cadastro de tutor ---")

        tutor = self.tutor_service.cadastrar(
            nome=input("Nome: "),
            cpf=input("CPF (000.000.000-00): "),
            telefone=input("Telefone: "),
            email=input("E-mail: "),
        )

        print(f"\nTutor cadastrado. ID: {tutor.id}")

    def _listar_tutores(self) -> None:
        tutores = self.tutor_service.listar()

        if not tutores:
            print("\nNenhum tutor cadastrado.")
            return

        for tutor in tutores:
            print("-" * 40)
            print(f"ID: {tutor.id}")
            print(tutor)

    def _buscar_tutor(self) -> None:
        tutor = self.tutor_service.buscar_por_id(
            self._ler_id("ID do tutor: ")
        )

        print(f"\nID: {tutor.id}")
        print(tutor)

    def _atualizar_tutor(self) -> None:
        tutor_id = self._ler_id("ID do tutor: ")
        atual = self.tutor_service.buscar_por_id(tutor_id)

        print("\nPressione Enter para manter o valor atual.")

        nome = input(f"Nome [{atual.nome}]: ").strip()
        cpf = input(f"CPF [{atual.cpf}]: ").strip()
        telefone = input(
            f"Telefone [{atual.telefone}]: "
        ).strip()
        email = input(f"E-mail [{atual.email}]: ").strip()

        tutor = self.tutor_service.atualizar(
            tutor_id=tutor_id,
            nome=nome or atual.nome,
            cpf=cpf or atual.cpf,
            telefone=telefone or atual.telefone,
            email=email or atual.email,
        )

        print("\nTutor atualizado.")
        print(tutor)

    def _excluir_tutor(self) -> None:
        tutor_id = self._ler_id("ID do tutor: ")
        tutor = self.tutor_service.buscar_por_id(tutor_id)

        print(tutor)

        if self._confirmar_exclusao():
            self.tutor_service.excluir(tutor_id)
            print("\nTutor excluído.")

    # ====================== VETERINÁRIOS ======================

    def _menu_veterinarios(self) -> None:
        while True:
            print(
                "\n====================================\n"
                "      GERENCIAR VETERINÁRIOS\n"
                "====================================\n"
                "1 - Cadastrar veterinário\n"
                "2 - Listar veterinários\n"
                "3 - Buscar veterinário por ID\n"
                "4 - Atualizar veterinário\n"
                "5 - Excluir veterinário\n"
                "0 - Voltar\n"
                "===================================="
            )

            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._cadastrar_veterinario()
                elif opcao == "2":
                    self._listar_veterinarios()
                elif opcao == "3":
                    self._buscar_veterinario()
                elif opcao == "4":
                    self._atualizar_veterinario()
                elif opcao == "5":
                    self._excluir_veterinario()
                elif opcao == "0":
                    break
                else:
                    print("\nOpção inválida.")

            except (ValueError, RuntimeError) as erro:
                print(f"\nErro: {erro}")

    def _cadastrar_veterinario(self) -> None:
        veterinario = self.veterinario_service.cadastrar(
            nome=input("Nome: "),
            crmv=input("CRMV: "),
            especialidade=input("Especialidade: "),
            telefone=input("Telefone: "),
            email=input("E-mail: "),
        )

        print(
            f"\nVeterinário cadastrado. ID: {veterinario.id}"
        )

    def _listar_veterinarios(self) -> None:
        veterinarios = self.veterinario_service.listar()

        if not veterinarios:
            print("\nNenhum veterinário cadastrado.")
            return

        for veterinario in veterinarios:
            print("-" * 40)
            print(f"ID: {veterinario.id}")
            print(veterinario)

    def _buscar_veterinario(self) -> None:
        veterinario = (
            self.veterinario_service.buscar_por_id(
                self._ler_id("ID do veterinário: ")
            )
        )

        print(f"\nID: {veterinario.id}")
        print(veterinario)

    def _atualizar_veterinario(self) -> None:
        veterinario_id = self._ler_id(
            "ID do veterinário: "
        )

        atual = self.veterinario_service.buscar_por_id(
            veterinario_id
        )

        print("\nPressione Enter para manter o valor atual.")

        nome = input(f"Nome [{atual.nome}]: ").strip()
        crmv = input(f"CRMV [{atual.crmv}]: ").strip()
        especialidade = input(
            f"Especialidade [{atual.especialidade}]: "
        ).strip()
        telefone = input(
            f"Telefone [{atual.telefone}]: "
        ).strip()
        email = input(f"E-mail [{atual.email}]: ").strip()

        veterinario = self.veterinario_service.atualizar(
            veterinario_id=veterinario_id,
            nome=nome or atual.nome,
            crmv=crmv or atual.crmv,
            especialidade=especialidade or atual.especialidade,
            telefone=telefone or atual.telefone,
            email=email or atual.email,
        )

        print("\nVeterinário atualizado.")
        print(veterinario)

    def _excluir_veterinario(self) -> None:
        veterinario_id = self._ler_id(
            "ID do veterinário: "
        )

        veterinario = (
            self.veterinario_service.buscar_por_id(
                veterinario_id
            )
        )

        print(veterinario)

        if self._confirmar_exclusao():
            self.veterinario_service.excluir(
                veterinario_id
            )
            print("\nVeterinário excluído.")

    # ========================= ANIMAIS =========================

    def _menu_animais(self) -> None:
        while True:
            print(
                "\n====================================\n"
                "         GERENCIAR ANIMAIS\n"
                "====================================\n"
                "1 - Cadastrar animal\n"
                "2 - Listar animais\n"
                "3 - Buscar animal por ID\n"
                "4 - Listar animais por tutor\n"
                "5 - Atualizar animal\n"
                "6 - Excluir animal\n"
                "0 - Voltar\n"
                "===================================="
            )

            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._cadastrar_animal()
                elif opcao == "2":
                    self._listar_animais()
                elif opcao == "3":
                    self._buscar_animal()
                elif opcao == "4":
                    self._listar_animais_por_tutor()
                elif opcao == "5":
                    self._atualizar_animal()
                elif opcao == "6":
                    self._excluir_animal()
                elif opcao == "0":
                    break
                else:
                    print("\nOpção inválida.")

            except (ValueError, RuntimeError) as erro:
                print(f"\nErro: {erro}")

    def _cadastrar_animal(self) -> None:
        animal = self.animal_service.cadastrar(
            nome=input("Nome: "),
            especie=input("Espécie: "),
            raca=input("Raça: "),
            idade=self._ler_inteiro("Idade: "),
            peso=self._ler_float("Peso em kg: "),
            tutor_id=self._ler_id("ID do tutor: "),
        )

        print(f"\nAnimal cadastrado. ID: {animal.id}")

    def _listar_animais(self) -> None:
        animais = self.animal_service.listar()

        if not animais:
            print("\nNenhum animal cadastrado.")
            return

        for animal in animais:
            print("-" * 40)
            print(f"ID: {animal.id}")
            print(animal)
            print(f"ID do tutor: {animal.tutor_id}")

    def _buscar_animal(self) -> None:
        animal = self.animal_service.buscar_por_id(
            self._ler_id("ID do animal: ")
        )

        print(f"\nID: {animal.id}")
        print(animal)
        print(f"ID do tutor: {animal.tutor_id}")

    def _listar_animais_por_tutor(self) -> None:
        animais = self.animal_service.listar_por_tutor(
            self._ler_id("ID do tutor: ")
        )

        if not animais:
            print("\nEsse tutor não possui animais.")
            return

        for animal in animais:
            print("-" * 40)
            print(f"ID: {animal.id}")
            print(animal)

    def _atualizar_animal(self) -> None:
        animal_id = self._ler_id("ID do animal: ")
        atual = self.animal_service.buscar_por_id(animal_id)

        print("\nPressione Enter para manter o valor atual.")

        nome = input(f"Nome [{atual.nome}]: ").strip()
        especie = input(
            f"Espécie [{atual.especie}]: "
        ).strip()
        raca = input(f"Raça [{atual.raca}]: ").strip()
        idade_texto = input(
            f"Idade [{atual.idade}]: "
        ).strip()
        peso_texto = input(
            f"Peso [{atual.peso:.2f}]: "
        ).strip()
        tutor_texto = input(
            f"ID do tutor [{atual.tutor_id}]: "
        ).strip()

        animal = self.animal_service.atualizar(
            animal_id=animal_id,
            nome=nome or atual.nome,
            especie=especie or atual.especie,
            raca=raca or atual.raca,
            idade=(
                self._converter_inteiro(idade_texto)
                if idade_texto
                else atual.idade
            ),
            peso=(
                self._converter_float(peso_texto)
                if peso_texto
                else atual.peso
            ),
            tutor_id=(
                self._converter_inteiro(tutor_texto)
                if tutor_texto
                else atual.tutor_id
            ),
        )

        print("\nAnimal atualizado.")
        print(animal)

    def _excluir_animal(self) -> None:
        animal_id = self._ler_id("ID do animal: ")
        animal = self.animal_service.buscar_por_id(animal_id)

        print(animal)

        if self._confirmar_exclusao():
            self.animal_service.excluir(animal_id)
            print("\nAnimal excluído.")

    # ======================== CONSULTAS ========================

    def _menu_consultas(self) -> None:
        while True:
            print(
                "\n====================================\n"
                "        GERENCIAR CONSULTAS\n"
                "====================================\n"
                "1 - Agendar consulta\n"
                "2 - Listar consultas\n"
                "3 - Buscar consulta por ID\n"
                "4 - Atualizar consulta\n"
                "5 - Alterar status\n"
                "6 - Excluir consulta\n"
                "0 - Voltar\n"
                "===================================="
            )

            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._cadastrar_consulta()
                elif opcao == "2":
                    self._listar_consultas()
                elif opcao == "3":
                    self._buscar_consulta()
                elif opcao == "4":
                    self._atualizar_consulta()
                elif opcao == "5":
                    self._alterar_status_consulta()
                elif opcao == "6":
                    self._excluir_consulta()
                elif opcao == "0":
                    break
                else:
                    print("\nOpção inválida.")

            except (ValueError, RuntimeError) as erro:
                print(f"\nErro: {erro}")

    def _cadastrar_consulta(self) -> None:
        consulta = self.consulta_service.cadastrar(
            data_consulta=self._ler_data(
                "Data (DD/MM/AAAA): "
            ),
            horario=self._ler_horario(
                "Horário (HH:MM): "
            ),
            motivo=input("Motivo: "),
            animal_id=self._ler_id("ID do animal: "),
            veterinario_id=self._ler_id(
                "ID do veterinário: "
            ),
        )

        print(f"\nConsulta agendada. ID: {consulta.id}")

    def _listar_consultas(self) -> None:
        consultas = self.consulta_service.listar()

        if not consultas:
            print("\nNenhuma consulta cadastrada.")
            return

        for consulta in consultas:
            self._mostrar_consulta(consulta)

    def _buscar_consulta(self) -> None:
        consulta = self.consulta_service.buscar_por_id(
            self._ler_id("ID da consulta: ")
        )

        self._mostrar_consulta(consulta)

    def _atualizar_consulta(self) -> None:
        consulta_id = self._ler_id("ID da consulta: ")
        atual = self.consulta_service.buscar_por_id(
            consulta_id
        )

        print("\nPressione Enter para manter o valor atual.")

        data_texto = input(
            f"Data [{atual.data.strftime('%d/%m/%Y')}]: "
        ).strip()

        horario_texto = input(
            f"Horário [{atual.horario.strftime('%H:%M')}]: "
        ).strip()

        motivo = input(
            f"Motivo [{atual.motivo}]: "
        ).strip()

        status = input(
            f"Status [{atual.status}]: "
        ).strip()

        animal_texto = input(
            f"ID do animal [{atual.animal_id}]: "
        ).strip()

        veterinario_texto = input(
            f"ID do veterinário "
            f"[{atual.veterinario_id}]: "
        ).strip()

        consulta = self.consulta_service.atualizar(
            consulta_id=consulta_id,
            data_consulta=(
                self._converter_data(data_texto)
                if data_texto
                else atual.data
            ),
            horario=(
                self._converter_horario(horario_texto)
                if horario_texto
                else atual.horario
            ),
            motivo=motivo or atual.motivo,
            status=status or atual.status,
            animal_id=(
                self._converter_inteiro(animal_texto)
                if animal_texto
                else atual.animal_id
            ),
            veterinario_id=(
                self._converter_inteiro(
                    veterinario_texto
                )
                if veterinario_texto
                else atual.veterinario_id
            ),
        )

        print("\nConsulta atualizada.")
        self._mostrar_consulta(consulta)

    def _alterar_status_consulta(self) -> None:
        consulta_id = self._ler_id("ID da consulta: ")

        print(
            "\nStatus permitidos:"
            "\n- AGENDADA"
            "\n- CONCLUÍDA"
            "\n- CANCELADA"
        )

        novo_status = input("Novo status: ")

        consulta = self.consulta_service.alterar_status(
            consulta_id,
            novo_status,
        )

        print("\nStatus atualizado.")
        self._mostrar_consulta(consulta)

    def _excluir_consulta(self) -> None:
        consulta_id = self._ler_id("ID da consulta: ")
        consulta = self.consulta_service.buscar_por_id(
            consulta_id
        )

        self._mostrar_consulta(consulta)

        if self._confirmar_exclusao():
            self.consulta_service.excluir(consulta_id)
            print("\nConsulta excluída.")

    @staticmethod
    def _mostrar_consulta(consulta) -> None:
        print("-" * 40)
        print(f"ID: {consulta.id}")
        print(
            f"Data: {consulta.data.strftime('%d/%m/%Y')}"
        )
        print(
            f"Horário: {consulta.horario.strftime('%H:%M')}"
        )
        print(f"Motivo: {consulta.motivo}")
        print(f"Status: {consulta.status}")
        print(f"ID do animal: {consulta.animal_id}")
        print(
            f"ID do veterinário: "
            f"{consulta.veterinario_id}"
        )

    # ======================== UTILITÁRIOS ======================

    @staticmethod
    def _confirmar_exclusao() -> bool:
        confirmacao = input(
            "\nConfirma a exclusão? (s/n): "
        ).strip().lower()

        if confirmacao != "s":
            print("\nExclusão cancelada.")
            return False

        return True

    @classmethod
    def _ler_id(cls, mensagem: str) -> int:
        identificador = cls._ler_inteiro(mensagem)

        if identificador <= 0:
            raise ValueError(
                "O ID deve ser maior que zero."
            )

        return identificador

    @classmethod
    def _ler_inteiro(cls, mensagem: str) -> int:
        return cls._converter_inteiro(
            input(mensagem).strip()
        )

    @staticmethod
    def _converter_inteiro(valor: str) -> int:
        try:
            return int(valor)
        except ValueError as erro:
            raise ValueError(
                "Informe um número inteiro válido."
            ) from erro

    @classmethod
    def _ler_float(cls, mensagem: str) -> float:
        return cls._converter_float(
            input(mensagem).strip()
        )

    @staticmethod
    def _converter_float(valor: str) -> float:
        try:
            return float(valor.replace(",", "."))
        except ValueError as erro:
            raise ValueError(
                "Informe um número válido."
            ) from erro

    @classmethod
    def _ler_data(cls, mensagem: str):
        return cls._converter_data(
            input(mensagem).strip()
        )

    @staticmethod
    def _converter_data(valor: str):
        try:
            return datetime.strptime(
                valor,
                "%d/%m/%Y",
            ).date()
        except ValueError as erro:
            raise ValueError(
                "Informe a data no formato DD/MM/AAAA."
            ) from erro

    @classmethod
    def _ler_horario(cls, mensagem: str):
        return cls._converter_horario(
            input(mensagem).strip()
        )

    @staticmethod
    def _converter_horario(valor: str):
        try:
            return datetime.strptime(
                valor,
                "%H:%M",
            ).time()
        except ValueError as erro:
            raise ValueError(
                "Informe o horário no formato HH:MM."
            ) from erro