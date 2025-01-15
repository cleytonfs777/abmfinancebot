import flet as ft

def gestao_page(page: ft.Page, table_edit):
    response = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Edição e Exclusão de militar",
                                        color=ft.Colors.BLUE_GREY,
                                        size=30, weight="bold", text_align=ft.TextAlign.CENTER)
                            ]
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row([table_edit], scroll=ft.ScrollMode.ALWAYS)
                                ],
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            width=page.width - 40,
                            height=300,
                            bgcolor=ft.Colors.GREY_50
                        )
                    ],
                    width=page.width,
                    height=page.height - 200
                ),
                padding=ft.padding.all(20),
                bgcolor=ft.Colors.WHITE
            )
    page.update()

    return response