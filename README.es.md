# 🚀 Plantilla de Proyecto IA - DevContainer

## 🌍 Descripción del Proyecto

Esta plantilla está diseñada para facilitar el desarrollo de aplicaciones con agente inteligente local utilizando el modelo Qwen3-code, configurado para funcionar como agente a través de la extensión Continue en VSCode.

## 🚀 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- [Visual Studio Code](https://code.visualstudio.com/)
- Extensión **Remote - Containers** en VSCode
👉 [Instalar aquí](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers)
- [Docker Desktop](https://www.docker.com/get-started/)

## 🛠️ Instrucciones de uso

### Paso 1: Crear un nuevo repositorio desde esta plantilla

Puedes crear un nuevo repositorio usando esta plantilla desde la consola con GitHub CLI:

```bash
gh repo create mi-nuevo-repo --template imcrisam/template-devcontainer-qwen --public
```

### Paso 2: Crear volumen para los modelos

```bash
docker volume create models_data
```

Este volumen se debe crear para guardar y reutilizar modelos.

### Paso 3: Establecer permisos (si es necesario)

```bash
chmod +x ./docker-ia-entrypoint.sh
```

## 🧪 Construir el Dev Container

Al abrir el proyecto en VSCode, asegúrate de tener la paleta de comandos abierta presionando `F1`. Luego, ejecuta el comando "Dev Containers: Rebuild and Reopen in Container" para construir y abrir el entorno de desarrollo dentro del contenedor.

- **Rebuild and Reopen in Container**: Construye la infraestructura inicial.
- **Reopen in Container**: Abre el proyecto en el contenedor existente.

Ten en cuenta que la descarga del modelo puede tomar varios minutos. Puedes monitorear el progreso ejecutando el siguiente comando en tu terminal:

```bash
    docker logs -f <nombre_carpeta>_devcontainer-ia-1
```

## 📁 Estructura del Proyecto

```
.
├── .continue/
│   └── config.yaml
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   ├── docker-ia-entrypoint.sh
│   ├── DockerFile
│   └── DockerFile.ia
├── AGENTS.md
└── README.md
```

### Descripción de archivos clave:

- **.continue/config.yaml**: Configuración de la extensión Continue para la conexión con la IA
- **.devcontainer/devcontainer.json**: Configuración del VSCode y DevContainer
- **.devcontainer/docker-compose.yml**: Configuración de servicios, volúmenes del modelo y IA dentro de Docker
- **.devcontainer/docker-ia-entrypoint.sh**: Script para la gestión de descarga y ejecución del modelo
- **.devcontainer/DockerFile**: Imagen base para el proyecto, puede ser modificada para diferentes dependencias
- **.devcontainer/DockerFile.ia**: Imagen específica para la ejecución de la IA
- **AGENTS.md**: Reglas principales del agente de IA

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o realiza un pull request.

## 📄 Licencia

Este proyecto está licenciado bajo la MIT License - mira el archivo [LICENSE](LICENSE) para más detalles.