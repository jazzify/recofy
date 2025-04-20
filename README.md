# Recofy (EDUCATIONAL USE ONLY)

## About
Recofy is a Django-based application that integrates with the Spotify API to retrieve, store, and manage music data including artists, albums, and tracks. It provides a RESTful API for accessing this data.

## License

This project is licensed under the MIT License (Educational Use Only) - see the [LICENSE](LICENSE) file for details.

### Built with:
- Docker + Compose - For containerization and orchestration
- Nginx + Gunicorn - For web server and WSGI handling
- Redis + Celery + Beats - For caching and task management
- PostgreSQL - For database storage
- Docs (Open API 3.0) - For API documentation
- Debug Toolbar - For development debugging
- Spotify API Integration - For music data retrieval

## Requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Task](https://taskfile.dev/)
- pre-commit (`pip install pre-commit`)

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/jazzify/recofy.git [project_dir_name]
    cd [project_dir_name]
    ```

1. Create a `.env` file just like `.env.example` with your custom data, including your Spotify API credentials (client ID and secret). If you add something to your `.env` file, also keep `.env.example` updated with dummy values for key reference.

1. Run the following command to build and start the containers:
    ```sh
    task compose-up -- -d
    ```

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

## Developer Guides
- [Django ORM Query Optimization](apps/recofy/db.md) - Learn techniques to optimize database queries, reduce query count, and improve execution time with practical examples using Django's bulk operations.

## Cache
- [Redis](https://github.com/redis/hiredis-py)

## Tasks
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Django Celery Beats](https://django-celery-beat.readthedocs.io/en/latest/)

**NOTE:** Remember to run the initial migrations if you are going to use `Django Celery Beats` before starting the `beats` process as it uses its own table in the DB.

## Project Structure
- **Key project files and directories:**
  - **docker/**: Defines the Docker setup for local and production environments.
  - **nginx/**: Defines the Nginx setup for serving the application.
  - **Taskfile.yml**: Contains task definitions for automation.
  - **django_base/**: Django project directory with settings and configuration.
  - **apps/**: Contains the application modules:
    - **api/**: API configuration and routing.
    - **core/**: Core models and functionality.
    - **recofy/**: Main application with Spotify integration, models, and services.
  - **.env**: Environment variables configuration file (including Spotify API credentials).
  - **pyproject.toml, poetry.lock**: Poetry files for dependency management.
  - **pre-commit-config.yaml**: pre-commit configuration file.

## Notes
- **Environment configuration:** Ensure `.env` file settings are accurate before running commands, including Spotify API credentials.
- **Spotify API:** You need to register your application with Spotify Developer Dashboard to get client ID and secret.
- Once your project has a domain ensure to add it to:
    - `CSRF_TRUSTED_ORIGINS` at `django_base/settings/prod`
    - `DJANGO_ALLOWED_HOSTS` at production's `.env`
    - `nginx/nginx.conf`
