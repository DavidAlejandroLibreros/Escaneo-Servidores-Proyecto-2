import nmap

objetivo = "127.0.0.1"
puertos = "22,80,443,8080"

scanner = nmap.PortScanner()
resultado = scanner.scan(objetivo, puertos)

for host in scanner.all_hosts():
    print(f"Host: {host}")
    print(f"Estado: {scanner[host].state()}")

    for protocolo in scanner[host].all_protocols():
        print(f"\nProtocolo: {protocolo}")

        for puerto in sorted(scanner[host][protocolo]):
            datos = scanner[host][protocolo][puerto]

            print(
                f"Puerto {puerto}: "
                f"{datos.get('state', 'desconocido')} "
                f"{datos.get('name', '')}"
            )
