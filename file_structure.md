Here's a clean, well-organized, and readable Markdown file for your FastAPI project structure and code, with repetitive code removed.

---

# FastAPI Project Structure

This project structure follows a modular approach using FastAPI. The application is split into multiple modules and packages, with well-defined routers and dependencies for managing endpoints.

## Project Structure

```plaintext
.
├── app                      # Main application package
│   ├── __init__.py          # Marks "app" as a Python package
│   ├── main.py              # Entry point for the application
│   ├── dependencies.py      # Shared dependencies across modules
│   ├── routers              # Routers subpackage
│   │   ├── __init__.py      # Makes "routers" a subpackage
│   │   ├── items.py         # "items" module with item-related routes
│   │   └── users.py         # "users" module with user-related routes
│   └── internal             # Internal functionality subpackage
│       ├── __init__.py      # Makes "internal" a subpackage
│       └── admin.py         # "admin" module with admin-related routes
```

## Code Files

### `app/main.py`

The entry point of the application, where FastAPI instance setup and routing are managed.

```python
from fastapi import FastAPI
from .routers import items, users

app = FastAPI()

# Including routers
app.include_router(users.router)
app.include_router(items.router)
```

### `app/dependencies.py`

Contains dependencies for token-based authentication.

```python
from typing import Annotated
from fastapi import Header, HTTPException

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
```

### `app/routers/users.py`

Handles routes related to user operations.

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

### `app/routers/items.py`

Manages item-related routes with token-based dependency.

```python
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
```

### `app/internal/admin.py`

Reserved for admin-related routes.

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/admin/")
async def read_admin_data():
    return {"admin_data": "This is restricted admin data"}
```

---

This structure and organization make the project more modular, with specific functionality split into relevant files and folders, improving readability and maintainability.