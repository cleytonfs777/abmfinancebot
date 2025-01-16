import flet as ft
from utils import create_login_dialog, MUNICIPIOS
from db import ler_militares
from datetime import datetime
import pandas as pd

# Criar a tabela de valores como um DataFrame
TABELA_VALORES = pd.read_csv("tabela_valores.csv")

def calcular_qtd_diarias(inicio, fim):
    fmt = "%d/%m/%Y %H:%M"
    try:
        inicio_dt = datetime.strptime(inicio, fmt)
        fim_dt = datetime.strptime(fim, fmt)
        delta = fim_dt - inicio_dt
        dias = delta.days
        horas_restantes = delta.seconds / 3600
        if horas_restantes >= 12:
            return dias + 0.5
        elif horas_restantes > 0:
            return dias + 0.5 if dias == 0 else dias
        return dias
    except Exception:
        return 0

def calcular_valor(pg, vantagem, destino, qtd_diarias):
    # Determinar a categoria do município
    if destino in ["Belo Horizonte"] or destino in MUNICIPIOS:
        categoria = "Capitais"
    elif destino in ["Uberlândia", "Patos de Minas", "Poços de Caldas"]:
        categoria = "Especiais"
    else:
        categoria = "Demais"

    # Filtrar a tabela com base no P/G e Vantagem
    linha = TABELA_VALORES[
        (TABELA_VALORES["P/G"] == pg) & 
        (TABELA_VALORES["Vantagem"] == vantagem)
    ]

    if linha.empty:
        print(f"Erro: Não encontrado valor para P/G {pg}, Vantagem {vantagem}.")
        return 0

    # Obter o valor base e calcular o total
    # substitui , por . e converte para float
    valor_base = float(linha[categoria].str.replace(",", ".").values[0])
    return valor_base * qtd_diarias

