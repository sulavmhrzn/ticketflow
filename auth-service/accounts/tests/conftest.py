import pytest


@pytest.fixture(autouse=True)
def celery_eager_mode(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
