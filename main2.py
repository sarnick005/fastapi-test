import time
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


"""A Pydantic BaseModel is a class that defines how your data looks like and the validation requirements it needs to pass in order to be valid."""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class FormData(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/about")
async def about():
    return {"message": "about page"}


# Path Parameters
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# Path parameters with types
@app.get("/items2/{item_id}")
async def read_item2(item_id: int):
    return {"item_id": item_id}


# Create an Enum class
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# sending request body


@app.post("/items/")
async def create_item(item: Item):
    return item


# Import Form from fastapi:


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


# form model


@app.post("/register/")
async def register(data: Annotated[FormData, Form()]):
    return data


# file
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):  # bytes
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# handling errors
items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


# JSON Compatible Encoder
fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data


# Create a middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# SQL (Relational) Databases
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
