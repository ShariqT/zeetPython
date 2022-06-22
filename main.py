from flask import Flask, render_template, request
from datetime import datetime
from distutils.util import strtobool
app = Flask(__name__)

def generate_todos():
    return [{
        "ID": 1,
        "Title": "Make example app on Zeet",
        "Finished": False,
        "Posted": datetime.now()
    },{
        "ID": 2,
        "Title": "Write up experience",
        "Finished": False,
        "Posted": datetime.now()
    },{
        "ID": 3,
        "Title": "Profit???",
        "Finished": False,
        "Posted": datetime.now()
    }]

def searchTodos(todoId, todos):
    for idx, todo in enumerate(todos):
        if todoId == todo["ID"]:
            return (todo, idx)
    return None


def createNewTodo(title, status, ID):
    newTodo = {"Title":title, "Finished": status}
    newTodo["Posted"] = datetime.now()
    newTodo["ID"] = ID
    return newTodo



masterTodoList = generate_todos()

@app.route('/')
def index():
    return render_template("index.html", todos=masterTodoList)

@app.route('/update', methods=['POST'])
def updateTodo():
    selectedId = int(request.form["ID"])
    newStatus = bool(strtobool(request.form["Finished"]))
    print(newStatus)
    print(selectedId)
    selectedTodo, selectedTodoIndex = searchTodos(selectedId, masterTodoList)
    selectedTodo["Finished"] = newStatus
    masterTodoList[selectedTodoIndex] = selectedTodo
    data = {}
    data["todo"] = selectedTodo
    data["action"] = f"Changed {selectedTodo['Title']} status to {newStatus}"
    return render_template("status.html", data=data)

@app.route("/delete", methods=["POST"])
def deleteTodo():
    selectedId = int(request.form["ID"])
    todoToDelete, deleteIndex = searchTodos(selectedId, masterTodoList)
    del masterTodoList[deleteIndex]
    data = {}
    data['todo'] = todoToDelete
    data['action'] = f"Deleted {todoToDelete['Title']} from list"
    return render_template("status.html", data=data)

@app.route("/add", methods=['GET', 'POST'])
def addTodo():
    if request.method == 'GET':
        return render_template("add.html")
    if request.method == 'POST':
        title = request.form["Title"]
        newTodo = createNewTodo(title, False, len(masterTodoList) + 1)
        masterTodoList.append(newTodo)
        data = {}
        data['todo'] = newTodo
        data['action'] = f"Added {newTodo['Title']} to list"
        return render_template("status.html", data=data)
    


app.run()