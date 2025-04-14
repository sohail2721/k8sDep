import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId  # Corrected E402: Move imports to the top

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.taskdb
tasks_collection = db.tasks

# View Tasks
@app.route('/')
def index():
    tasks = list(tasks_collection.find())
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    if task_content:
        tasks_collection.insert_one({'content': task_content, 'completed': False})
    return redirect(url_for('index'))

# Mark Complete
@app.route('/complete/<task_id>')
def complete_task(task_id):
    tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': True}})
    return redirect(url_for('index'))

# Delete Task
@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
