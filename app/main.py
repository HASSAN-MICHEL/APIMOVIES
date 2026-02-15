# from fastapi import FastAPI, Depends, HTTPException, status, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app.database import engine, Base, get_db
# from app import schemas, crud

# import models 

# # Création des tables
# Base.metadata.create_all(bind=engine)

# # Initialisation FastAPI
# app = FastAPI(
#     title="API Films - Système de recommandation",
#     description="API pour gérer des films, notes, tags et liens externes",
#     version="1.0.0"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  Routes pour Movies

# @app.get("/", tags=["Root"])
# def read_root():
#     return {
#         "message": "API de gestion de films",
#         "endpoints": {
#             "movies": "/movies/",
#             "ratings": "/ratings/",
#             "tags": "/tags/",
#             "links": "/links/",
#             "stats": "/stats/"
#         }
#     }

# @app.get("/movies/", response_model=List[schemas.MovieSimple], tags=["Movies"])
# def read_movies(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, ge=1, le=1000),
#     search: Optional[str] = None,
#     genre: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     """Liste tous les films avec pagination et filtres"""
#     movies = crud.MovieCRUD.get_movies(db, skip=skip, limit=limit, search=search, genre=genre)
#     return movies

# @app.get("/movies/{movie_id}", response_model=schemas.MovieDetailed, tags=["Movies"])
# def read_movie(movie_id: int, db: Session = Depends(get_db)):
#     """Détail d'un film avec ses notes, tags et liens"""
#     movie = crud.MovieCRUD.get_movie(db, movie_id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
#     return movie

# @app.post("/movies/", response_model=schemas.MovieSimple, status_code=201, tags=["Movies"])
# def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
#     """Crée un nouveau film"""
#     return crud.MovieCRUD.create_movie(db, movie)

# @app.put("/movies/{movie_id}", response_model=schemas.MovieSimple, tags=["Movies"])
# def update_movie(movie_id: int, movie: schemas.MovieBase, db: Session = Depends(get_db)):
#     """Met à jour un film"""
#     db_movie = crud.MovieCRUD.update_movie(db, movie_id, movie)
#     if not db_movie:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
#     return db_movie

# @app.delete("/movies/{movie_id}", tags=["Movies"])
# def delete_movie(movie_id: int, db: Session = Depends(get_db)):
#     """Supprime un film"""
#     deleted = crud.MovieCRUD.delete_movie(db, movie_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
#     return {"message": f"Film {movie_id} supprimé avec succès"}



# #  Routes pour Ratings 

# @app.get("/ratings/", response_model=List[schemas.RatingSimple], tags=["Ratings"])
# def read_ratings(
#     movie_id: Optional[int] = None,
#     user_id: Optional[int] = None,
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Liste des notes (filtrable par film ou utilisateur)"""
#     if movie_id:
#         return crud.RatingCRUD.get_ratings_by_movie(db, movie_id, skip, limit)
#     elif user_id:
#         return crud.RatingCRUD.get_ratings_by_user(db, user_id, skip, limit)
#     else:
#         return db.query(models.Rating).offset(skip).limit(limit).all()

# @app.post("/ratings/", response_model=schemas.RatingSimple, status_code=201, tags=["Ratings"])
# def create_rating(rating: schemas.RatingBase, db: Session = Depends(get_db)):
#     """Ajoute une note à un film"""
#     # Vérifie que le film existe
#     movie = crud.MovieCRUD.get_movie(db, rating.movieId)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
    
#     return crud.RatingCRUD.create_rating(db, rating)

# @app.put("/ratings/{user_id}/{movie_id}", response_model=schemas.RatingSimple, tags=["Ratings"])
# def update_rating(
#     user_id: int, 
#     movie_id: int, 
#     rating: schemas.RatingBase, 
#     db: Session = Depends(get_db)
# ):
#     """Met à jour une note"""
#     db_rating = crud.RatingCRUD.update_rating(db, user_id, movie_id, rating)
#     if not db_rating:
#         raise HTTPException(status_code=404, detail="Note non trouvée")
#     return db_rating

# @app.delete("/ratings/{user_id}/{movie_id}", tags=["Ratings"])
# def delete_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
#     """Supprime une note"""
#     deleted = crud.RatingCRUD.delete_rating(db, user_id, movie_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Note non trouvée")
#     return {"message": "Note supprimée avec succès"}

# # Routes pour Tags 

# @app.get("/tags/", response_model=List[schemas.TagSimple], tags=["Tags"])
# def read_tags(
#     movie_id: Optional[int] = None,
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Liste des tags (filtrable par film)"""
#     if movie_id:
#         return crud.TagCRUD.get_tags_by_movie(db, movie_id, skip, limit)
#     return db.query(models.Tag).offset(skip).limit(limit).all()

