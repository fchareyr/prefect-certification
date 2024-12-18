from prefect import task, flow

@task
def add(a: int, b: int) -> int:
    return a + b

@flow
def make_add():
    add(2, 3)

@flow
def make_operation():
    make_add()

if __name__ == '__main__':
    flow.from_source(
        source="https://github.com/fchareyr/prefect-certification.git",
        entrypoint="lab105/main.py:make_operation",
    ).deploy(
        name="deploy-5",
        work_pool_name="managed"
    )