# Aplicación de escáner


## Crear ambiente virtual

```bash
python -m venv mi_virtualenv
```

## Instalar librerías

```bash
pip install python-nmap
```

> [!NOTE]
> Debe tener instalado NMAP para que la librería funcione.

### Interfaz gráfica

```bash
pip install 'flet[all]'
```

> [!NOTE]
> Esto no aplica para los proyectos que no incluyen interfaz gráfica

## Ejecutar la aplicación

### uv

Ejecutar como aplicación de escritorio:

```bash
flet run
```

Ejecutar como aplicación web:

```bash
flet run --web
```

Para más detalles sobre cómo ejecutar la aplicación, consulte la [Guía de inicio](https://flet.dev/docs/).

## Compilar la aplicación

### Android

```bash
flet build apk -v
```

Para más detalles sobre cómo compilar y firmar `.apk` o `.aab`, consulte la [Guía de empaquetado para Android](https://flet.dev/docs/publish/android/).

### iOS

```bash
flet build ipa -v
```

Para más detalles sobre cómo compilar y firmar `.ipa`, consulte la [Guía de empaquetado para iOS](https://flet.dev/docs/publish/ios/).

### macOS

```bash
flet build macos -v
```

Para más detalles sobre cómo compilar un paquete para macOS, consulte la [Guía de empaquetado para macOS](https://flet.dev/docs/publish/macos/).

### Linux

```bash
flet build linux -v
```

Para más detalles sobre cómo compilar un paquete para Linux, consulte la [Guía de empaquetado para Linux](https://flet.dev/docs/publish/linux/).

### Windows

```bash
flet build windows -v
```

Para más detalles sobre cómo compilar un paquete para Windows, consulte la [Guía de empaquetado para Windows](https://flet.dev/docs/publish/windows/).

### Web

```bash
flet build web -v
```

Para más detalles sobre cómo compilar la aplicación web, consulte la [Guía de empaquetado para Web](https://flet.dev/docs/publish/web/).