def empenho_page(page: ft.Page, table_comum, file_picker):
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
            color="#000000"
        )
    )

    # Criar o diálogo de login no início do programa
    login_dialog = create_login_dialog(page)
    page.overlay.append(login_dialog)

    def gerar_empenho(e):
        login_dialog.open = True
        page.update()
        print("Empenho Gerado com sucesso!!!")

    def buscar_militares(e):
        nome = pesquisa_input.value.strip()
        if nome:
            resultados = ler_militares("nome", nome)
            tabela_dados.rows.clear()
            for militar in resultados:
                tabela_dados.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(militar[1], color="#000000")),
                            ft.DataCell(ft.Text(militar[2], color="#000000")),
                            ft.DataCell(ft.Text(militar[3], color="#000000")),
                            ft.DataCell(ft.Text(militar[4], color="#000000")),
                            ft.DataCell(ft.Text(militar[5], color="#000000")),
                            ft.DataCell(ft.Text(militar[6], color="#000000")),
                            ft.DataCell(ft.Text(militar[7], color="#000000")),
                            ft.DataCell(ft.Text(militar[8], color="#000000")),
                            ft.DataCell(ft.Text(militar[9], color="#000000")),
                            ft.DataCell(ft.Text(militar[10], color="#000000")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    on_click=lambda e, m=militar: adicionar_na_tabela_final(m)
                                )
                            )
                        ]
                    )
                )
            tabela_dados.update()
        else:
            tabela_dados.rows.clear()
            tabela_dados.update()

    def adicionar_na_tabela_final(militar):
        for row in tabela_final.rows:
            if row.cells[0].content.value == militar[1]:
                print("Número já existe na tabela final.")
                return

        inicio = inicio_dsp.value
        fim = fim_dsp.value
        destino = municipio_destino.value

        qtd_diarias = calcular_qtd_diarias(inicio, fim)
        valor = calcular_valor(militar[2], militar[10], destino, qtd_diarias)

        def remover_row(e):
            tabela_final.rows.remove(new_row)
            tabela_final.update()

        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(militar[1], color="#000000")),
                ft.DataCell(ft.Text(militar[2], color="#000000")),
                ft.DataCell(ft.Text(militar[3], color="#000000")),
                ft.DataCell(ft.Text(militar[4], color="#000000")),
                ft.DataCell(ft.Text(militar[5], color="#000000")),
                ft.DataCell(ft.Text(militar[6], color="#000000")),
                ft.DataCell(ft.Text(militar[7], color="#000000")),
                ft.DataCell(ft.Text(militar[8], color="#000000")),
                ft.DataCell(ft.Text(militar[9], color="#000000")),
                ft.DataCell(ft.Text(militar[10], color="#000000")),
                ft.DataCell(ft.Text(str(qtd_diarias), color="#000000")),
                ft.DataCell(ft.Text(f"R$ {valor:.2f}", color="#000000")),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.REMOVE,
                        on_click=remover_row
                    )
                )
            ]
        )
        tabela_final.rows.append(new_row)
        tabela_final.update()

    def remover_da_tabela_final(row):
        tabela_final.rows.remove(row)
        tabela_final.update()

    # Primeira divisão
    primeira_divisao_titulo = ft.Container(
        content=ft.Text(
            "DEFINIÇÕES DE LOCAIS",
            size=16,
            weight="bold",
            color="#000000"
        ),
        padding=ft.padding.only(bottom=10)
    )

    inicio_dsp = ft.TextField(
        label="Início DSP (Data e Hora)",
        hint_text="DD/MM/AAAA HH:MM",
        width=250,
        border_color="#000000",
        border_radius=6,
        text_style=ft.TextStyle(color="#000000")
    )

    fim_dsp = ft.TextField(
        label="Fim DSP (Data e Hora)",
        hint_text="DD/MM/AAAA HH:MM",
        width=250,
        border_color="#000000",
        border_radius=6,
        text_style=ft.TextStyle(color="#000000")
    )

    municipio_origem = ft.Dropdown(
        label="Município de Origem",
        options=[ft.dropdown.Option(municipio) for municipio in MUNICIPIOS],
        width=250,
        border_color="#000000",
        border_radius=6,
    )

    municipio_destino = ft.Dropdown(
        label="Município de Destino",
        options=[ft.dropdown.Option(municipio) for municipio in MUNICIPIOS],
        width=250,
        border_color="#000000",
        border_radius=6,
    )

    primeira_divisao = ft.Column(
        controls=[
            primeira_divisao_titulo,
            ft.Row(
                controls=[inicio_dsp, fim_dsp],
                spacing=20,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            ft.Row(
                controls=[municipio_origem, municipio_destino],
                spacing=20,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        ],
        spacing=20,
        tight=True
    )

    # Segunda divisão
    segunda_divisao_titulo = ft.Container(
        content=ft.Text(
            "SELEÇÃO DE MILITARES DILIGENTES",
            size=16,
            weight="bold",
            color="#000000"
        ),
        padding=ft.padding.only(top=20, bottom=10)
    )
    pesquisa_input = ft.TextField(
        label="Pesquisar Militar",
        expand=True,
        border_color="#000000",
        border_radius=6,
        text_style=ft.TextStyle(color="#000000")
    )
    lupa_pesquisa = ft.IconButton(
        icon=ft.Icons.SEARCH,
        on_click=buscar_militares,
        icon_color="white",
        bgcolor="#12204C",
    )
    tabela_dados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número", color="#000000")),
            ft.DataColumn(ft.Text("P/G", color="#000000")),
            ft.DataColumn(ft.Text("Nome", color="#000000")),
            ft.DataColumn(ft.Text("RG", color="#000000")),
            ft.DataColumn(ft.Text("CPF", color="#000000")),
            ft.DataColumn(ft.Text("Banco", color="#000000")),
            ft.DataColumn(ft.Text("Conta Corrente", color="#000000")),
            ft.DataColumn(ft.Text("Agência", color="#000000")),
            ft.DataColumn(ft.Text("Tipo de Vantagem", color="#000000")),
            ft.DataColumn(ft.Text("Vantagem", color="#000000")),
            ft.DataColumn(ft.Text("Ação", color="#000000"))
        ],
        rows=[]
    )

    segunda_divisao = ft.Column(
        controls=[
            segunda_divisao_titulo,
            ft.Row(controls=[pesquisa_input, lupa_pesquisa], spacing=10),
            tabela_dados
        ],
        tight=True
    )

    # Terceira divisão
    terceira_divisao_titulo = ft.Container(
        content=ft.Text(
            "MILITARES PARA GERAÇÃO DE EMPENHO",
            size=16,
            weight="bold",
            color="#000000"
        ),
        padding=ft.padding.only(top=20, bottom=10)
    )
    tabela_final = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número", color="#000000")),
            ft.DataColumn(ft.Text("P/G", color="#000000")),
            ft.DataColumn(ft.Text("Nome", color="#000000")),
            ft.DataColumn(ft.Text("RG", color="#000000")),
            ft.DataColumn(ft.Text("CPF", color="#000000")),
            ft.DataColumn(ft.Text("Banco", color="#000000")),
            ft.DataColumn(ft.Text("Conta Corrente", color="#000000")),
            ft.DataColumn(ft.Text("Agência", color="#000000")),
            ft.DataColumn(ft.Text("Tipo de Vantagem", color="#000000")),
            ft.DataColumn(ft.Text("Vantagem", color="#000000")),
            ft.DataColumn(ft.Text("Qtd Diárias", color="#000000")),
            ft.DataColumn(ft.Text("Valor", color="#000000")),
            ft.DataColumn(ft.Text("Ação", color="#000000"))
        ],
        rows=[]
    )

    terceira_divisao = ft.Column(
        controls=[
            terceira_divisao_titulo,
            tabela_final],
        tight=True
    )

    body_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Divider(),
                primeira_divisao,
                ft.Divider(),
                segunda_divisao,
                ft.Divider(),
                terceira_divisao,
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Gerar Empenho",
                            on_click=lambda e: gerar_empenho(e),
                            bgcolor="#000000",
                            color="white",
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,
            tight=True
        ),
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.WHITE
    )

    page.update()
    return body_container
