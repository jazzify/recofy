# Recofy (EDUCATIONAL USE ONLY)

## License

This project is licensed under the MIT License (Educational Use Only) - see the [LICENSE](LICENSE) file for details.


### Built with:
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

## Taskfile usage
The tasks defined in the Taskfile are executed within a Docker container, which has a volume mounted to the host PC. This volume specifically includes the application's codebase, allowing for a seamless integration between the development environment on the host and the containerized tasks.

Here's how it works:

1. Code Synchronization: The mounted volume in the docker/docker-compose.yaml>web ensures that the code inside the container is the same as on the host machine. Any changes made to the code on the host are immediately reflected within the container. This is crucial for development workflows, where frequent changes to the codebase are tested and iterated upon.

1. Docker Compose and Django Operations: The tasks typically involve operations such as starting, stopping, or managing services using Docker Compose, as well as running commands related to Django. Since these tasks rely on the codebase, the volume ensures they operate on the latest version of the code, regardless of where the task is run.

1. Host and Container Interaction: While the tasks are executed in an isolated container environment, the mounted volume enables these tasks to access and manipulate the code on the host machine. This setup is particularly useful for tasks that need to interact closely with the host's file system or leverage host-specific configurations.

Run `task --list` to see a full list of available tasks with their description.

- **Common docker compose commands**
    ```bash
    # build the containers without cache
    task compose-build -- --no-cache
    ```
    ```bash
    # start the containers in detached mode
    task compose-up -- -d
    ```
    ```bash
    # stop the containers
    task compose-stop
    ```
    ```bash
    # down the containers
    task compose-down
    ```

- **Common manage.py commands**
    ```bash
    # create a super user
    task manage-createsuperuser
    ```
    ```bash
    # make migrations for a specific app
    task manage-makemigrations -- <app_name>
    ```
    ```bash
    # migrate a specific db
    task manage-migrate -- --database=<db_name>
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
