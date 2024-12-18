from prefect import flow
from prefect.flow_runs import pause_flow_run
from prefect.logging import get_run_logger

from prefect.input import RunInput

class UserInput(RunInput):
    name: str
    age: int

@flow
def greet_user():
    logger = get_run_logger()

    user = pause_flow_run(wait_for_input=UserInput)

    if user.age >= 18:
        logger.info(f"Hello, {user.name}! You are an adult.")
    else:
        logger.info(f"Hello, {user.name}! You are a minor.")

if __name__ == '__main__':
    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab106/main.py:greet_user",
    ).deploy(
        name="deploy-6",
        work_pool_name="managed"
    )