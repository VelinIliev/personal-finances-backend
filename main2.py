from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(1, "Title One", "Author One", "some description", 5, 2009),
    Book(2, "Title Two", "Author One", "some description", 3, 2010),
    Book(3, "Title Three", "Author One", "some description", 4, 2020),
    Book(4, "Title Four", "Author Four", "some description", 2, 2002),
    Book(5, "Title Five", "Author Five", "some description", 1, 1977),
]


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=0, le=5)
    published_date: int = Field(ge=1500)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'New book',
                'author': 'New author',
                'description': 'some description',
                'rating': 5,
                'published_date': 2024
            }
        }


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            found_book = book
            return found_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/" , status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(ge=0, le=5)):
    found_books = []
    for book in BOOKS:
        if book.rating == rating:
            found_books.append(book)
    return found_books


@app.post("/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_last_id(new_book))
    return new_book


@app.put("/books/edit/{book_id}", status_code=status.HTTP_201_CREATED)
async def edit_book(book_request: BookRequest, book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            book.published_date = book_request.published_date
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
    raise HTTPException(status_code=404, detail="Book not found")


def find_last_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
