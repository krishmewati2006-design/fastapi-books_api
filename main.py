from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict
from database import get_db
from models import Book as BookModel
from models import User as UserModel
from auth import get_password_hash, verify_password, create_access_token, get_current_user
import boto3, os

s3 = boto3.client("s3", region_name="ap-southeast-2")
BUCKET = os.getenv("S3_BUCKET")

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user:UserCreate, db = Depends(get_db)):
    add_user = UserModel(username=user.username, password=get_password_hash(user.password))
    db.add(add_user)
    db.commit()
    return {"Message": "User Created Successfully."}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/books", response_model=list[Book])
async def return_books(db = Depends(get_db), username = Depends(get_current_user)):
    return db.query(BookModel).all()

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id:int, db = Depends(get_db), username = Depends(get_current_user)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/books", response_model=Book)
async def create_book(book: Book, db = Depends(get_db), username = Depends(get_current_user)):
    add_book = BookModel(id=book.id, title=book.title, author=book.author, published_year=book.published_year)
    db.add(add_book)
    db.commit()
    db.refresh(add_book)
    return add_book

@app.delete("/books/{book_id}")
async def delete_book(book_id:int, db = Depends(get_db), username = Depends(get_current_user)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"Message": f"Book With ID {book_id} Has Been Deleted."}

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id:int, book:Book, db = Depends(get_db), username = Depends(get_current_user)):
    item = db.get(BookModel, book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = book.title
    item.author = book.author
    item.published_year = book.published_year
    db.commit()
    db.refresh(item)
    return item

@app.post("/books/{book_id}/cover")
def upload_book_cover(book_id:int, file: UploadFile = File(...), username = Depends(get_current_user)):
    file_key = f"covers/{book_id}/{file.filename}"

    try:
        s3.upload_fileobj(
            file.file,
            BUCKET,
            file_key,
            ExtraArgs={"ContentType": file.content_type}
        )
            
        return {
            "message": "Cover uploaded successfully",
            "book_id": book_id,
            "file_key": file_key,
            "filename": file.filename,
            "bucket": BUCKET
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to S3"
        )
    finally:
        file.close()
    