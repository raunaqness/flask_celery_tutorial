import time
from flask import Flask, render_template

# importing function to get celery app instance
from celery_utils import get_celery_app_instance

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

# celery app instance
celery = get_celery_app_instance(app)

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

# celery tasks
@celery.task
def sending_email_with_celery():
    print("Executing Long running task : Sending email with celery...")
    time.sleep(15)
    print("Task complete!")

# route to trigger celery task
@app.route("/long_running_task_celery")
def long_running_task_celery():
    # function.delay() is used to trigger function as celery task
    sending_email_with_celery.delay()
    return f"Long running task trigged with Celery! Check terminal to see the logs..."
    