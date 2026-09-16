import flet as ft
from port_scanner import EscanerPuertos, es_url_valida, normalizar_url

def main(page: ft.Page):
    def hacer_escaneo(url):
        def al_encontrar_puerto(texto):
            resultados.controls.append(ft.Text(texto))
            page.update()

        escaner = EscanerPuertos(url)
        escaner.escanear_en_vivo(al_encontrar_puerto)

        resultados.controls.append(ft.Text(escaner.detectar_sistema_operativo()))
        resultados.controls.append(ft.Text("Escaneo finalizado..."))
        send_btn.disabled = False
        url_box.disabled = False
        page.update()

    def send(e):
        url = normalizar_url(url_box.value)

        if not es_url_valida(url):
            resultados.controls = [ft.Text("URL inválida. Asegúrate de incluir una página verdadera")]
            page.update()
            return

        resultados.controls = [ft.Text("Escaneando, los puertos abiertos irán apareciendo aquí...")]
        send_btn.disabled = True
        url_box.disabled = True
        page.update()

        page.run_thread(hacer_escaneo, url)

    url_box = ft.TextField(label="Ingresa la URL", hint_text="https://ejemplo.com", expand=True)
    send_btn = ft.Button("Escanear", on_click=send)
    resultados = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(
        ft.Row(expand=True, controls=[url_box, send_btn]),
        ft.Row(expand=True, controls=[resultados]),
    )


if __name__ == "__main__":
    ft.run(main)