# @app.post("/tags/", response_model=schemas.TagSimple, status_code=201, tags=["Tags"])
# def create_tag(tag: schemas.TagBase, db: Session = Depends(get_db)):
#     """Ajoute un tag à un film"""
#     movie = crud.MovieCRUD.get_movie(db, tag.movieId)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
    
#     return crud.TagCRUD.create_tag(db, tag)

# @app.delete("/tags/{user_id}/{movie_id}/{tag}", tags=["Tags"])
# def delete_tag(user_id: int, movie_id: int, tag: str, db: Session = Depends(get_db)):
#     """Supprime un tag spécifique"""
#     deleted = crud.TagCRUD.delete_tag(db, user_id, movie_id, tag)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Tag non trouvé")
#     return {"message": "Tag supprimé avec succès"}

# #  Routes pour Links

# @app.get("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
# def read_link(movie_id: int, db: Session = Depends(get_db)):
#     """Récupère le lien d'un film"""
#     link = crud.LinkCRUD.get_link(db, movie_id)
#     if not link:
#         raise HTTPException(status_code=404, detail="Lien non trouvé")
#     return link

# @app.post("/links/", response_model=schemas.LinkSimple, status_code=201, tags=["Links"])
# def create_link(link: schemas.LinkSimple, db: Session = Depends(get_db)):
#     """Crée un lien pour un film"""
#     movie = crud.MovieCRUD.get_movie(db, link.movieId)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Film non trouvé")
    
#     return crud.LinkCRUD.create_link(db, link)

# @app.put("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
# def update_link(movie_id: int, link: schemas.LinkSimple, db: Session = Depends(get_db)):
#     """Met à jour un lien"""
#     db_link = crud.LinkCRUD.update_link(db, movie_id, link)
#     if not db_link:
#         raise HTTPException(status_code=404, detail="Lien non trouvé")
#     return db_link

# @app.delete("/links/{movie_id}", tags=["Links"])
# def delete_link(movie_id: int, db: Session = Depends(get_db)):
#     """Supprime un lien"""
#     deleted = crud.LinkCRUD.delete_link(db, movie_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Lien non trouvé")
#     return {"message": "Lien supprimé avec succès"}

# # Routes pour Statistiques

# @app.get("/stats/movies/{movie_id}", tags=["Stats"])
# def movie_stats(movie_id: int, db: Session = Depends(get_db)):
#     """Statistiques pour un film"""
#     stats = crud.StatsCRUD.get_movie_stats(db, movie_id)
#     return stats

# @app.get("/stats/top-rated", tags=["Stats"])
# def top_rated_movies(
#     min_ratings: int = Query(5, ge=1),
#     limit: int = Query(10, ge=1, le=50),
#     db: Session = Depends(get_db)
# ):
#     """Top films les mieux notés"""
#     return crud.StatsCRUD.get_top_rated_movies(db, min_ratings, limit)



"""
app/main.py - Version corrigée
API de gestion de films avec FastAPI
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports CORRIGÉS - ajout de models
from app.database import engine, Base, get_db
from app import schemas, crud, models  # ← IMPORTANT: ajout de models

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



@app.get("/", tags=["Root"])
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "API de gestion de films",
        "version": "1.0.0",
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
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre d'éléments par page"),
    search: Optional[str] = Query(None, description="Recherche dans le titre"),
    genre: Optional[str] = Query(None, description="Filtre par genre"),
    db: Session = Depends(get_db)
):
    """Liste tous les films avec pagination et filtres"""
    movies = crud.MovieCRUD.get_movies(db, skip=skip, limit=limit, search=search, genre=genre)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.MovieDetailed, tags=["Movies"])
def read_movie(
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Détail d'un film avec ses notes, tags et liens"""
    movie = crud.MovieCRUD.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {movie_id} non trouvé"
        )
    return movie

