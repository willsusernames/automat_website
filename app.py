from flask import Flask, render_template, url_for, request, redirect  
# Import Flask and related modules for rendering templates, handling requests, and redirects.

from flask_sqlalchemy import SQLAlchemy  
# Import SQLAlchemy for working with the database.

from datetime import datetime  
# Import datetime to manage timestamps.

import test
# import test file

import subprocess
from subprocess import call
# to run python scripts

app = Flask(__name__)  
# Create an instance of the Flask class for the web app.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
# Configure the SQLite database location as `test.db`. `sqlite:///` specifies a relative path.

db = SQLAlchemy(app)  
# Initialize the database extension with the Flask app.

# Define a model for a to-do list item.
class Todo(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    # Define an integer column for the task ID, which is the primary key.

    content = db.Column(db.String(200), nullable=False)  
    # Define a string column to hold the task content, with a max length of 200 characters. Cannot be null.

    date_created = db.Column(db.DateTime, default=datetime.utcnow)  
    # Define a datetime column that automatically stores the creation timestamp.

    def __repr__(self):  
        return '<Task %r>' % self.id  
    # Define a representation method to return a string representation of the task, useful for debugging.
    

# Define a route for the home page ("/") that supports both GET and POST methods.
@app.route('/', methods=["POST", "GET"])  
def index():
    if request.method == "POST":  
        # If the request is a POST request (form submission), handle adding a new task.
        task_content = request.form['content']  
        # Get the `content` field from the submitted form.

        new_task = Todo(content=task_content)  
        # Create a new `Todo` instance with the submitted content.

        try:
            db.session.add(new_task)  
            # Add the new task to the database session.

            db.session.commit()  
            # Commit the changes to save the task in the database.

            return redirect('/')  
            # Redirect the user back to the home page.

        except:
            return 'Issue adding task'  
            # If an error occurs during the database operation, return an error message.

    else:
        # If the request is a GET request, retrieve all tasks and render the page.
        tasks = Todo.query.order_by(Todo.date_created).all()  
        # Query all tasks from the database, ordered by creation date.

        return render_template('index.html', tasks=tasks)  
        # Render the `index.html` template and pass the tasks as context.

# This is for link downloading
@app.route('/MIT/download')

def push1():
    return call(['python3', 'test.py'])



# This is to lead to the about page
@app.route('/<string:content>')

def about(content):
    return render_template('about1.html')

# This is for row deletion
@app.route('/delete/<int:id>')
# if the user clicks on the delete hyperlink

def delete(id):
# create a function that takes in the id parameter
    task_to_delete = Todo.query.get_or_404(id)
    # where is id in the database?

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this row'
    

if __name__ == "__main__":
    app.run(debug=True)

