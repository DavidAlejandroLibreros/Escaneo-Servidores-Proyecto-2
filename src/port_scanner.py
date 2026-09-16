import nmap
import subprocess
import re
from urllib.parse import urlparse

def normalizar_url(texto: str) -> str:
    texto = texto.strip()
    if texto and "://" not in texto:
        texto = f"https://{texto}"
    return texto


def es_url_valida(texto: str) -> bool:
    resultado = urlparse(texto)
    return resultado.scheme in ("http", "https") and bool(resultado.hostname)


class EscanerPuertos:
    def __init__(self, url: str, puertos: str = "1-1000"):
        self.url = url
        self.host = urlparse(url).hostname
        self.puertos = puertos

    def escanear_en_vivo(self, al_encontrar_puerto):
        proceso = subprocess.Popen(
            ["nmap", "-v", "-sS", "-sU", "-p", self.puertos, self.host],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        patron = re.compile(r"Discovered open port (\d+)/(\w+) on")

        for linea in proceso.stdout:
            coincidencia = patron.search(linea)
            if coincidencia:
                puerto, protocolo = coincidencia.groups()
                detalle = self._escanear_detalle(puerto, protocolo)
                al_encontrar_puerto(detalle)

        proceso.wait()

    def _escanear_detalle(self, puerto: str, protocolo: str) -> dict:
        scanner = nmap.PortScanner()
        argumentos = "-sU -sV" if protocolo == "udp" else "-sV -sC"
        scanner.scan(self.host, puerto, arguments=argumentos)

        if not scanner.all_hosts():
            return {
                "puerto": puerto, "protocolo": protocolo, "servicio": "desconocido",
                "producto": "", "version": "", "confirmado": False,
                "confianza": "0", "scripts": {},
            }

        host_real = scanner.all_hosts()[0]
        datos = scanner[host_real][protocolo][int(puerto)]

        return {
            "puerto": puerto,
            "protocolo": protocolo,
            "servicio": datos.get("name", "desconocido"),
            "producto": datos.get("product", ""),
            "version": datos.get("version", ""),
            "confirmado": datos.get("method") == "probed",
            "confianza": datos.get("conf", "0"),
            "scripts": datos.get("script", {}),
        }

    def detectar_sistema_operativo(self) -> str:
        scanner = nmap.PortScanner()
        scanner.scan(self.host, arguments="-O")

        if not scanner.all_hosts():
            return "No se pudo determinar el sistema operativo."

        host_real = scanner.all_hosts()[0]
        coincidencias = scanner[host_real].get("osmatch", [])

        if not coincidencias:
            return "No se pudo determinar el sistema operativo."

        mejor = coincidencias[0]
        return f"Sistema operativo probable: {mejor['name']} ({mejor['accuracy']}% de confianza)"