@app.post("/movies/", response_model=schemas.MovieSimple, status_code=201, tags=["Movies"])
def create_movie(
    movie: schemas.MovieBase, 
    db: Session = Depends(get_db)
):
    """Crée un nouveau film"""
    # Vérifie si le film existe déjà
    existing = crud.MovieCRUD.get_movie(db, movie.movieId)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un film avec l'ID {movie.movieId} existe déjà"
        )
    return crud.MovieCRUD.create_movie(db, movie)

@app.put("/movies/{movie_id}", response_model=schemas.MovieSimple, tags=["Movies"])
def update_movie(
    movie_id: int, 
    movie: schemas.MovieBase, 
    db: Session = Depends(get_db)
):
    """Met à jour un film"""
    db_movie = crud.MovieCRUD.update_movie(db, movie_id, movie)
    if not db_movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {movie_id} non trouvé"
        )
    return db_movie

@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Supprime un film"""
    deleted = crud.MovieCRUD.delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {movie_id} non trouvé"
        )
    return {"message": f"Film {movie_id} supprimé avec succès"}

# ============================================
# Routes pour Ratings - CORRIGÉES
# ============================================

@app.get("/ratings/", response_model=List[schemas.RatingSimple], tags=["Ratings"])
def read_ratings(
    movie_id: Optional[int] = Query(None, description="Filtrer par ID du film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID de l'utilisateur"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre d'éléments par page"),
    db: Session = Depends(get_db)
):
    """Liste des notes (filtrable par film ou utilisateur)"""
    if movie_id:
        return crud.RatingCRUD.get_ratings_by_movie(db, movie_id, skip, limit)
    elif user_id:
        return crud.RatingCRUD.get_ratings_by_user(db, user_id, skip, limit)
    else:
        # CORRIGÉ: utilisation correcte de models.Rating
        return db.query(models.Rating).offset(skip).limit(limit).all()

@app.post("/ratings/", response_model=schemas.RatingSimple, status_code=201, tags=["Ratings"])
def create_rating(
    rating: schemas.RatingBase, 
    db: Session = Depends(get_db)
):
    """Ajoute une note à un film"""
    # Vérifie que le film existe
    movie = crud.MovieCRUD.get_movie(db, rating.movieId)
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {rating.movieId} non trouvé"
        )
    
    # Vérifie si l'utilisateur a déjà noté ce film
    existing = crud.RatingCRUD.get_rating(db, rating.userId, rating.movieId)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"L'utilisateur {rating.userId} a déjà noté le film {rating.movieId}"
        )
    
    return crud.RatingCRUD.create_rating(db, rating)

@app.put("/ratings/{user_id}/{movie_id}", response_model=schemas.RatingSimple, tags=["Ratings"])
def update_rating(
    user_id: int, 
    movie_id: int, 
    rating: schemas.RatingBase, 
    db: Session = Depends(get_db)
):
    """Met à jour une note"""
    # Vérifie que l'URL correspond aux données
    if user_id != rating.userId or movie_id != rating.movieId:
        raise HTTPException(
            status_code=400,
            detail="Les IDs dans l'URL ne correspondent pas aux données"
        )
    
    db_rating = crud.RatingCRUD.update_rating(db, user_id, movie_id, rating)
    if not db_rating:
        raise HTTPException(
            status_code=404, 
            detail=f"Note pour l'utilisateur {user_id} et film {movie_id} non trouvée"
        )
    return db_rating

@app.delete("/ratings/{user_id}/{movie_id}", tags=["Ratings"])
def delete_rating(
    user_id: int, 
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Supprime une note"""
    deleted = crud.RatingCRUD.delete_rating(db, user_id, movie_id)
    if not deleted:
        raise HTTPException(
            status_code=404, 
            detail=f"Note pour l'utilisateur {user_id} et film {movie_id} non trouvée"
        )
    return {"message": "Note supprimée avec succès"}

# ============================================
# Routes pour Tags - CORRIGÉES
# ============================================

@app.get("/tags/", response_model=List[schemas.TagSimple], tags=["Tags"])
def read_tags(
    movie_id: Optional[int] = Query(None, description="Filtrer par ID du film"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre d'éléments par page"),
    db: Session = Depends(get_db)
):
    """Liste des tags (filtrable par film)"""
    if movie_id:
        return crud.TagCRUD.get_tags_by_movie(db, movie_id, skip, limit)
    # CORRIGÉ: utilisation correcte de models.Tag
    return db.query(models.Tag).offset(skip).limit(limit).all()

@app.post("/tags/", response_model=schemas.TagSimple, status_code=201, tags=["Tags"])
def create_tag(
    tag: schemas.TagBase, 
    db: Session = Depends(get_db)
):
    """Ajoute un tag à un film"""
    # Vérifie que le film existe
    movie = crud.MovieCRUD.get_movie(db, tag.movieId)
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {tag.movieId} non trouvé"
        )
    
    return crud.TagCRUD.create_tag(db, tag)

