from invoke import task
import os

@task
def up(c):
    """Build and start all containers"""
    print("Starting Airflow and Postgres...")
    c.run("docker-compose up -d --build", pty=True)

@task
def down(c):
    """Stop all containers"""
    print("Stopping services...")
    c.run("docker-compose down", pty=True)

@task
def down_volumes(c):
    """Stop and remove containers + volumes"""
    print("Removing containers and volumes...")
    c.run("docker-compose down -v", pty=True)

@task
def restart(c):
    """Restart the Airflow environment"""
    down(c)
    up(c)

@task
def logs(c):
    """Show logs from all containers"""
    c.run("docker-compose logs -f", pty=True)

@task
def shell(c, service="airflow"):
    """Open a shell inside a container (default: airflow)"""
    c.run(f"docker exec -it {service}_webserver bash", pty=True)

@task
def ps(c):
    """List running containers"""
    c.run("docker ps", pty=True)
