from typing import List, Optional

import databases
import sqlalchemy
from fastapi import FastAPI

import ormar



app = FastAPI()

user_name_db = 'surglin'
password_db = 'Nusha230399'
db_name = 'test_db'

metadata = sqlalchemy.MetaData()
database = databases.Database(f"postgresql://{user_name_db}:{password_db}@localhost/{db_name}")
app.state.database = database

engine = sqlalchemy.create_engine(f"postgresql://{user_name_db}:{password_db}@localhost/{db_name}")
#metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)

class Item(ormar.Model):
    class Meta:
        tablename = 'items'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    category: Optional[Category] = ormar.ForeignKey(Category, nullable=True)

metadata.create_all(engine)

@app.get("/items/", response_model=List[Item])
async def get_items():
    items = await Item.objects.select_related('category').all()
    return items


@app.post("/items/", response_model= Item)
async def create_item(item: Item):
    await item.save()
    return item


@app.post("/categories/", response_model=Category)
async def create_category(category: Category):
    await category.save()
    return category


@app.put("/items/{item_id}")
async def get_item(item_id: int, item: Item):
    item_db = await Item.objects.get(pk=item_id)
    return await item_db.update(**item.dict())


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, item: Item = None):
    if item:
        return {"deleted_rows": await item.delete()}
    item_db = await Item.objects.get(pk=item_id)
    return {"deleted_rows": await item_db.delete()}