from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

from app.routers.cinemas import router as cinemas_router
from app.routers.movies import router as movies_router
from app.routers.halls import router as halls_router
from app.routers.movie_times import router as movie_times_router
from app.routers.seating import router as seating_router
from app.routers.tickets import router as tickets_router
#from app.routers.events import router as events_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.compat_dotnet import router as compat_dotnet_router
from app.routers import auth
from app.routers.photos import router as photos_router
from app.routers.reviews import router as reviews_router
from app.routers.events import router as events_router
from app.routers.actors import router as actors_router



app = FastAPI(title="ETickets API")

# ✅ Static assets (photos, default images, etj)
BASE_DIR = Path(__file__).resolve().parent.parent  # -> backend/
ASSETS_DIR = BASE_DIR / "assets"
UPLOAD_DIR = BASE_DIR / "uploads"

app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# ✅ Routers
app.include_router(photos_router)
app.include_router(cinemas_router)
app.include_router(movies_router)
app.include_router(halls_router)
app.include_router(movie_times_router)
app.include_router(seating_router)
app.include_router(tickets_router)
app.include_router(events_router)
app.include_router(compat_dotnet_router)
app.include_router(auth.router)
app.include_router(reviews_router)
app.include_router(actors_router)

# ✅ Health checks
@app.get("/")
def root():
    return {"message": "Backend ETickets po funksionon 🚀"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
    return {"db": "ok", "result": result}

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_ORIGIN,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
