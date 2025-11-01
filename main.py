from fastapi import FastAPI

app = FastAPI()


all_todos = [{'todo_id': 1, 'sports': 'soccer'},{'todo_id': 2, 'sports': 'basketball'},
                {'todo_id': 3, 'sports': 'baseball'},{'todo_id': 4, 'sports': 'tennis'},
                {'todo_id': 5, 'sports': 'ping pong'},{'todo_id': 6, 'sports': 'chess'},

              ]
@app.get("/")
def index():
    return {"message":"hello world"}

@app.get('/sports/{todo_id}')
async def get_todo(todo_id):
    for todo in all_todos:
        if  todo['todo_id'] == todo_id:
            return {'result': todo}

@app.get('/sports')
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


class Task(BaseModel):
    title: str
    due_at: int
    duration_min: int
    importance:
    type: 
    
@app.post('/tasks')
def post_task(title: str, due_at: int, duration_min, importance:)