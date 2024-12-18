from prefect import task, flow
from prefect.deployments import run_deployment

@task
def add(a: int, b: int) -> int:
    return a + b

@flow
def make_add():
    add(2, 3)

@flow
def make_operation():
    make_add()

@flow
def run_operation():
    run_deployment(
        name="make-operation/deploy-5-nested"
    )

if __name__ == '__main__':
    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab105/main.py:make_operation",
    ).deploy(
        name="deploy-5-nested",
        work_pool_name="managed"
    )

    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab105/main.py:run_operation",
    ).deploy(
        name="deploy-5-run-deployment",
        work_pool_name="managed"
    )