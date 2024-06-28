# Django Rest Framework Base Project

Sample project with:
- Docker + Compose
- Nginx + Gunicorn
- Redis + Celery + Beats
- PostgreSQL
- Docs (Open API 3.0)
- Debug Toolbar

## Requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Task](https://taskfile.dev/)
- pre-commit (`pip install pre-commit`)

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/jazzify/django-base.git [project_dir_name]
    cd [project_dir_name]
    ```
1. Delete the `.git` directory:
    ```sh
    rm -rf .git # for Unix based
    rm -r -fo .git # for Windows (Terminal)
    # or just right click and delete.
    ```
1. Install pre-commit hooks with `pre-commit install`
1. Create the project's git to have a clean git history:
    ```sh
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin <github-uri>
    git push -u --force origin [master|main]
    ```
1. Create a `.env` file just like `.env.example` with your custom data, if you add something to your `.env` file, also and keep `.env.example` updated with dummy values for key reference.

## Usage

- **Docker containers:**
    ```bash
    # Command to build Docker containers
    task build-[local|prod]
    ```
    ```bash
    # Command to start Docker containers
    task start-[local|prod]
    ```
    ```bash
    # Command to stop Docker containers
    task stop-[local|prod]
    ```
    ```bash
    # Command to down Docker containers
    task down-[local|prod]
    ```

 - **Django management commands:**

    _Since we are defining our own custom apps directory we needed to create a custom startapp command:_
    ```bash
    # Command to run manage.py commands
    task startapp-[local|prod] -- <app_name>
    ```
    _For everything else use:_
    ```bash
    # Command to run manage.py commands
    task manage-[local|prod] -- [command]

    # Example Command to create a super user:
    # task manage-local -- createsuperuser

    # Example: Command to create migrations for a specific app
    # task manage-local -- makemigrations myapp
    ```

<!-- - **Testing and development:**
    ```bash
    # Command to run tests
    task test-[local|prod]
    ```
    ```bash
    # Command to access the Django shell
    task shell-[local|prod]
    ``` -->

## Docs generation
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)

## Cache
- [Redis](https://github.com/redis/hiredis-py)

## Tasks
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Django Celery Beats](https://django-celery-beat.readthedocs.io/en/latest/)

## Project Structure

- **Key project files and directories:**
  - **docker/**: Defines the Docker setup.
  - **Taskfile.yml**: Contains task definitions for automation.
  - **django_base/**: Django project directory.
  - **.env**: Environment variables configuration file.
  - **pyproject.toml, poetry.lock**: Poetry files for dependency management.

## Notes
- **Environment configuration:** Ensure `.env` file settings are accurate before running commands.
- Once your project has a domain ensure to add it to:
    - `CSRF_TRUSTED_ORIGINS` at `django_base/settings/prod`
    - `DJANGO_ALLOWED_HOSTS` at production's `.env`
    - `nginx/nginx.conf`
