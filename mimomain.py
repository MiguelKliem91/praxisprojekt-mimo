# Import aller nötigen Module
from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel, ValidationError
import psycopg2
from sqlalchemy.orm import Session
from datetime import datetime



# Klassen erstellen
class Book(BaseModel):
    ID: int
    Titel: str
    Autor: str
    Erscheinungsjahr: int
    Herausgeber: str
    Seitenanzahl: int
    Preis: float
    Auf_Lager: int

class E_Book(BaseModel):
    ID: int
    Titel: str
    Autor: str
    Erscheinungsjahr: int
    Herausgeber: str
    Seitenanzahl: int
    Preis: float

class Film(BaseModel):
    ID: int
    Titel: str
    Produzent: str
    Erscheinungsjahr: int
    Preis: float
    Auf_Lager: int

# Klassen für die Cafe Datenbank
class Produkt(BaseModel):
    Produkt_ID: int
    Name: str
    Preis: float

class Bestellung(BaseModel):
    Bestell_ID: int
    Produkt_ID: int
    Anzahl: int
    Datum_Uhrzeit: datetime
    
# Connection Buchhaltung
def get_connection_buchhandlung():
    return psycopg2.connect(
        user="postgres",
        password="DataCraft",
        host="localhost",
        database="Buchhandlung"
    )
    
# Connection Café
def get_connection_cafe():
    return psycopg2.connect(
        user="postgres",
        password="DataCraft",
        host="localhost",
        database="Cafe"
    )
    


# App erstellen
app = FastAPI()

# Willkommensseite einrichten
@app.get("/")
def welcome_status():
    return {"nachricht": "Herzlich Willkommen in unserer Bücher Datenbank!"}

# Alle Bücher anzeigen lassen
@app.get("/books")
def get_all_books(connection:Session=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM buch")
    rows = cursor.fetchall()
    print(rows)
    books = []
    for row in rows:
        try:
            book = Book(
                ID=row[0],
                Titel=row[1],
                Autor=row[2],
                Erscheinungsjahr=row[3],
                Herausgeber=row[4],
                Seitenanzahl=row[5],
                Preis=row[6],
                Auf_Lager=row[7]
            )
            books.append(book)
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
    return books

@app.get("/e_books")
def get_all_e_books(connection:Session=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ebook")
    rows = cursor.fetchall()
    e_books = []
    for row in rows:
        try:
            e_book = E_Book(
                ID=row[0],
                Titel=row[1],
                Autor=row[2],
                Erscheinungsjahr=row[3],
                Herausgeber=row[4],
                Seitenanzahl=row[5],
                Preis=row[6]
            )
            e_books.append(e_book)
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
    return e_books


@app.get("/movies")
def get_all_films(connection:Session=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM film")
    rows = cursor.fetchall()
    films = []
    for row in rows:
        try:
            film = Film(
                ID=row[0],
                Titel=row[1],
                Produzent=row[2],
                Erscheinungsjahr=row[3],
                Preis=row[4],
                Auf_Lager=row[5]
            )
            films.append(film)
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
    return films

# Bestimmtes Buch abrufen
@app.get("/books/{book_id}")
def get_book(book_id: int, con:Session = Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM buch WHERE id = %s", (book_id,))
    row = cursor.fetchone()
    con.close()
    
    if row:
        try:
            book = Book.model_validate(dict(zip(Book.model_fields.keys(), row)))
            # book = Book(
            #     ID=row[0],
            #     Titel=row[1],
            #     Autor=row[2],
            #     Erscheinungsjahr=row[3],
            #     Herausgeber=row[4],
            #     Seitenanzahl=row[5],
            #     Preis=row[6],
            #     Auf_Lager=row[7]
            # )
            return book
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
            raise HTTPException(status_code=500, detail="Validation error")
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# Bestimmtes E_Book suchen
@app.get("/e_books/{e_book_id}")
def get_e_book(e_book_id: int, con:Session = Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ebook WHERE id = %s", (e_book_id,))
    row = cursor.fetchone()
    con.close()
    
    if row:
        try:
            e_book = E_Book.model_validate(dict(zip(E_Book.model_fields.keys(), row)))
            # e_book = E_Book(
            #     ID=row[0],
            #     Titel=row[1],
            #     Autor=row[2],
            #     Erscheinungsjahr=row[3],
            #     Herausgeber=row[4],
            #     Seitenanzahl=row[5],
            #     Preis=row[6],
            # )
            return e_book
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
            raise HTTPException(status_code=500, detail="Validation error")
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# Bestimmten Film suchen
@app.get("/movies/{film_id}")
def get_movie(film_id: int, con:Session = Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM film WHERE id = %s", (film_id,))
    row = cursor.fetchone()
    con.close()
    if row:
        try:
            film = Film.parse_obj(dict(zip(Film.model_fields.keys(), row))
            )
            return film
        except ValidationError as e:
            print(f"Validation error for row {row}: {e}")
            raise HTTPException(status_code=500, detail="Validation error")
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# Buch hinzufügen
@app.post("/post_book")
def buch_hinzufuegen(book: Book, con:Session=Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute(
        ("INSERT INTO buch (id, titel, autor, erscheinungsjahr, herausgeber, seitenanzahl, preis, auf_lager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *"),
        (book.ID, book.Titel, book.Autor, book.Erscheinungsjahr, book.Herausgeber, book.Seitenanzahl, book.Preis, book.Auf_Lager)
    )
    new_book = cursor.fetchone()
    con.commit()
    con.close()
    if new_book:
        return Book.parse_obj(dict(zip(Book.model_fields.keys(), new_book)))
    else:
        raise HTTPException(status_code=500, detail="Error while adding book")
    

# E_Book hinzufügen
@app.post("/post_e_book")
def e_book_hinzufuegen(e_book: E_Book, con:Session=Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO ebook (id, titel, autor, erscheinungsjahr, herausgeber, seitenanzahl, preis) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
        (e_book.ID, e_book.Titel, e_book.Autor, e_book.Erscheinungsjahr, e_book.Herausgeber, e_book.Seitenanzahl, e_book.Preis)
    )
    new_e_book = cursor.fetchone()
    con.commit()
    con.close()
    if new_e_book:
        return E_Book.parse_obj(dict(zip(E_Book.model_fields.keys(), new_e_book)))
    else:
        raise HTTPException(status_code=500, detail="Error while adding e_book")

# Buch hinzufügen
@app.post("/post_movie")
def film_hinzufuegen(film: Film, con:Session=Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO film (id, titel, produzent, erscheinungsjahr, preis, auf_lager) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
        (film.ID, film.Titel, film.Produzent, film.Erscheinungsjahr, film.Preis, film.Auf_Lager)
    )
    new_film = cursor.fetchone()
    con.commit()
    con.close()
    if new_film:
        return Film.parse_obj(dict(zip(Film.model_fields.keys(), new_film)))
    else:
        raise HTTPException(status_code=500, detail="Error while adding film")


# Buch ändern
@app.put("/update_book/{book_id}")
def update_book(book_id: int, updated_book: Book, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE buch SET titel = %s, autor = %s, erscheinungsjahr = %s, herausgeber = %s, seitenanzahl = %s, preis = %s, auf_lager = %s WHERE id = %s RETURNING *",
        (updated_book.Titel, updated_book.Autor, updated_book.Erscheinungsjahr, updated_book.Herausgeber, updated_book.Seitenanzahl, updated_book.Preis, updated_book.Auf_Lager, book_id)
    )
    updated_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if updated_row:
        return Book.parse_obj(dict(zip(Book.model_fields.keys(), updated_row)))
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# E_Book ändern
@app.put("/update_e_book/{e_book_id}")
def update_e_book(e_book_id: int, updated_e_book: E_Book, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE ebook SET titel = %s, autor = %s, erscheinungsjahr = %s, herausgeber = %s, seitenanzahl = %s, preis = %s WHERE id = %s RETURNING *",
        (updated_e_book.Titel, updated_e_book.Autor, updated_e_book.Erscheinungsjahr, updated_e_book.Herausgeber, updated_e_book.Seitenanzahl, updated_e_book.Preis, e_book_id)
    )
    updated_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if updated_row:
        return E_Book.parse_obj(dict(zip(E_Book.model_fields.keys(), updated_row)))
    else:
        raise HTTPException(status_code=404, detail="E-Book not found")

# Film ändern        
@app.put("/update_movie/{film_id}")
def update_film(film_id: int, updated_film: Film, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE film SET titel = %s, produzent = %s, erscheinungsjahr = %s, preis = %s, auf_lager = %s WHERE id = %s RETURNING *",
        (updated_film.Titel, updated_film.Produzent, updated_film.Erscheinungsjahr, updated_film.Preis, updated_film.Auf_Lager, film_id)
    )
    updated_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if updated_row:
        return Film.parse_obj(dict(zip(Film.model_fields.keys(), updated_row)))
    else:
        raise HTTPException(status_code=404, detail="Film not found")
        

# Buch löschen
@app.delete("/delete_books/{book_id}")
def delete_book(book_id: int, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM buch WHERE id = %s RETURNING *",
        (book_id,)
    )
    deleted_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if deleted_row:
        return Book.parse_obj(dict(zip(Book.model_fields.keys(), deleted_row)))
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# E_Book löschen
@app.delete("/delete_e_books/{e_book_id}")
def delete_e_book(e_book_id: int, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM ebook WHERE id = %s RETURNING *",
        (e_book_id,)
    )
    deleted_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if deleted_row:
        return E_Book.parse_obj(dict(zip(E_Book.model_fields.keys(), deleted_row)))
    else:
        raise HTTPException(status_code=404, detail="E-Book not found")

# Film löschen    
@app.delete("/delete_movies/{film_id}")
def delete_film(film_id: int, connection=Depends(get_connection_buchhandlung)):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM film WHERE id = %s RETURNING *",
        (film_id,)
    )
    deleted_row = cursor.fetchone()
    connection.commit()
    connection.close()
    if deleted_row:
        return Film.parse_obj(dict(zip(Film.model_fields.keys(), deleted_row)))
    else:
        raise HTTPException(status_code=404, detail="Film not found")

# Gesamtmenge auf Lager + Gesamtsumme
@app.get("/inventory")
def get_inventory_sum(con:Session=Depends(get_connection_buchhandlung)):
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT
            (SELECT SUM(auf_lager) FROM buch) +
            (SELECT SUM(auf_lager) FROM film) AS total_quantity,
            (SELECT SUM(preis * auf_lager) FROM buch) +
            (SELECT SUM(preis * auf_lager) FROM film) AS total_value
        """
    )
    ergebnis = cursor.fetchone()
    con.close()
    if ergebnis:
        return{"Gesamtmenge": ergebnis[0], "Gesamtwert": ergebnis[1]}
    else:
        raise HTTPException(status_code=500, detail="Error beim berechnen vom Inventar.")
    




# Cafe Datenbank abfrage --------------------------------------------------------------------------------------------------------




# Alle Produkte abrufen
@app.get("/cafe/products")
def get_all_products(connection:Session=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM produkt")
    rows = cursor.fetchall()
    connection.close()
    if rows:
        products = [Produkt(Produkt_ID=row[0], Name=row[1], Preis=row[2]) for row in rows]
        return products
    else:
        raise HTTPException(status_code=404, detail="No products found")
    
# Alle Bestellungen abrufen
@app.get("/cafe/orders")
def get_all_bestellungen(connection:Session=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bestellung")
    rows = cursor.fetchall()
    connection.close()
    if rows:
        bestellungen = [Bestellung(Bestell_ID=row[0], Produkt_ID=row[1], Anzahl=row[2], Datum_Uhrzeit=row[3]) for row in rows]
        return bestellungen
    else:
        raise HTTPException(status_code=404, detail="No orders found")

# Produkte hinzufügen
@app.post("/cafe/products/post")
def add_product(product: Produkt, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO produkt (Name, Preis)
            VALUES (%s, %s) RETURNING Produkt_ID
            """,
            (product.Name, product.Preis)
        )
        product_id = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return Produkt(Produkt_ID=product_id, Name=product.Name, Preis=product.Preis)
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))
    
# Bestellungen hinzufügen
@app.post("/orders/post")
def add_bestellung(bestellung: Bestellung, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO bestellungen (Produkt_ID, Anzahl, Datum_Uhrzeit)
            VALUES (%s, %s, %s) RETURNING Bestell_ID
            """,
            (bestellung.Produkt_ID, bestellung.Anzahl, bestellung.Datum_Uhrzeit)
        )
        bestell_id = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return Bestellung(Bestell_ID=bestell_id, Produkt_ID=bestellung.Produkt_ID, Anzahl=bestellung.Anzahl, Datum_Uhrzeit=bestellung.Datum_Uhrzeit)
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))
    
# Einträge aktualisieren/ändern
@app.put("/cafe/products/{produkt_id}")
def update_product(produkt_id: int, updated_product: Produkt, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            UPDATE produkt
            SET Name = %s, Preis = %s
            WHERE Produkt_ID = %s
            """,
            (updated_product.Name, updated_product.Preis, produkt_id)
        )
        connection.commit()
        connection.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/cafe/orders/{bestell_id}")
def update_bestellung(bestell_id: int, updated_bestellung: Bestellung, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            UPDATE bestellungen
            SET Produkt_ID = %s, Anzahl = %s, Datum_Uhrzeit = %s
            WHERE Bestell_ID = %s
            """,
            (updated_bestellung.Produkt_ID, updated_bestellung.Anzahl, updated_bestellung.Datum_Uhrzeit, bestell_id)
        )
        connection.commit()
        connection.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated_bestellung
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))

# Löschen von Einträgen
@app.delete("/cafe/products/{produkt_id}")
def delete_product(produkt_id: int, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM produkt WHERE Produkt_ID = %s",
            (produkt_id,)
        )
        connection.commit()
        connection.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cafe/orders/{bestell_id}")
def delete_bestellung(bestell_id: int, connection=Depends(get_connection_cafe)):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM bestellungen WHERE Bestell_ID = %s",
            (bestell_id,)
        )
        connection.commit()
        connection.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"detail": "Order deleted successfully"}
    except Exception as e:
        connection.rollback()
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))

# Server starten und neuladen
if __name__ == "__main__":
    uvicorn.run("mimomain:app",
                reload=True)