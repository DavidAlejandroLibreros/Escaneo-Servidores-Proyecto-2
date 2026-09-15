import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def send(e):
        url = url_box.value
        page.show_dialog(ft.SnackBar(ft.Text(f"Escaneando: {url} ...")))
        result.value="Espera"
        page.update()

    url_box = ft.TextField("Ingresa la URL", expand=True)
    send_btn = ft.Button("Escanear", on_click=send)
    result = ft.Text("Ingresa la URL y has clic en Escanear")

    page.add(
        ft.Row(
            expand=True,
            controls=[url_box, send_btn]
        ),
        ft.Row(
            expand=True,
            controls=[result]
        )
    )


if __name__ == "__main__":
    ft.run(main)
