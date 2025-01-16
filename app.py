import flet as ft
import pandas as pd
import threading
from utils import POST_GRAD
from tabelas import table_comum, data_list, table_edit, data_list_edit, carregar_dados_table_edit, campo_field, drop_field
# Importação de Paginas
from pages.gestao import gestao_page
from pages.cadastro import cadastro_page
from pages.empenho import empenho_page

def main(page: ft.Page):
    # Input de planilha com dados excel
    file_picker = ft.FilePicker(on_result=lambda e: on_file_upload(e))
    page.overlay.append(file_picker)

    # Dimensionar tela
    page.window.width = 800
    page.window.height = 600

    # Cache para páginas carregadas
    cached_pages = {}

    def open_login_popup(e):
        login_dialog.open = True
        page.update()

    def on_file_upload(e):
        if not e.files:
            return

        def load_file():
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
                for index, row in df.iterrows():
                    data = row[required_columns].tolist()
                    data_list.append(data)
                    cells = [ft.DataCell(ft.Text(str(value), color=ft.Colors.BLUE_900))
                             for value in data]
                    delete_button = ft.ElevatedButton(
                        text="X",
                        on_click=lambda e, idx=index: delete_row(idx)
                    )
                    table_comum.rows.append(ft.DataRow(
                        cells=cells + [ft.DataCell(delete_button)]))

                table_comum.update()
            except Exception as err:
                page.add(ft.Text(f"Erro ao carregar o arquivo: {str(err)}"))

        threading.Thread(target=load_file).start()

    def delete_row(index):
        # Remover a linha da tabela e da lista de dados
        if 0 <= index < len(table_comum.rows):
            del table_comum.rows[index]
            del data_list[index]
            table_comum.update()

    def change_page(e):
        selected_page = e.control.text
        if selected_page in cached_pages:
            body_container.content = cached_pages[selected_page]
        else:
            if selected_page == "CADASTRO":
                cached_pages["CADASTRO"] = cadastro_page(page)
            elif selected_page == "GESTÃO":
                carregar_dados_table_edit(page)
                cached_pages["GESTÃO"] = gestao_page(page, table_edit)
            elif selected_page == "EMPENHO":
                cached_pages["EMPENHO"] = empenho_page(page, table_comum, file_picker)
            elif selected_page == "LIQUIDAÇÃO":
                cached_pages["LIQUIDAÇÃO"] = ft.Container(
                    bgcolor=ft.Colors.RED,
                    width=page.width,
                    height=page.height - 200
                )
            elif selected_page == "PAGAMENTO":
                cached_pages["PAGAMENTO"] = ft.Container(
                    bgcolor=ft.Colors.GREEN,
                    width=page.width,
                    height=page.height - 200
                )
            body_container.content = cached_pages[selected_page]

        body_container.update()

    # Cabeçalho
    header = ft.Row(
        controls=[
            ft.Image(src="logo.png", width=50, height=50),
            ft.Text("FINANÇAS CBMMG BOT", style=ft.TextStyle(
                size=25, color=ft.Colors.WHITE), text_align=ft.TextAlign.CENTER),
            ft.Image(src="logo.png", width=50, height=50),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=50,
        spacing=10
    )

    # Menu
    menu = ft.Row(
        controls=[
            ft.ElevatedButton(text="CADASTRO", on_click=change_page),
            ft.ElevatedButton(text="GESTÃO", on_click=change_page),
            ft.ElevatedButton(text="EMPENHO", on_click=change_page),
            ft.ElevatedButton(text="LIQUIDAÇÃO", on_click=change_page),
            ft.ElevatedButton(text="PAGAMENTO", on_click=change_page),
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
            bgcolor=ft.Colors.WHITE
        ),
        height=page.height - 100  # Altura fixa
    )

    page.add(
        header,
        menu,
        body_container
    )

ft.app(target=main)
