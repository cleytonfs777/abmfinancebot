import flet as ft

# Colunas predefinidas para a tabela
table_columns = [
    ft.DataColumn(ft.Text('Nº BM', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('P/G', color=ft.colors.BLUE_700)),
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

table_comum = ft.DataTable(columns=table_columns, rows=[])
data_list = []

# COlunas predefinidas para tabela de edição e exclusão de militares
table_edit_columns = [
    ft.DataColumn(ft.Text('Nº BM', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('P/G', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('Nome', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('RG', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('CPF', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('Banco', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('CC', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('Agencia', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('tipo', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('Vantagem', color=ft.colors.BLUE_700)),
    ft.DataColumn(ft.Text('Ação', color=ft.colors.BLUE_700))
]

table_edit = ft.DataTable(columns=table_edit_columns, rows=[])
data_list_edit = []

#
rows_main =[]
data_main = ["123456", "Cap", "Cleyton Batista de Jesus", "MG44562445", "068.356.086-06", "077 - Inter", "4566841-9", "0001", "QQ", "05"]
cells = [ft.DataCell(ft.Text(str(value), color=ft.colors.BLUE_900))
                         for value in data_main]

# Deletar btn
delete_button = ft.ElevatedButton(
    text="X",
    on_click=lambda _:print("Teste teste")
)

# Edital btn
edit_button = ft.ElevatedButton(
    text="X",
    on_click=lambda _:print("Teste teste")
)
rows.append(ft.DataRow(
    cells=cells + [ft.DataCell(delete_button, edit_button)]))

rows_main.append(ft.DataRow(cells=cells))

table_edit.rows = rows_main