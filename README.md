# tech_challenge_ml_engineer
 This will be my main project in my Machine Learning Engineering Master's. I will refine my communication skills to handle more complex questions and work on a real case for my portfolio. At the end of each of the five phases, I will complete a full stage of this project.

# Code Structure

vitivinicultura-api/
│
├── .github/                      # Configurações de CI/CD para GitHub Actions
│   └── workflows/
│       └── deploy.yml            # Workflow para automação de deploy
│
├── api/                          # Código principal da API
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada da aplicação
│   ├── core/                     # Componentes centrais
│   │   ├── __init__.py
│   │   ├── config.py             # Configurações da aplicação
│   │   ├── security.py           # Autenticação JWT
│   │   └── logging.py            # Configuração de logs
│   │
│   ├── models/                   # Modelos de dados/schemas
│   │   ├── __init__.py
│   │   ├── producao.py
│   │   ├── processamento.py
│   │   ├── comercializacao.py
│   │   ├── importacao.py
│   │   └── exportacao.py
│   │
│   ├── services/                 # Lógica de negócio/serviços
│   │   ├── __init__.py
│   │   ├── scraper.py            # Serviço para raspagem de dados da Embrapa
│   │   └── data_processor.py     # Processamento de dados
│   │
│   ├── routes/                   # Endpoints da API
│   │   ├── __init__.py
│   │   ├── producao.py
│   │   ├── processamento.py
│   │   ├── comercializacao.py
│   │   ├── importacao.py
│   │   └── exportacao.py
│   │
│   └── utils/                    # Utilitários
│       ├── __init__.py
│       └── helpers.py            # Funções auxiliares
│
├── database/                     # Banco de dados SQLite
│   ├── __init__.py
│   ├── db.py                     # Configuração do SQLite
│   └── models.py                 # Modelos ORM
│
├── data/                         # Diretório para armazenar o arquivo SQLite
│   └── .gitkeep                  # Garante que o diretório seja versionado mesmo vazio
│
├── docs/                         # Documentação
│   ├── architecture.md           # Documentação da arquitetura
│   └── api.md                    # Documentação da API
│
├── tests/                        # Testes automatizados
│   ├── __init__.py
│   ├── test_routes/              # Testes dos endpoints
│   ├── test_services/            # Testes dos serviços
│   └── conftest.py               # Configurações para testes
│
├── .gitignore                    # Arquivos a serem ignorados pelo git
├── Dockerfile                    # Configuração para containerização
├── docker-compose.yml            # Orquestração de containers
├── requirements.txt              # Dependências do projeto
├── README.md                     # Documentação do projeto
└── setup.py                      # Configuração para instalação do pacote

# Detailed Explanation of the Project Structure

## Top-Level Folders

### `.github/`
**Purpose:** Contains configurations for GitHub integration.
- `workflows/deploy.yml`: Defines the CI/CD (Continuous Integration/Continuous Delivery) pipeline that automates testing and deployment of the application when new changes are pushed to the repository.

### `api/`
**Purpose:** Contains all the main code of the API application.
- It's the heart of the project where the API logic is implemented.

### `database/`
**Purpose:** Contains everything related to the SQLite database.
- Responsible for configuration, connection, and database models.

### `data/`
**Purpose:** Directory where the physical SQLite database file will be stored.
- `.gitkeep`: Empty file that ensures Git keeps the empty directory in the repository.

### `docs/`
**Purpose:** Contains project documentation.
- Includes technical documentation, architecture documentation, and usage guides.

### `tests/`
**Purpose:** Contains all automated tests for the project.
- Fundamental to ensure the API works correctly.

## Internal API Structure

### `api/main.py`
**Purpose:** Entry point of the application.
- Defines the main FastAPI or Flask application object and registers routes and middlewares.

### `api/core/`
**Purpose:** Contains core components that serve as the foundation for the entire application.
- `config.py`: Manages application configurations such as environment variables.
- `security.py`: Implements JWT authentication and access control.
- `logging.py`: Configures the application's logging system.

### `api/models/`
**Purpose:** Defines data schemas/models for API input and output validation.
- Each file corresponds to a category of Embrapa data:
  - `producao.py`: Schemas for wine production data.
  - `processamento.py`: Schemas for processing data.
  - `comercializacao.py`: Schemas for commercialization data.
  - `importacao.py`: Schemas for import data.
  - `exportacao.py`: Schemas for export data.

### `api/services/`
**Purpose:** Contains the application's core business logic.
- `scraper.py`: Implements functionality to extract data from the Embrapa website.
- `data_processor.py`: Processes and transforms scraped data into the appropriate format.

### `api/routes/`
**Purpose:** Defines the REST API endpoints.
- Each file corresponds to a different category and defines specific endpoints:
  - `producao.py`: Endpoints for querying production data.
  - `processamento.py`: Endpoints for processing data.
  - `comercializacao.py`: Endpoints for commercialization data.
  - `importacao.py`: Endpoints for import data.
  - `exportacao.py`: Endpoints for export data.

### `api/utils/`
**Purpose:** Contains utility functions that can be used in various parts of the application.
- `helpers.py`: Generic helper functions, such as data formatting, validations, etc.

## Database

### `database/db.py`
**Purpose:** Configures the connection to the SQLite database.
- Defines functions to create connections and manage sessions.

### `database/models.py`
**Purpose:** Defines the ORM (Object-Relational Mapping) models that represent the tables in the database.
- Defines the structure of the tables where data will be stored.

## Configuration Files

### `Dockerfile`
**Purpose:** Defines how to build the Docker image of the application.
- Specifies the environment, dependencies, and how to run the application.

### `docker-compose.yml`
**Purpose:** Defines how the different application services relate to each other.
- Allows starting all necessary components with a single command.

### `requirements.txt`
**Purpose:** Lists all Python dependencies required for the project.
- Used to install packages with pip: `pip install -r requirements.txt`.

### `README.md`
**Purpose:** Main project documentation.
- Contains installation instructions, configuration, usage, and other important information.

### `setup.py`
**Purpose:** Configures the project as an installable Python package.
- Allows the project to be installed via pip in other environments.

### `.gitignore`
**Purpose:** Specifies which files or directories should be ignored by Git.
- Typically includes temporary files, caches, virtual environments, and credentials.

## Tests

### `tests/conftest.py`
**Purpose:** Contains configurations and fixtures for tests.
- Defines shared resources that can be used in multiple tests.

### `tests/test_routes/`
**Purpose:** Contains tests for the API endpoints.
- Verifies that routes respond correctly to requests.

### `tests/test_services/`
**Purpose:** Contains tests for services (business logic).
- Verifies that services process data correctly.