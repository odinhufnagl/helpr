from celery import Celery


celeryy = Celery('celery_test', broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0")

@celeryy.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    import time
    task = add.delay(1, 2)
    while not task.ready():
        print(task.state)
        time.sleep(1)
    print(task.get())
