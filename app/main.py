from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import engine, Base, get_db
from app import schemas, crud

from .models import Rating

# Création des tables
Base.metadata.create_all(bind=engine)

# Initialisation FastAPI
app = FastAPI(
    title="API Films - Système de recommandation",
    description="API pour gérer des films, notes, tags et liens externes",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Routes pour Movies

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "API de gestion de films",
        "endpoints": {
            "movies": "/movies/",
            "ratings": "/ratings/",
            "tags": "/tags/",
            "links": "/links/",
            "stats": "/stats/"
        }
    }

@app.get("/movies/", response_model=List[schemas.MovieSimple], tags=["Movies"])
def read_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Liste tous les films avec pagination et filtres"""
    movies = crud.MovieCRUD.get_movies(db, skip=skip, limit=limit, search=search, genre=genre)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.MovieDetailed, tags=["Movies"])
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """Détail d'un film avec ses notes, tags et liens"""
    movie = crud.MovieCRUD.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie

@app.post("/movies/", response_model=schemas.MovieSimple, status_code=201, tags=["Movies"])
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    """Crée un nouveau film"""
    return crud.MovieCRUD.create_movie(db, movie)

@app.put("/movies/{movie_id}", response_model=schemas.MovieSimple, tags=["Movies"])
def update_movie(movie_id: int, movie: schemas.MovieBase, db: Session = Depends(get_db)):
    """Met à jour un film"""
    db_movie = crud.MovieCRUD.update_movie(db, movie_id, movie)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return db_movie

@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Supprime un film"""
    deleted = crud.MovieCRUD.delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return {"message": f"Film {movie_id} supprimé avec succès"}



#  Routes pour Ratings 

@app.get("/ratings/", response_model=List[schemas.RatingSimple], tags=["Ratings"])
def read_ratings(
    movie_id: Optional[int] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Liste des notes (filtrable par film ou utilisateur)"""
    if movie_id:
        return crud.RatingCRUD.get_ratings_by_movie(db, movie_id, skip, limit)
    elif user_id:
        return crud.RatingCRUD.get_ratings_by_user(db, user_id, skip, limit)
    else:
        return db.query(models.Rating).offset(skip).limit(limit).all()

@app.post("/ratings/", response_model=schemas.RatingSimple, status_code=201, tags=["Ratings"])
def create_rating(rating: schemas.RatingBase, db: Session = Depends(get_db)):
    """Ajoute une note à un film"""
    # Vérifie que le film existe
    movie = crud.MovieCRUD.get_movie(db, rating.movieId)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    return crud.RatingCRUD.create_rating(db, rating)

@app.put("/ratings/{user_id}/{movie_id}", response_model=schemas.RatingSimple, tags=["Ratings"])
def update_rating(
    user_id: int, 
    movie_id: int, 
    rating: schemas.RatingBase, 
    db: Session = Depends(get_db)
):
    """Met à jour une note"""
    db_rating = crud.RatingCRUD.update_rating(db, user_id, movie_id, rating)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return db_rating

@app.delete("/ratings/{user_id}/{movie_id}", tags=["Ratings"])
def delete_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    """Supprime une note"""
    deleted = crud.RatingCRUD.delete_rating(db, user_id, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return {"message": "Note supprimée avec succès"}

# Routes pour Tags 

@app.get("/tags/", response_model=List[schemas.TagSimple], tags=["Tags"])
def read_tags(
    movie_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Liste des tags (filtrable par film)"""
    if movie_id:
        return crud.TagCRUD.get_tags_by_movie(db, movie_id, skip, limit)
    return db.query(models.Tag).offset(skip).limit(limit).all()

@app.post("/tags/", response_model=schemas.TagSimple, status_code=201, tags=["Tags"])
def create_tag(tag: schemas.TagBase, db: Session = Depends(get_db)):
    """Ajoute un tag à un film"""
    movie = crud.MovieCRUD.get_movie(db, tag.movieId)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    return crud.TagCRUD.create_tag(db, tag)

@app.delete("/tags/{user_id}/{movie_id}/{tag}", tags=["Tags"])
def delete_tag(user_id: int, movie_id: int, tag: str, db: Session = Depends(get_db)):
    """Supprime un tag spécifique"""
    deleted = crud.TagCRUD.delete_tag(db, user_id, movie_id, tag)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    return {"message": "Tag supprimé avec succès"}

#  Routes pour Links

@app.get("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
def read_link(movie_id: int, db: Session = Depends(get_db)):
    """Récupère le lien d'un film"""
    link = crud.LinkCRUD.get_link(db, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Lien non trouvé")
    return link

@app.post("/links/", response_model=schemas.LinkSimple, status_code=201, tags=["Links"])
def create_link(link: schemas.LinkSimple, db: Session = Depends(get_db)):
    """Crée un lien pour un film"""
    movie = crud.MovieCRUD.get_movie(db, link.movieId)
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    return crud.LinkCRUD.create_link(db, link)

@app.put("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
def update_link(movie_id: int, link: schemas.LinkSimple, db: Session = Depends(get_db)):
    """Met à jour un lien"""
    db_link = crud.LinkCRUD.update_link(db, movie_id, link)
    if not db_link:
        raise HTTPException(status_code=404, detail="Lien non trouvé")
    return db_link

@app.delete("/links/{movie_id}", tags=["Links"])
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    """Supprime un lien"""
    deleted = crud.LinkCRUD.delete_link(db, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lien non trouvé")
    return {"message": "Lien supprimé avec succès"}

# Routes pour Statistiques

@app.get("/stats/movies/{movie_id}", tags=["Stats"])
def movie_stats(movie_id: int, db: Session = Depends(get_db)):
    """Statistiques pour un film"""
    stats = crud.StatsCRUD.get_movie_stats(db, movie_id)
    return stats

@app.get("/stats/top-rated", tags=["Stats"])
def top_rated_movies(
    min_ratings: int = Query(5, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Top films les mieux notés"""
    return crud.StatsCRUD.get_top_rated_movies(db, min_ratings, limit)

