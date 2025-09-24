from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Simple CRUD API",
    description="A simple API to manage items with POST, GET, PUT, and DELETE methods.",
    version="0.1.0",
)

# In-memory storage for items (acting as a simple database)
fake_db = []
item_id_counter = 0

# Pydantic model for item data (what the client sends for creation/update)
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Pydantic model for item data including ID (what the API returns)
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# --- API Endpoints will be defined below ---

# POST endpoint to create a new item
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item_create: ItemCreate):
    global item_id_counter
    item_id_counter += 1
    new_item = Item(id=item_id_counter, name=item_create.name, description=item_create.description)
    fake_db.append(new_item)
    return new_item

# GET endpoint to retrieve all items
@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip : skip + limit]

# GET endpoint to retrieve a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item_in_db in fake_db:
        if item_in_db.id == item_id:
            return item_in_db
    raise HTTPException(status_code=404, detail="Item not found")

# PUT endpoint to update an existing item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate):
    for index, item_in_db in enumerate(fake_db):
        if item_in_db.id == item_id:
            updated_item = Item(id=item_id, name=item_update.name, description=item_update.description)
            fake_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE endpoint to delete an item by ID
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    for index, item_in_db in enumerate(fake_db):
        if item_in_db.id == item_id:
            deleted_item_name = fake_db.pop(index).name
            return {"message": f"Item '{deleted_item_name}' with ID {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
