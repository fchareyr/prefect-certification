import random
from datetime import timedelta

import httpx
from prefect import flow, get_run_logger, runtime, task
from prefect.artifacts import create_markdown_artifact
from prefect.cache_policies import INPUTS
from prefect.tasks import exponential_backoff
from prefect.variables import Variable


@task(cache_policy=INPUTS, cache_expiration=timedelta(minutes=1))
def fetch_weather(latitude: float = 25.8, longitude: float = 25.0) -> float:
    if not isinstance(base_url := Variable.get("open_meteo_url"), str):
        raise ValueError("Missing open_meteo_url variable")

    response = httpx.get(
        url=base_url,
        params=dict(
            latitude=latitude,
            longitude=longitude,
            current="temperature_2m",
        ),
    )

    temperature = response.json()["current"]["temperature_2m"]

    return temperature


@task(retries=5, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def save_temperature(temperature: float):
    if random.randint(0, 2) > 1:
        raise Exception("Random failure")

    with open("temperature.csv", "w+") as f:
        f.write(f"{temperature}\n")


@flow
def pipeline():
    logger = get_run_logger()
    logger.info(f"Running flow {runtime.flow_run.name}")

    temperature = fetch_weather()
    save_temperature(temperature=temperature)

    create_markdown_artifact(
        markdown=f"""
# Weather data
Temperature: {temperature}
        """,
        key="weather",
        description="Weather data",
    )

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab104/main.py:pipeline",
    ).deploy(
        name="deploy-4-managed",
        work_pool_name="managed"
    )

    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab104/main.py:pipeline",
    ).deploy(
        name="deploy-5-local",
        work_pool_name="local"
    )

    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab104/main.py:pipeline",
    ).deploy(
        name="deploy-6-docker",
        work_pool_name="docker"
    )