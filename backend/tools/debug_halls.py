import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def inspect_db():
    load_dotenv("C:/Users/GNTC/Desktop/ETickets-master/backend/.env")
    url = os.getenv("DATABASE_URL")
    if not url:
        print("No DATABASE_URL found in backend/.env")
        return

    engine = create_engine(url)
    with engine.connect() as conn:
        print("\n--- CINEMAS ---")
        cinemas = conn.execute(text("SELECT id, name, deleted FROM cinemas")).fetchall()
        for c in cinemas:
            print(f"ID: {c[0]}, Name: {c[1]}, Deleted: {c[2]}")

        print("\n--- HALLS ---")
        halls = conn.execute(text("SELECT id, name, cinema_id, deleted FROM halls")).fetchall()
        for h in halls:
            print(f"ID: {h[0]}, Name: {h[1]}, Cinema ID: {h[2]}, Deleted: {h[3]}")

        print("\n--- MOVIES ---")
        movies = conn.execute(text("SELECT id, title, cinema_id, deleted FROM movies")).fetchall()
        for m in movies:
            print(f"ID: {m[0]}, Title: {m[1]}, Cinema ID: {m[2]}, Deleted: {m[3]}")

if __name__ == "__main__":
    inspect_db()
