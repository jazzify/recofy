# Django Project with PostgreSQL, Docker, Poetry, and Task

This is a sample project that utilizes Django with PostgreSQL as the database,
Docker for containerization, Poetry for dependency management, and Task for task automation.

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Task](https://taskfile.dev/)
- pre-commit (`pip install pre-commit`)

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/path/django_base.git
    cd django_base
    ```

2. Create a `.env` file:
    ```
    # Django settings
    SECRET_KEY=tu_clave_secreta
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]

    # PostgreSQL settings
    POSTGRES_DB=mydatabase
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    # Database URL
    DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
    ```

### Usage

- **Building and starting Docker containers:**
    ```bash
    # Command to build Docker containers
    task-[dev|prod] build
    ```
    ```bash
    # Command to start Docker containers
    task-[dev|prod] start
    ```

- **Django management commands:**
    ```bash
    # Command to apply database migrations
    task-[dev|prod] migrate
    ```
    ```bash
    # Command to create a Django superuser
    task-[dev|prod] createsuperuser
    ```
    ```bash
    # Command to collect static files
    task-[dev|prod] collectstatic
    ```

- **Testing and development:**
    ```bash
    # Command to run tests
    task-[dev|prod] test
    ```
    ```bash
    # Command to access the Django shell
    task-[dev|prod] shell
    ```
    ```bash
    # Example: Command to create migrations for a specific app
    task-[dev|prod] manage -- cmd="makemigrations myapp"

    # Example: Command to start a new Django app
    task-[dev|prod] manage -- cmd="startapp newapp"
    ```

### Project Structure

- **Key project files and directories:**
  - **Dockerfile**: Defines the Docker container setup.
  - **Taskfile.yml**: Contains task definitions for automation.
  - **manage.py**: Django management script.
  - **myproject/**: Django project directory.
  - **.env**: Environment variables configuration file.
  - **docker-compose.yml**: Docker Compose configuration.
  - **pyproject.toml, poetry.lock**: Poetry files for dependency management.
  - **tasks.py**: Task-related Python script.
  - **.gitignore**: Git ignore file to exclude certain files from version control.

### Notes

- **Environment configuration:** Ensure `.env` file settings are accurate before running commands.
- **Dependencies:** Uses `django-environ` for managing environment variables and `psycopg2` for PostgreSQL during development.
- **Contributions:** Contributions are welcome! Please submit pull requests or open issues for suggestions or improvements.
