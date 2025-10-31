# 🚀 AI Project Template - DevContainer

## 🌍 Project Description

This template is designed to facilitate the development of intelligent agent applications using the Qwen3-code model, configured to function as an agent via the Continue extension in VSCode.

## 🚀 Prerequisites

Before you start, make sure you have installed:
- [Visual Studio Code](https://code.visualstudio.com/)
- **Remote - Containers** extension in VSCode
👉 [Install here](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers)
- [Docker Desktop](https://www.docker.com/get-started/)

## 🛠️ Usage Instructions

### Step 1: Create a new repository from this template

You can create a new repository using this template from the console with GitHub CLI:

```bash
gh repo create my-new-repo --template imcrisam/template-devcontainer-qwen --public
```

### Step 2: Create volume for models

```bash
docker volume create models_data
```

This volume must be created to store and reuse models.

### Step 3: Set permissions (if needed)

```bash
chmod +x ./docker-ia-entrypoint.sh
```

## 🧪 Build the Dev Container

When opening the project in VSCode, make sure you have the command palette open by pressing `F1`. Then, execute the command "Dev Containers: Rebuild and Reopen in Container" to build and open the development environment within the container.

- **Rebuild and Reopen in Container**: Builds the initial infrastructure.
- **Reopen in Container**: Opens the project in the existing container.

Note that downloading the model may take several minutes. You can monitor the progress by running the following command in your terminal:

```bash
    docker logs -f <folder_name>_devcontainer-ia-1
```

## 📁 Project Structure

```
.
├── .continue/
│   ├── rules/                  # Custom rules for the environment / Reglas personalizadas para el entorno
│   │   └── ...
│   ├── config.yaml             # Configuration for model connection / Configuración de conexión con los modelos
│   └── globalContext.json      # Persistent context across sessions or runs / Contexto persistente entre sesiones o ejecuciones
├── .devcontainer/              # Development environment using Dev Container / Entorno de desarrollo con Dev Container
│   ├── ai/
│   │   ├── DockerFile.ia       # Image for AI environments (llama-server / CUDA) / Imagen para entornos de IA (llama-server / CUDA)
│   │   └── docker-ia-entrypoint.sh  # Entry script for the AI container / Script de entrada del contenedor de IA
│   ├── proxy/                  # Internal proxy server / Servidor proxy interno
│   │   ├── logs/
│   │   ├── Dockerfile.proxy    # Image for the HTTP proxy server / Imagen para el servidor proxy HTTP
│   │   └── server.py           # Intercepts, logs, and can modify requests / Intercepta, genera logs y puede modificar las solicitudes
│   ├── devcontainer.json       # VS Code Dev Container configuration / Configuración de VS Code para el Dev Container
│   ├── docker-compose.yml      # Docker composition for multiple services (AI + Proxy) / Composición Docker para múltiples servicios (IA + Proxy)
│   └── DockerFile              # Main or base image for the general environment / Imagen principal o base del entorno general
├── AGENTS.md                   # Describes implemented intelligent agents / Describe los agentes inteligentes implementados
└── README.md                   # Project introduction and general instructions / Introducción al proyecto e instrucciones generales

```

### Key file descriptions:

- **.continue/config.yaml**: Configuration of the Continue extension for connection with the AI
- **.devcontainer/devcontainer.json**: VSCode and DevContainer configuration
- **.devcontainer/docker-compose.yml**: Services, model volumes and AI configuration within Docker
- **.devcontainer/docker-ia-entrypoint.sh**: Script for model download and execution management
- **.devcontainer/DockerFile**: Base image for the project, can be modified for different dependencies
- **.devcontainer/DockerFile.ia**: Image specifically for AI execution
- **AGENTS.md**: Main rules of the AI agent

## 🤝 Contributions

Contributions are welcome. Please open an issue or make a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


> **Note:**
> The *proxy* container is temporary and used only for debugging purposes.