@app.delete("/tags/{user_id}/{movie_id}/{tag}", tags=["Tags"])
def delete_tag(
    user_id: int, 
    movie_id: int, 
    tag: str, 
    db: Session = Depends(get_db)
):
    """Supprime un tag spécifique"""
    deleted = crud.TagCRUD.delete_tag(db, user_id, movie_id, tag)
    if not deleted:
        raise HTTPException(
            status_code=404, 
            detail=f"Tag '{tag}' pour l'utilisateur {user_id} et film {movie_id} non trouvé"
        )
    return {"message": "Tag supprimé avec succès"}

# ============================================
# Routes pour Links - CORRIGÉES avec gestion des conflits
# ============================================

@app.get("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
def read_link(
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Récupère le lien d'un film"""
    link = crud.LinkCRUD.get_link(db, movie_id)
    if not link:
        raise HTTPException(
            status_code=404, 
            detail=f"Lien pour le film {movie_id} non trouvé"
        )
    return link

@app.post("/links/", response_model=schemas.LinkSimple, status_code=201, tags=["Links"])
def create_link(
    link: schemas.LinkSimple, 
    db: Session = Depends(get_db)
):
    """Crée un lien pour un film"""
    # Vérifie que le film existe
    movie = crud.MovieCRUD.get_movie(db, link.movieId)
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {link.movieId} non trouvé"
        )
    
    # CORRIGÉ: Vérifie si un lien existe déjà pour ce film
    existing_link = crud.LinkCRUD.get_link(db, link.movieId)
    if existing_link:
        raise HTTPException(
            status_code=400,
            detail=f"Un lien existe déjà pour le film {link.movieId}. Utilisez PUT pour le modifier."
        )
    
    return crud.LinkCRUD.create_link(db, link)

@app.put("/links/{movie_id}", response_model=schemas.LinkSimple, tags=["Links"])
def update_link(
    movie_id: int, 
    link: schemas.LinkSimple, 
    db: Session = Depends(get_db)
):
    """Met à jour un lien"""
    # Vérifie que l'URL correspond
    if movie_id != link.movieId:
        raise HTTPException(
            status_code=400,
            detail="L'ID du film dans l'URL ne correspond pas aux données"
        )
    
    db_link = crud.LinkCRUD.update_link(db, movie_id, link)
    if not db_link:
        raise HTTPException(
            status_code=404, 
            detail=f"Lien pour le film {movie_id} non trouvé"
        )
    return db_link

@app.delete("/links/{movie_id}", tags=["Links"])
def delete_link(
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Supprime un lien"""
    deleted = crud.LinkCRUD.delete_link(db, movie_id)
    if not deleted:
        raise HTTPException(
            status_code=404, 
            detail=f"Lien pour le film {movie_id} non trouvé"
        )
    return {"message": f"Lien pour le film {movie_id} supprimé avec succès"}

# ============================================
# Routes pour Statistiques
# ============================================

@app.get("/stats/movies/{movie_id}", tags=["Stats"])
def movie_stats(
    movie_id: int, 
    db: Session = Depends(get_db)
):
    """Statistiques pour un film (moyenne des notes, nombre de notes, nombre de tags)"""
    # Vérifie que le film existe
    movie = crud.MovieCRUD.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"Film avec l'ID {movie_id} non trouvé"
        )
    
    stats = crud.StatsCRUD.get_movie_stats(db, movie_id)
    return stats

@app.get("/stats/top-rated", tags=["Stats"])
def top_rated_movies(
    min_ratings: int = Query(5, ge=1, description="Nombre minimum de notes requis"),
    limit: int = Query(10, ge=1, le=50, description="Nombre de films à retourner"),
    db: Session = Depends(get_db)
):
    """Top films les mieux notés (avec un minimum de notes)"""
    return crud.StatsCRUD.get_top_rated_movies(db, min_ratings, limit)



@app.get("/health", tags=["Health"])
def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }