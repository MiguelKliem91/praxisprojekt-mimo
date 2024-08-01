# Import aller nötigen Module
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import json


# Klassen erstellen
class Book(BaseModel):
    Titel: str 
    Autor: str
    Erscheinungsjahr: int
    Herausgeber: str
    Seitenanzahl: int
    ID: int
    Preis: float
    Auf_Lager: int

class E_Book(BaseModel):
    Titel: str
    Autor: str
    Erscheinungsjahr: int
    Herausgeber: str
    Seitenanzahl: int
    ID: int
    Preis: float

class Film(BaseModel):
    Titel: str
    Produzent: str
    Erscheinungsjahr: int
    ID: int
    Preis: float
    Auf_Lager: int


# Daten abrufen

with open("C:/Users/MOE/miniconda3/Data Craft Kurs Material/REST-API/praxisprojekt mimo/e_books.json", "r") as r:
    e_books = json.load(r)
with open("C:/Users/MOE/miniconda3/Data Craft Kurs Material/REST-API/praxisprojekt mimo/buecher.json", "r") as r:
    books = json.load(r)
with open("C:/Users/MOE/miniconda3/Data Craft Kurs Material/REST-API/praxisprojekt mimo/filme.json", "r") as r:
    filme = json.load(r)


# App erstellen
app = FastAPI()

# Willkommensseite einrichten
@app.get("/")
def welcome_status():
    return {"nachricht": "Herzlich Willkommen in unserer Bücher Datenbank!"}

# Alle Bücher anzeigen lassen
@app.get("/books")
def get_all_books():
    return books
@app.get("/e_books")
def get_all_e_books():
    return e_books
@app.get("/movies")
def get_all_filme():
    return filme


# Bestimmten Eintrag abrufen
@app.get("/books/{book_id}")
def get_bestimmtes_buch(book_id: int):
    for book in books:
        if book['ID'] == book_id:
            return book
    else:
        print("Fehler beim wiedergeben des Buches.")

@app.get("/e_books/{e_book_id}")
def get_bestimmtes_e_book(e_book_id: int):
    for e_book in e_books:
        if e_book['ID'] == e_book_id:
            return e_book
    else:
        print("Fehler beim wiedergeben des E-Buches.")

@app.get("/movies/{film_id}")
def get_bestimmten_film(film_id: int):
    for film in filme:
        if film['ID'] == film_id:
            return film
    else:
        print("Fehler beim wiedergeben des Buches.")

# Eintrag hinzufügen
@app.post("/post_book")
def buch_hinzufuegen(book: Book):
    books.append(book)
    return {"nachricht": "Buch erfolgreich hinzugefügt:",
            "Buch": book}

@app.post("/post_e_book")
def e_buch_hinzufuegen(e_book: E_Book):
    books.append(e_book)
    return {"nachricht": "E-Book erfolgreich hinzugefügt:",
            "Buch": e_book}

@app.post("/post_movie")
def film_hinzufuegen(film: Film):
    books.append(film)
    return {"nachricht": "Film erfolgreich hinzugefügt:",
            "Buch": film}


# Einträge updaten/aktualisieren
@app.put("/update_book/{book_id}")
def change_book(book_id: int, updated_book: Book):
    for book in books:
        if book["ID"] == book_id:
            print(book)
            book.update(updated_book.dict())
            return {"nachricht": "Buch erfolgreich aktualisiert:", "Buch": updated_book}

@app.put("/update_e_book/{e_book_id}")
def change_e_book(e_book_id: int, updated_e_book: E_Book):
    for e_book in books:
        if e_book["ID"] == e_book_id:
            print(e_book)
            e_book.update(updated_e_book.dict())
            return {"nachricht": "E-Book erfolgreich aktualisiert:", "E-Book": updated_e_book}
        
@app.put("/update_movie/{film_id}")
def change_movie(film_id: int, updated_film: Film):
    for film in filme:
        if film["ID"] == film_id:
            print(film)
            film.update(updated_film.dict())
            return {"nachricht": "Film erfolgreich aktualisiert:", "Film": updated_film}
        

# Einträge löschen
@app.delete("/delete_books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            del books[i]
            return {"deleted": id}


# Server starten und neuladen
if __name__ == "__main__":
    uvicorn.run("mimomain.json:app",
                reload=True)