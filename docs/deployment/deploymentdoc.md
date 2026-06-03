# Despliegue de modelos

## Infraestructura

- **Nombre del modelo:** RealWaste Classifier (`model_prd_colab.keras`)

- **Plataforma de despliegue:** Máquina on premise GMKTEC con 96 GB de RAM y 2 TB de almacenamiento. El acceso remoto se realiza mediante VPN de Cloudflare con autenticación OAuth 2.0; el acceso local se realiza directamente desde la red interna.

- **Requisitos técnicos:**
  - Docker Engine (versión 24 o superior) con soporte para Docker Compose v2
  - Python 3.11 (incluido en la imagen base del contenedor de la API)
  - TensorFlow 2.19.0 (incluido en la imagen base del contenedor de la API)
  - Keras (última versión compatible, instalada en el contenedor)
  - FastAPI 0.115.0, Uvicorn 0.30.0, python-multipart 0.0.9 (dependencias de la API)
  - Node.js 22 + Nginx Alpine (usados durante la construcción del contenedor del frontend)
  - Archivo del modelo en formato `.keras` ubicado en `scripts/evaluation/`
  - Disponibilidad de los puertos locales **7000** y **7001**

- **Requisitos de seguridad:**
  - Acceso remoto protegido mediante VPN de Cloudflare con autenticación OAuth 2.0
  - El túnel de Cloudflare (`cloudflared`) es el único punto de entrada público; el servidor no expone puertos directamente a Internet
  - El token del túnel (`CF_TUNNEL_TOKEN`) debe mantenerse confidencial y gestionarse como secreto de entorno
- **Diagrama de arquitectura:**

  ```
  Usuario (Internet)
        │
        ▼
  Cloudflare Tunnel (cloudflared)  ←── CF_TUNNEL_TOKEN
        │
        ▼
  Frontend – Nginx (puerto 7000)   ◄── VITE_URL_EP
        │
        ▼
  API de predicción – FastAPI/Uvicorn (puerto 7001→8000)
        │
        ▼
  Modelo Keras (model_prd_colab.keras)
  ```

  Para uso local (sin túnel), el usuario accede directamente a `http://localhost:7000/`. El diagrama de la respuesta del servidor con la predicción realizada es completamente análogo, pero sin la capa de Cloudflare.

---

## Código de despliegue

- **Archivos principales:**
  - `src/docker-compose-local.yml` — despliegue local para revisión y pruebas
  - `src/docker-compose-online.yml` — despliegue en línea desde el servidor hosting (incluye túnel Cloudflare)
- **Rutas de acceso a los archivos relevantes:**
  - `src/predict/Dockerfile` — imagen de la API de predicción (TensorFlow + FastAPI)
  - `src/load/Dockerfile` — imagen del frontend (React + Vite + Nginx)
  - `src/predict/main.py` — punto de entrada de la API
  - `src/predict/requirements.txt` — dependencias Python de la API
  - `scripts/evaluation/model_prd_colab.keras` — modelo en producción
- **Variables de entorno:**
  | Variable | Alcance | Descripción |
  |---|---|---|
  | `VITE_URL_EP` | Local y en línea | URL base del servicio de la API de predicción (p. ej. `http://localhost:7001` en local). Inyectada como argumento de build en el contenedor del frontend. |
  | `CF_TUNNEL_TOKEN` | Solo en línea | Token de autenticación del túnel Cloudflare. Permite exponer el servicio bajo el subdominio [realwaste.sierrainnovate.com](https://realwaste.sierrainnovate.com). |

---

## Documentación del despliegue

### Instrucciones de instalación

#### 1. Instalar Docker

- **Windows / macOS:** Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/). Durante la instalación, asegurarse de habilitar la integración con WSL 2 (Windows).
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get update
  sudo apt-get install -y docker.io docker-compose-plugin
  sudo systemctl enable --now docker
  sudo usermod -aG docker $USER   # requiere cerrar sesión y volver a entrar
  ```
- Verificar la instalación:
  ```bash
  docker --version
  docker compose version
  ```

#### 2. Clonar el repositorio y ubicar los archivos del modelo

Asegurarse de que el archivo del modelo en producción se encuentre en:
```
scripts/evaluation/model_prd_colab.keras
```

#### 3. Construir y levantar los servicios (entorno local)

Desde la raíz del repositorio:
```bash
docker compose -f src/docker-compose-local.yml up --build
```

Para el despliegue en línea (servidor hosting), configurar primero las variables de entorno y luego ejecutar:
```bash
docker compose -f src/docker-compose-online.yml up --build -d
```

#### 4. Acceder a la documentación de la API (opcional)
- En local: [http://localhost:7001/docs](http://localhost:7001/docs)
- En línea: [https://realwaste.sierrainnovate.com/api/docs](https://realwaste.sierrainnovate.com/api/docs)

---

### Instrucciones de configuración

#### Cambiar el modelo desplegado

1. Colocar el nuevo archivo `.keras` en:
   ```
   scripts/evaluation/model_{name}.keras
   ```
2. Editar la **línea 9** de `src/predict/Dockerfile`, reemplazando la instrucción `COPY` del modelo:
   ```dockerfile
   COPY scripts/evaluation/model_{name}.keras /app/model/model_prd_colab.keras
   ```
3. Reconstruir los contenedores:
   ```bash
   docker compose -f src/docker-compose-local.yml up --build
   ```

#### Variables de entorno para despliegue en línea

Crear un archivo `.env` en la raíz del repositorio (o exportar las variables en el entorno del servidor) con el siguiente contenido:
```env
VITE_URL_EP=https://realwaste.sierrainnovate.com/api   # ajustar según configuración del túnel
CF_TUNNEL_TOKEN=<token_del_tunel_cloudflare>
```

---

### Instrucciones de uso

- **Entorno local:** Abrir el navegador en [http://localhost:7000/](http://localhost:7000/)
- **Entorno en línea:** Acceder a [https://realwaste.sierrainnovate.com/](https://realwaste.sierrainnovate.com/)

Al ingresar, si la API aún no está lista, se mostrará una página de carga en lugar de la interfaz de clasificación. Esperar a que desaparezca antes de continuar.

Una vez cargada la aplicación, el usuario puede:
1. **Subir una imagen** del residuo desde su dispositivo, o
2. **Usar la cámara** para capturar una foto directamente.

Para obtener mejores resultados en la clasificación, se recomienda que la imagen cumpla con las siguientes condiciones:
- Buena iluminación, sin sombras pronunciadas
- Imagen enfocada y nítida
- Fondo blanco o neutro
- El residuo debe ocupar la mayor parte del encuadre

---

### Instrucciones de mantenimiento

Para reportar errores, solicitar actualizaciones del modelo o realizar cualquier ajuste en el sistema, abrir un ticket enviando un correo a:

**klealp@unal.edu.co**

El responsable del sistema realizará las revisiones y los ajustes correspondientes.
