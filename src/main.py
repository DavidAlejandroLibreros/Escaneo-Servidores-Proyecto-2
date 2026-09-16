import flet as ft
from port_scanner import EscanerPuertos, es_url_valida, normalizar_url


def crear_tarjeta_puerto(info: dict) -> ft.Card:
    color_confianza = ft.Colors.GREEN_400 if info["confirmado"] else ft.Colors.AMBER_400
    texto_confianza = (
        f"Confirmado ({info['confianza']}/10)" if info["confirmado"] else "Supuesto por el puerto"
    )

    nombre_servicio = info["servicio"]
    if info["producto"]:
        nombre_servicio += f" — {info['producto']} {info['version']}".strip()

    contenido = [
        ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.LAN if info["protocolo"] == "tcp" else ft.Icons.WIFI_TETHERING,
                    color=ft.Colors.CYAN_300,
                ),
                ft.Text(f"Puerto {info['puerto']}/{info['protocolo']}", weight=ft.FontWeight.BOLD, size=16),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(texto_confianza, size=11, color=ft.Colors.BLACK),
                    bgcolor=color_confianza,
                    padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                    border_radius=10,
                ),
            ]
        ),
        ft.Text(nombre_servicio, color=ft.Colors.GREY_300),
    ]

    for nombre_script, salida in info["scripts"].items():
        contenido.append(ft.Text(f"{nombre_script}: {salida.strip()}", size=12, color=ft.Colors.GREY_500))

    return ft.Card(
        content=ft.Container(
            content=ft.Column(contenido, spacing=4),
            padding=15,
            bgcolor=ft.Colors.GREY_900,
            border_radius=10
        )
    )


def main(page: ft.Page):
    page.title = "Escáner de Puertos"
    page.bgcolor = "#0d1117"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30

    def hacer_escaneo(url):
        def al_encontrar_puerto(info):
            resultados.controls.append(crear_tarjeta_puerto(info))
            page.update()

        escaner = EscanerPuertos(url)
        escaner.escanear_en_vivo(al_encontrar_puerto)

        resultados.controls.append(
            ft.Container(
                content=ft.Text(escaner.detectar_sistema_operativo(), italic=True, color=ft.Colors.CYAN_200),
                padding=10,
            )
        )

        send_btn.visible = True
        progreso.visible = False
        url_box.disabled = False
        page.update()

    def send(e):
        url = normalizar_url(url_box.value)

        if not es_url_valida(url):
            resultados.controls = [ft.Text("URL inválida. Asegúrate de incluir una página verdadera", color=ft.Colors.RED_300)]
            page.update()
            return

        resultados.controls = []
        send_btn.visible = False
        progreso.visible = True
        url_box.disabled = True
        page.update()

        page.run_thread(hacer_escaneo, url)

    url_box = ft.TextField(
        label="Ingresa la URL",
        hint_text="https://ejemplo.com",
        expand=True,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.GREY_900,
        border_color=ft.Colors.CYAN_700,
    )

    send_btn = ft.FilledButton(
        "Escanear",
        icon=ft.Icons.SEARCH,
        on_click=send,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=30),
            bgcolor=ft.Colors.CYAN_700,
            color=ft.Colors.WHITE,
            padding=20,
        ),
    )

    progreso = ft.Row(
        controls=[
            ft.ProgressRing(width=18, height=18, stroke_width=2, color=ft.Colors.CYAN_300),
            ft.Text("Escaneando...", color=ft.Colors.CYAN_300),
        ],
        visible=False,
        spacing=8,
    )

    resultados = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    page.add(
        ft.Row(controls=[url_box, send_btn, progreso], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(content=resultados, expand=True, padding=ft.Padding(left=0, top=20, right=0, bottom=0)),
    )


if __name__ == "__main__":
    ft.run(main)