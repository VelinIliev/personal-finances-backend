from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'},
]


@app.get("/")
async def root():
    return {"message": "Hello Velko"}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/title/{title}")
async def get_book_by_title(title: str):
    return [x for x in BOOKS if x.get('title').casefold().__contains__(title.casefold())]


@app.get("/books/author/{author}")
async def get_book_by_author(author: str):
    return [x for x in BOOKS if x.get('author').casefold().__contains__(author.casefold())]


@app.get("/books/category/{category}")
async def get_book_by_category(category: str):
    return [x for x in BOOKS if x.get('category').casefold().__contains__(category.casefold())]


@app.get("/books/search/")
async def search_books(category: str = None, author: str = None, title: str = None):
    current_books = BOOKS
    if category:
        current_books = [x for x in current_books if x.get('category').casefold().__contains__(category.casefold())]
    if title:
        current_books = [x for x in current_books if x.get('title').casefold().__contains__(title.casefold())]
    if author:
        current_books = [x for x in current_books if x.get('author').casefold().__contains__(author.casefold())]
    return current_books


@app.post("/books/create")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/edit")
async def edit_book(update_book=Body()):
    for book in range(len(BOOKS)):
        if BOOKS[book].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[book] = update_book
            return update_book
    return "Not Found"


@app.delete("/books/delete/{name}")
async def delete_book(name: str):
    for book in range(len(BOOKS)):
        if BOOKS[book].get('title').casefold() == name.casefold():
            BOOKS.pop(book)
            return "Deleted"
    return "Not Found"
