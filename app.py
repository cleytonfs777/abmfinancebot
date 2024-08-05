import flet as ft
import pandas as pd


def main(page: ft.Page):
    # Input de planilha com dados excel
    file_picker = ft.FilePicker(on_result=lambda e: on_file_upload(e))
    page.overlay.append(file_picker)

    # Colunas predefinidas para a tabela
    table_columns = [
        ft.DataColumn(ft.Text('Nome', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('RG', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('CPF', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('Banco', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('CC', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('Agencia', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('PIS/PASEP', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('DOC SEI', color=ft.colors.BLUE_700)),
        ft.DataColumn(ft.Text('Ação', color=ft.colors.BLUE_700))
    ]

    table = ft.DataTable(columns=table_columns, rows=[])
    data_list = []

    def on_file_upload(e):
        if not e.files:
            return

        file_path = e.files[0].path
        try:
            df = pd.read_excel(file_path)
            # Validar o cabeçalho
            required_columns = ['Nome', 'RG', 'CPF', 'Banco',
                                'CC', 'Agencia', 'PIS/PASEP', 'DOC SEI']
            if not all(col in df.columns for col in required_columns):
                page.add(ft.Text("Formato de planilha inválido"))
                return

            # Criar as linhas da tabela e a lista de dados
            rows = []
            for index, row in df.iterrows():
                data = row[required_columns].tolist()
                data_list.append(data)
                cells = [ft.DataCell(ft.Text(str(value)))
                         for value in data]
                delete_button = ft.ElevatedButton(
                    text="X",
                    on_click=lambda e, idx=index - 1: delete_row(idx)
                )
                rows.append(ft.DataRow(
                    cells=cells + [ft.DataCell(delete_button)]))

            table.rows = rows
            page.update()
        except Exception as e:
            page.add(ft.Text(f"Erro ao carregar o arquivo: {str(e)}"))

    def delete_row(index):
        # Remover a linha da tabela e da lista de dados
        del table.rows[index]
        del data_list[index]
        page.update()

    def gerar_empenho(e):
        for item in data_list:
            print(item)
            page.add(ft.Text(str(item)))

    # Função para mudar a cor do container no corpo da tela
    def change_color(e):
        if e.control.text == "EMPENHO":
            body_container.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Carregue o arquivo com os dados:",
                                        color=ft.colors.BLUE_700),
                                ft.ElevatedButton(
                                    text="Selecionar Arquivo",
                                    on_click=lambda _: file_picker.pick_files()
                                ),
                            ]
                        ),
                        # Adiciona a tabela na Row com rolagem
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row([table], scroll=ft.ScrollMode.ALWAYS)],
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            width=page.width - 40,  # Ajuste para considerar o padding
                            height=300,  # Altura fixa da tabela
                            bgcolor=ft.colors.GREY_50,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Gerar Empenho",
                                    on_click=gerar_empenho
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    width=page.width,
                    height=page.height - 200,  # Ajuste para considerar o espaço do cabeçalho e do menu
                ),
                padding=ft.padding.all(20),
                bgcolor=ft.colors.WHITE,
            )
        elif e.control.text == "LIQUIDAÇÃO":
            body_container.content = ft.Container(
                bgcolor=ft.colors.RED,
                width=page.width,
                height=page.height - 200,
            )
        elif e.control.text == "PAGAMENTO":
            body_container.content = ft.Container(
                bgcolor=ft.colors.GREEN,
                width=page.width,
                height=page.height - 200,
            )
        page.update()

    # Função para abrir o popup de login
    def open_login_popup(e):
        login_dialog.open = True
        page.update()

    # Função para processar o login
    def process_login(e):
        if username.value == "admin" and password.value == "admin":
            login_dialog.open = False
            page.update()
        else:
            error_message.value = "Login ou senha incorretos"
            page.update()

    # Função para cancelar o login
    def cancel_login(e):
        login_dialog.open = False
        page.update()

    # Cabeçalho
    header = ft.Row(
        controls=[
            # Substitua "logo.png" pelo caminho da sua logo
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
            height=page.height - 200,  # Ajuste para considerar o espaço do cabeçalho e do menu
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

    # Adicionar componentes à página
    page.overlay.append(login_dialog)
    page.add(
        header,
        menu,
        body_container
    )


ft.app(target=main)
