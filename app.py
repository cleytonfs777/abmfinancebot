import flet as ft
import pandas as pd
from db import criar_militar, ler_militares
from utils import POST_GRAD
from tabelas import table_comum, data_list, table_edit, data_list_edit


def main(page: ft.Page):
    # Input de planilha com dados excel
    file_picker = ft.FilePicker(on_result=lambda e: on_file_upload(e))
    page.overlay.append(file_picker)

    # Dimensionar tela
    page.window.width = 800
    page.window.height = 600

    def on_file_upload(e):
        if not e.files:
            return

        file_path = e.files[0].path
        try:
            df = pd.read_excel(file_path)
            # Validar o cabeçalho
            required_columns = ["Nº BM", "P/G", 'Nome', 'RG', 'CPF', 'Banco',
                                'CC', 'Agencia', 'PIS/PASEP', 'DOC SEI']
            if not all(col in df.columns for col in required_columns):
                page.add(ft.Text("Formato de planilha inválido"))
                return

            # Criar as linhas da tabela e a lista de dados
            rows = []
            for index, row in df.iterrows():
                data = row[required_columns].tolist()
                data_list.append(data)
                cells = [ft.DataCell(ft.Text(str(value), color=ft.colors.BLUE_900))
                         for value in data]
                delete_button = ft.ElevatedButton(
                    text="X",
                    on_click=lambda e, idx=index - 1: delete_row(idx)
                )
                rows.append(ft.DataRow(
                    cells=cells + [ft.DataCell(delete_button)]))

            table_comum.rows = rows
            page.update()
        except Exception as e:
            page.add(ft.Text(f"Erro ao carregar o arquivo: {str(e)}"))

    def delete_row(index):
        # Remover a linha da tabela e da lista de dados
        del table_comum.rows[index]
        del data_list[index]
        page.update()

    def gerar_empenho(e):
        for item in data_list:
            print(item)
            page.add(ft.Text(str(item)))

    def campo_field(nome_main="preencha", max_l=0, apenas_numeros=False):
        def validar_numeros(e):
            if not e.control.value.isdigit():
                e.control.value = ''.join(filter(str.isdigit, e.control.value))
            e.page.update()

        if apenas_numeros:
            return ft.TextField(
                label=nome_main,
                width=300,
                text_align=ft.TextAlign.CENTER,
                label_style={"color": "#081d33", "font_size": 13, "font_weight": "bold"},
                border_radius=6,
                color="#081d33",
                border_color="#081d33",
                text_size=13,
                max_length=max_l if max_l > 0 else None,
                content_padding=10,
                on_change=validar_numeros
            )
        else:
            return ft.TextField(
                label=nome_main,
                width=300,
                text_align=ft.TextAlign.CENTER,
                label_style={"color": "#081d33", "font_size": 13, "font_weight": "bold"},
                border_radius=6,
                color="#081d33",
                border_color="#081d33",
                text_size=13,
                max_length=max_l if max_l > 0 else None,
                content_padding=10
            )

    def drop_field(options: list[str], label: str = ""):
        return ft.Dropdown(
                alignment=ft.alignment.center,
                padding=10,
                label=label,
                text_style={"color": "#081d33", "font_size": 13, "font_weight": "bold"},
                label_style={"color": "#1664B8", "font_size": 13, "font_weight": "bold"},
                options=[ft.dropdown.Option(
                item, alignment=ft.alignment.center) for item in options],
                width=300,
                border_radius=6,
                color="#081d33",
                text_size=13,
                content_padding=0,
                bgcolor="#ebebeb",
            )

    def change_color(e):
        if e.control.text == "CADASTRO":
            # Campos do formulário
            numero_f = campo_field("Número", 7, apenas_numeros=True)  # Apenas números permitidos
            pg_f =  drop_field(POST_GRAD,"Posto/Grad")
            nome_f = campo_field("Nome")
            rg_f = campo_field("RG")
            cpf_f = campo_field("CPF")
            banco_f = campo_field("Banco")
            cc_f = campo_field("Conta Corrente")
            ag_f = campo_field("Agência")
            type_van_f = drop_field(["QQ", "ADE"],"Tipo de Vantagem")               
            vant_f = campo_field("Vantagem", 2, apenas_numeros=True)  # Apenas números permitidos


            # Função para validação de campos
            def validar_campos():
                erros = []
                if not numero_f.value:
                    erros.append("O campo 'Número' é obrigatório.")
                if not pg_f.value:
                    erros.append("O campo 'Graduação/Posto' é obrigatório.")
                if not nome_f.value:
                    erros.append("O campo 'Nome' é obrigatório.")
                if not rg_f.value:
                    erros.append("O campo 'RG' é obrigatório.")
                if not cpf_f.value:
                    erros.append("O campo 'CPF' é obrigatório.")
                if not banco_f.value:
                    erros.append("O campo 'Banco' é obrigatório.")
                if not cc_f.value:
                    erros.append("O campo 'Conta Corrente' é obrigatório.")
                if not ag_f.value:
                    erros.append("O campo 'Agência' é obrigatório.")
                if not type_van_f.value:
                    erros.append("O campo 'Tipo de Vantagem' é obrigatório.")
                try:
                    int(vant_f.value)
                except ValueError:
                    erros.append(
                        "O campo 'Vantagem' deve ser um número válido.")
                return erros

            # Botão de cadastro
            cadast_button = ft.ElevatedButton(
                text="Cadastrar",
                width=page.width*0.1,
                on_click=lambda e: processar_cadastro()
            )

            # Função para limpar os campos
            def limpar_campos():
                numero_f.value = ""
                pg_f.value = ""
                nome_f.value = ""
                rg_f.value = ""
                cpf_f.value = ""
                banco_f.value = ""
                cc_f.value = ""
                ag_f.value = ""
                type_van_f.value = ""
                vant_f.value = ""
                page.update()

            # Botão de limpar
            limp_button = ft.ElevatedButton(
                text="Limpar",
                width=page.width*0.1,
                on_click=lambda e: limpar_campos()
            )

            # Função para processar o cadastro
            def processar_cadastro():
                erros = validar_campos()
                if erros:
                    popup_erros = ft.AlertDialog(
                        title=ft.Text("Erro de Validação"),
                        content=ft.Column(
                            controls=[ft.Text(erro) for erro in erros],
                            tight=True
                        ),
                        actions=[ft.TextButton(
                            "OK", on_click=lambda e: fechar_popup(popup_erros))],
                        modal=True
                    )
                    page.overlay.append(popup_erros)
                    popup_erros.open = True
                    page.update()
                else:
                    militares_existentes = ler_militares(
                        "numero", numero_f.value)
                    if militares_existentes:
                        popup_existe = ft.AlertDialog(
                            title=ft.Text("Registro já existe"),
                            content=ft.Text(f"O registro com o número {
                                            numero_f.value} já está cadastrado."),
                            actions=[ft.TextButton(
                                "OK", on_click=lambda e: fechar_popup(popup_existe))],
                            modal=True
                        )
                        page.overlay.append(popup_existe)
                        popup_existe.open = True
                        page.update()
                    else:
                        criar_militar(
                            numero=numero_f.value,
                            gradpost=pg_f.value,
                            nome=nome_f.value,
                            rg=rg_f.value,
                            cpf=cpf_f.value,
                            banco=banco_f.value,
                            cc=cc_f.value,
                            agencia=ag_f.value,
                            type_vant=type_van_f.value,
                            vantagem=int(vant_f.value)
                        )
                        popup_sucesso = ft.AlertDialog(
                            title=ft.Text("Cadastro realizado"),
                            content=ft.Text(f"O registro com o número {
                                            numero_f.value} foi cadastrado com sucesso."),
                            actions=[ft.TextButton(
                                "OK", on_click=lambda e: fechar_popup(popup_sucesso))],
                            modal=True
                        )
                        page.overlay.append(popup_sucesso)
                        popup_sucesso.open = True
                        page.update()

            def fechar_popup(dialog):
                dialog.open = False
                page.update()

            body_container.content = ft.Container(
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE10,
                content=ft.Container(
                    bgcolor=ft.colors.WHITE,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(16),
                    border_radius=6,
                    content=ft.Column(
                        alignment=ft.alignment.center,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Text("Cadastro de Militares", color=ft.colors.BLUE_GREY,
                                        size=30, weight="bold", text_align=ft.TextAlign.CENTER),
                            ft.Divider(height=12, color="transparent"),
                            ft.Row(
                                controls=[numero_f, pg_f],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=6, color="transparent"),
                            ft.Row(
                                controls=[nome_f, rg_f],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=6, color="transparent"),
                            ft.Row(
                                controls=[cpf_f, banco_f],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=6, color="transparent"),
                            ft.Row(
                                controls=[cc_f, ag_f],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=6, color="transparent"),
                            ft.Row(
                                controls=[type_van_f, vant_f],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Divider(height=6, color="transparent"),
                            ft.Row(
                                controls=[cadast_button, limp_button],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                ),
            )

        elif e.control.text == "GESTÃO":
            body_container.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Edição e Exclusão de militar",
                                        color=ft.colors.BLUE_GREY,
                                        size=30, weight="bold", text_align=ft.TextAlign.CENTER)

                            ]
                        ),
                        # Adiciona a tabela na Row com rolagem
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [table_edit], scroll=ft.ScrollMode.ALWAYS)
                                ],
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            width=page.width - 40,  # Ajuste para considerar o padding
                            height=300,  # Altura fixa da tabela
                            bgcolor=ft.colors.GREY_50
                        ),
                        ft.Divider(),
                        ft.Row(controls=[])
                    ],
                    width=page.width,
                    height=page.height - 200  # Ajuste para considerar o espaço do cabeçalho e do menu
                ),
                padding=ft.padding.all(20),
                bgcolor=ft.colors.WHITE
            )
        elif e.control.text == "EMPENHO":
            painel_process = ft.Container(
                padding=ft.padding.all(10),
                alignment=ft.alignment.center,
                bgcolor="#081d33",
                expand=1,
                height=50,
                width=700,
                border_radius=6,
                content=ft.Text(
                    "",
                    size=18,
                    weight="bold",
                    color="#57A004"
                )
            )

            body_container.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Selecione o modo de carregamento desejado:",
                                        color=ft.colors.BLUE_700),
                                ft.ElevatedButton(
                                    text="Carregar Planilha",
                                    on_click=lambda _: file_picker.pick_files()
                                ),
                                ft.ElevatedButton(
                                    text="Carregar Manualmente",
                                    on_click=lambda _: print(
                                        "Carregar Manualmente")
                                )
                            ]
                        ),
                        # Adiciona a tabela na Row com rolagem
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [table_comum], scroll=ft.ScrollMode.ALWAYS)
                                ],
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            width=page.width - 40,  # Ajuste para considerar o padding
                            height=300,  # Altura fixa da tabela
                            bgcolor=ft.colors.GREY_50
                        ),
                        ft.Divider(),
                        ft.Row(controls=[painel_process])
                    ],
                    width=page.width,
                    height=page.height - 200  # Ajuste para considerar o espaço do cabeçalho e do menu
                ),
                padding=ft.padding.all(20),
                bgcolor=ft.colors.WHITE
            )
        elif e.control.text == "LIQUIDAÇÃO":
            body_container.content = ft.Container(
                bgcolor=ft.colors.RED,
                width=page.width,
                height=page.height - 200
            )
        elif e.control.text == "PAGAMENTO":
            body_container.content = ft.Container(
                bgcolor=ft.colors.GREEN,
                width=page.width,
                height=page.height - 200
            )
        page.update()

    def open_login_popup(e):
        login_dialog.open = True
        page.update()

    def process_login(e):
        if username.value == "admin" and password.value == "admin":
            login_dialog.open = False
            page.update()
        else:
            error_message.value = "Login ou senha incorretos"
            page.update()

    def cancel_login(e):
        login_dialog.open = False
        page.update()

    # Cabeçalho
    header = ft.Row(
        controls=[
            ft.Image(src="logo.png", width=50, height=50),
            ft.Text("FINANÇAS CBMMG BOT", style=ft.TextStyle(
                size=25, color=ft.colors.WHITE), text_align=ft.TextAlign.CENTER),
            ft.Image(src="logo.png", width=50, height=50),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=50,
        spacing=10
    )

    # Menu
    menu = ft.Row(
        controls=[
            ft.ElevatedButton(text="CADASTRO", on_click=change_color),
            ft.ElevatedButton(text="GESTÃO", on_click=change_color),
            ft.ElevatedButton(text="EMPENHO", on_click=change_color),
            ft.ElevatedButton(text="LIQUIDAÇÃO", on_click=change_color),
            ft.ElevatedButton(text="PAGAMENTO", on_click=change_color),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=50,
        spacing=10,
    )

    # Container do corpo da tela
    body_container = ft.Container(
        padding=ft.padding.symmetric(0, 20),
        content=ft.Container(
            padding=ft.padding.symmetric(0, 20),
            width=page.width,
            height=page.height - 200,
        )
    )

    # Elementos do popup de login
    username = ft.TextField(label="Usuário")
    password = ft.TextField(label="Senha", password=True,
                            can_reveal_password=True)
    error_message = ft.Text(value="", color=ft.colors.RED)
    login_dialog = ft.AlertDialog(
        title=ft.Text("Login"),
        content=ft.Column(
            controls=[username, password, error_message],
            tight=True
        ),
        actions=[
            ft.TextButton("Login", on_click=process_login),
            ft.TextButton("Cancelar", on_click=cancel_login)
        ]
    )

    page.overlay.append(login_dialog)
    page.add(
        header,
        menu,
        body_container
    )


ft.app(target=main)
