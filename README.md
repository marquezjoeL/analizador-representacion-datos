# Laboratorio de representaciones

Aplicación educativa Django para convertir valores entre las bases 2, 8, 10 y 16 (rango 0–65,535) y examinar puntos de código Unicode y bytes UTF-8 de textos de hasta 20 caracteres.

## Ejecución local

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. Ejecuta las seis pruebas automatizadas con:

```bash
python manage.py test conversor
```

## Docker

Construye y arranca el servicio (publicado en el puerto 8000):

```bash
docker compose build
docker compose up -d
```

Comprueba sus límites configurados y los límites efectivos del contenedor:

```bash
docker compose config
docker inspect $(docker compose ps -q web) --format 'RAM={{.HostConfig.Memory}} bytes; CPU={{.HostConfig.NanoCpus}} nanocpus'
```

La configuración Compose fija `mem_limit: 256m` y `cpus: 1.0` (268435456 bytes de RAM y 1000000000 nanocpus). Consulta la aplicación en <http://localhost:8000/> y detén el contenedor con `docker compose down`.

## Arquitectura de Von Neumann y contenedores

La aplicación usa memoria para mantener temporalmente instrucciones y datos durante su ejecución; la CPU ejecuta el servidor Django y sus operaciones, y la entrada/salida ocurre mediante el navegador y la respuesta HTTP. Las conversiones ilustran datos binarios y las representaciones que la CPU procesa.

Docker comparte el kernel del sistema operativo anfitrión porque los contenedores aíslan procesos y recursos mediante mecanismos del kernel, en lugar de arrancar un kernel propio como una máquina virtual. La imagen contiene el espacio de usuario de Python/Django; el kernel compartido administra los procesos, la memoria y la CPU asignada al contenedor.
