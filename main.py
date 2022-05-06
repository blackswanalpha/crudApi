# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import uvicorn
from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def index():
    return {"hey": {"name": "Tony"}}


@app.get('/about')
def about():
    return {'data': {'about page'}}


app.get('/blog')


def blog(limit=10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog/create')
def create_blog(request: Blog):
    return {'data': f"Blog is created with title as {request.title}"}


# if __name__ == " __main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
