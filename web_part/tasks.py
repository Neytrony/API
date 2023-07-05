from djangoProject.celery import app
import time

@app.task
def update_info(filename):
    time.sleep(100)
    pass