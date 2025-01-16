import flet as ft
from db import criar_militar, ler_militares
from tabelas import campo_field, drop_field
from utils import POST_GRAD, VANTEGENS


def cadastro_page(page: ft.Page):

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
    vant_f = drop_field(VANTEGENS,"Tipo de Vantagem") 


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
        if not vant_f.value:
            erros.append("O campo 'Vantagem' é obrigatório.")
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
                    content=ft.Text(f"O registro com o número {numero_f.value} já está cadastrado."),
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
                    vantagem=vant_f.value
                )
                page.update()
                popup_sucesso = ft.AlertDialog(
                    title=ft.Text("Cadastro realizado"),
                    content=ft.Text(f"O registro com o número {numero_f.value} foi cadastrado com sucesso."),
                    actions=[ft.TextButton(
                        "OK", on_click=lambda e: fechar_popup(popup_sucesso))],
                    modal=True
                )
                page.overlay.append(popup_sucesso)
                limpar_campos()
                popup_sucesso.open = True
                page.update()

    def fechar_popup(dialog):
        dialog.open = False
        page.update()

    body_container = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.WHITE10,
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
                    ft.Text("Cadastro de Militares", color=ft.Colors.BLUE_GREY,
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

    return body_container