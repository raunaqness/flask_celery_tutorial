import time
from flask import Flask, render_template
from celery import Celery

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

# celery config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.broker_url = app.config['CELERY_BROKER_URL']
celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# route that will show will simply render a HTML template
@app.route("/tasks")
def tasks():
    return render_template("tasks.html")

# route that will execute a long running task
@app.route("/long_running_task")
def long_running_task():
    # time in seconds 
    time_to_wait = 15
    
    print(f"This task will take {time_to_wait} seconds to complete...")
    time.sleep(time_to_wait)
    
    return f"<p>The task completed in {time_to_wait} seconds!"