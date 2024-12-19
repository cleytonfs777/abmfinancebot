import flet as ft
from db import todos_militares, deletar_militar, ler_militar, atualizar_militar
from utils import POST_GRAD

# Estilos dos campos
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


# Colunas predefinidas para a tabela
table_columns = [
    ft.DataColumn(ft.Text('Nº BM', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('P/G', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Nome', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('RG', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('CPF', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Banco', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('CC', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Agencia', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('PIS/PASEP', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('DOC SEI', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Ação', color=ft.Colors.BLUE_700))
]

table_comum = ft.DataTable(columns=table_columns, rows=[])
data_list = []

# Colunas predefinidas para a tabela
table_edit_columns = [
    ft.DataColumn(ft.Text('Nº BM', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('P/G', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Nome', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('RG', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('CPF', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Banco', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('CC', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Agencia', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Tipo', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Vantagem', color=ft.Colors.BLUE_700)),
    ft.DataColumn(ft.Text('Ações', color=ft.Colors.BLUE_700)),
]

table_edit = ft.DataTable(columns=table_edit_columns, rows=[])
popup_confirmacao = None  # Placeholder para o popup de confirmação


popup_edicao = None  # Placeholder para o popup de edição


def carregar_dados_table_edit(page):
    """Carrega os registros do banco de dados e insere na tabela 'table_edit'."""
    registros = todos_militares()  # Busca todos os registros do banco
    linhas = []

    for registro in registros:
        # Gera as células de texto para cada registro
        cells = [ft.DataCell(ft.Text(str(valor), color=ft.Colors.BLUE_900))
                 for valor in registro[1:]]  # Ignorando o ID (primeiro valor)

        # Botões Editar e Excluir
        botoes = ft.DataCell(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=ft.Colors.GREEN,
                        tooltip="Editar registro",
                        on_click=lambda e, id=registro[0]: abrir_popup_edicao(page, id)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Excluir registro",
                        on_click=lambda e, id=registro[0], nome=registro[3]: confirmar_exclusao(page, id, nome)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )

        # Adiciona as células + botões à linha
        linhas.append(ft.DataRow(cells=cells + [botoes]))

    # Atualiza a tabela com as linhas
    table_edit.rows = linhas


def abrir_popup_edicao(page, militar_id):
    """Abre um popup com os dados do militar preenchidos para edição."""
    # Busca os dados do militar pelo ID
    militar = ler_militar(militar_id)
    if not militar:
        return

    # Campos editáveis com o mesmo estilo usado no Cadastro
    numero = campo_field("Nº BM", max_l=7, apenas_numeros=True)
    gradpost = drop_field(POST_GRAD, label="P/G")
    nome = campo_field("Nome")
    rg = campo_field("RG")
    cpf = campo_field("CPF")
    banco = campo_field("Banco")
    cc = campo_field("Conta Corrente")
    agencia = campo_field("Agência")
    tipo_vant = drop_field(["QQ", "ADE"], label="Tipo de Vantagem")
    vantagem = campo_field("Vantagem", max_l=2, apenas_numeros=True)

    # Preenche os campos com os dados do militar
    numero.value = militar[1]
    gradpost.value = militar[2]
    nome.value = militar[3]
    rg.value = militar[4]
    cpf.value = militar[5]
    banco.value = militar[6]
    cc.value = militar[7]
    agencia.value = militar[8]
    tipo_vant.value = militar[9]
    vantagem.value = str(militar[10])

    # Função para salvar as alterações
    def salvar_alteracoes(e):
        try:
            atualizar_militar(
                militar_id,
                numero=numero.value,
                gradpost=gradpost.value,
                nome=nome.value,
                rg=rg.value,
                cpf=cpf.value,
                banco=banco.value,
                cc=cc.value,
                agencia=agencia.value,
                type_vant=tipo_vant.value,
                vantagem=int(vantagem.value)
            )
            fechar_popup_main(page)  # Fecha o popup
            carregar_dados_table_edit(page)  # Recarrega a tabela
            print(f"Registro {militar_id} atualizado com sucesso!")
        except Exception as ex:
            print(f"Erro ao salvar alterações: {ex}")

    # Configuração do Popup
    popup_edicao = ft.AlertDialog(
    title=ft.Text("Editar Registro"),
    content=ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.WHITE10,
        width=800,  # Aumenta a largura do popup
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
            padding=ft.padding.all(16),
            border_radius=6,
            content=ft.Column(
                alignment=ft.alignment.center,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Row(
                        controls=[numero, gradpost],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=6, color="transparent"),
                    ft.Row(
                        controls=[nome, rg],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=6, color="transparent"),
                    ft.Row(
                        controls=[cpf, banco],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=6, color="transparent"),
                    ft.Row(
                        controls=[cc, agencia],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=6, color="transparent"),
                    ft.Row(
                        controls=[tipo_vant, vantagem],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
        ),
    ),
    actions=[
        ft.TextButton("Cancelar", on_click=lambda e: fechar_popup_main(page)),
        ft.TextButton("Salvar", on_click=salvar_alteracoes),
    ],
    modal=True
    )


    # Substitui page.dialog por page.overlay.append
    page.overlay.append(popup_edicao)
    popup_edicao.open = True
    page.update()


def fechar_popup_main(page):
    """Fecha qualquer popup atualmente aberto."""
    for overlay in page.overlay:
        if isinstance(overlay, ft.AlertDialog):
            overlay.open = False
    page.update()



def confirmar_exclusao(page, militar_id, nome_militar):
    """Exibe um popup de confirmação antes de excluir um registro."""
    global popup_confirmacao

    # Define o conteúdo do popup com o nome do militar
    popup_confirmacao = ft.AlertDialog(
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text(f"Tem certeza de que deseja excluir o registro de {nome_militar}?"),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: fechar_popup(page)
            ),
            ft.TextButton(
                "Confirmar",
                on_click=lambda e: excluir_registro(page, militar_id)
            )
        ],
        modal=True
    )

    # Exibe o popup
    page.dialog = popup_confirmacao
    popup_confirmacao.open = True
    page.update()

def excluir_registro(page, militar_id):
    """Exclui o registro após confirmação e atualiza a tabela."""
    deletar_militar(militar_id)
    print(f"Registro {militar_id} deletado com sucesso!")
    fechar_popup(page)  # Fecha o popup
    carregar_dados_table_edit(page)  # Recarrega a tabela


def fechar_popup(page):
    """Fecha o popup de confirmação."""
    global popup_confirmacao
    if popup_confirmacao:
        popup_confirmacao.open = False
        page.update()

data_list_edit = []