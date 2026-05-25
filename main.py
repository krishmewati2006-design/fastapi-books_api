from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from database import get_db
from models import Book as BookModel

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/books", response_model=list[Book])
async def return_books(db = Depends(get_db)):
    return db.query(BookModel).all()

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id:int, db = Depends(get_db)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/books", response_model=Book)
async def create_book(book: Book, db = Depends(get_db)):
    add_book = BookModel(id=book.id, title=book.title, author=book.author, published_year=book.published_year)
    db.add(add_book)
    db.commit()
    db.refresh(add_book)
    return add_book

@app.delete("/books/{book_id}")
async def delete_book(book_id:int, db = Depends(get_db)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"Message": f"Book With ID {book_id} Has Been Deleted."}

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id:int, book:Book, db = Depends(get_db)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = book.title
    item.author = book.author
    item.published_year = book.published_year
    db.commit()
    db.refresh(item)
    return item