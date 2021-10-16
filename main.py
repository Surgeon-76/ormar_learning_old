from typing import Optional, Union, List

import databases
import sqlalchemy

import ormar


user_name_db = 'surglin'
password_db = 'Nusha230399'
db_name = 'test_db_old'

database = databases.Database(f"postgresql://{user_name_db}:{password_db}@localhost/{db_name}")
metadata = sqlalchemy.MetaData()


class Author(ormar.Model):
    class Meta:
        tablename = "authors"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(max_length=80)
    last_name: str = ormar.String(max_length=80)


class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=40)


class Post(ormar.Model):
    class Meta:
        tablename = "posts"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=200)
    categories: Optional[List[Category]] = ormar.ManyToMany(Category)
    author: Optional[Author] = ormar.ForeignKey(Author)


async def guido():
    return await Author.objects.create(first_name="Guido", last_name="Van Rossum")
post = await Post.objects.create(title="Hello, M2M", author=guido)
news = await Category.objects.create(name="News")

