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
1. This is the **best time to remove or replace** anything from the base project, for example we can remove `Celery` + `Beats` if we are not going to perform any Task nor cronjob or we can replace the DB settings to match any other engine and so on. The following are common things you might want to delete (but don't forget to remove all the references as well):
    - .github/ (to remove github actions)
    - Celery + Beats
        - docker/docker-compose.local.yaml
        - django_base/
            - celery.py
            - settings/base.py
            - extra_settings/celery.py
        - pyproject.toml (Project dependencies)
    - Redis
        - docker/docker-compose.local.yaml
        - django_base/
            - settings/base.py
        - pyproject.toml (Project dependencies)


1. Edit the README.md file to match your final initial setup
1. Create the project's git to have a clean git history:
    ```sh
    git init
    pre-commit install # install pre-commit hooks
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
    task build
    ```
    ```bash
    # Command to start Docker containers
    task start
    ```
    ```bash
    # Command to stop Docker containers
    task stop
    ```
    ```bash
    # Command to down Docker containers
    task down
    ```

 - **Django management commands:**

    Since we are defining our own custom `apps` directory we needed to create a custom startapp task

    First, create an `apps` directory if it does not exist yet and then:

    ```bash
    # Command to create a Django application
    task startapp -- <app_name>
    ```

    Aditional **required** steps:

    1. Modify the "example_app" `apps.py` to match the current route:

        ```python
        # at apps/example_app/apps.py
        class ExampleAppConfig(AppConfig):
            default_auto_field = 'django.db.models.BigAutoField'
            name = 'apps.example_app' # Prepend the "apps." part
        ```

    1. Add the new "example_app" to the settings:

        ```python
        # at django_base/settings/base.py
        LOCAL_APPS = [
            "apps.example_app"
        ]
        ```

    _For everything else use:_
    ```bash
    # Command to run manage.py commands
    task manage -- [command]

    # Example Command to create a super user:
    # task manage -- createsuperuser

    # Example: Command to create migrations for a specific app
    # task manage -- makemigrations myapp
    ```

## Docs generation
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)

## Cache
- [Redis](https://github.com/redis/hiredis-py)

## Tasks
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Django Celery Beats](https://django-celery-beat.readthedocs.io/en/latest/)

**NOTE:** Remember to run the initial migrations if you are going to use `Django Celery Beats` before starting the `beats` process as it uses its own table in the DB.

## Project Structure
- **Key project files and directories:**
  - **docker/**: Defines the Docker setup.
  - **nginx/**: Defines the Nginx setup.
  - **Taskfile.yml**: Contains task definitions for automation.
  - **django_base/**: Django project directory.
  - **.env**: Environment variables configuration file.
  - **pyproject.toml, poetry.lock**: Poetry files for dependency management.
  - **pre-commit-config.yaml**: pre-commit configuration file.

## Notes
- **Environment configuration:** Ensure `.env` file settings are accurate before running commands.
- Once your project has a domain ensure to add it to:
    - `CSRF_TRUSTED_ORIGINS` at `django_base/settings/prod`
    - `DJANGO_ALLOWED_HOSTS` at production's `.env`
    - `nginx/nginx.conf`
