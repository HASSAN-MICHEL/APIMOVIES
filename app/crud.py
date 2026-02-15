# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy import and_, or_
# from app import models, schemas
# from typing import List, Optional, Dict, Any



from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any

# Correction des imports
# import models
# import schemas 
from . import models, schemas

#je vais commencé par les movies :

class MovieCRUD:
    @staticmethod
    def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
        """Récupère un film par son ID avec toutes ses relations"""
        return db.query(models.Movie)\
                 .options(
                     joinedload(models.Movie.ratings),
                     joinedload(models.Movie.tags),
                     joinedload(models.Movie.link)
                 )\
                 .filter(models.Movie.movieId == movie_id)\
                 .first()
    
    @staticmethod
    def get_movies(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        genre: Optional[str] = None
    ) -> List[models.Movie]:
        """Récupère une liste de films avec filtres optionnels"""
        query = db.query(models.Movie)
        
        if search:
            query = query.filter(models.Movie.title.contains(search))
        
        if genre:
            query = query.filter(models.Movie.genres.contains(genre))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_movie(db: Session, movie: schemas.MovieBase) -> models.Movie:
        """Crée un nouveau film"""
        db_movie = models.Movie(
            movieId=movie.movieId,
            title=movie.title,
            genres=movie.genres
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def update_movie(
        db: Session, 
        movie_id: int, 
        movie_update: schemas.MovieBase
    ) -> Optional[models.Movie]:
        """Met à jour un film"""
        db_movie = db.query(models.Movie)\
                     .filter(models.Movie.movieId == movie_id)\
                     .first()
        if db_movie:
            if movie_update.title:
                db_movie.title = movie_update.title
            if movie_update.genres is not None:  # Permet de mettre à None
                db_movie.genres = movie_update.genres
            db.commit()
            db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int) -> bool:
        """Supprime un film et ses dépendances (cascade automatique si configurée)"""
        db_movie = db.query(models.Movie)\
                     .filter(models.Movie.movieId == movie_id)\
                     .first()
        if db_movie:
            db.delete(db_movie)
            db.commit()
            return True
        return False
    
#maintenant je vais me servir de ce modèle pour faire les CRUD de Rating, Tag et Link, en adaptant les méthodes pour gérer les relations et les contraintes spécifiques à chaque entité.


class RatingCRUD:
    @staticmethod
    def get_rating(db: Session, user_id: int, movie_id: int) -> Optional[models.Rating]:
        """Récupère une note spécifique"""
        return db.query(models.Rating)\
                 .filter(
                     and_(
                         models.Rating.userId == user_id,
                         models.Rating.movieId == movie_id
                     )
                 )\
                 .first()
    
    @staticmethod
    def get_ratings_by_movie(
        db: Session, 
        movie_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Rating]:
        """Récupère toutes les notes d'un film"""
        return db.query(models.Rating)\
                 .filter(models.Rating.movieId == movie_id)\
                 .offset(skip).limit(limit)\
                 .all()
    
    @staticmethod
    def get_ratings_by_user(
        db: Session, 
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Rating]:
        """Récupère toutes les notes d'un utilisateur"""
        return db.query(models.Rating)\
                 .filter(models.Rating.userId == user_id)\
                 .offset(skip).limit(limit)\
                 .all()
    
    @staticmethod
    def create_rating(db: Session, rating: schemas.RatingBase) -> models.Rating:
        """Crée une nouvelle note"""
        db_rating = models.Rating(**rating.model_dump())
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def update_rating(
        db: Session,
        user_id: int,
        movie_id: int,
        rating_update: schemas.RatingBase
    ) -> Optional[models.Rating]:
        """Met à jour une note"""
        db_rating = db.query(models.Rating)\
                      .filter(
                          and_(
                              models.Rating.userId == user_id,
                              models.Rating.movieId == movie_id
                          )
                      )\
                      .first()
        if db_rating:
            db_rating.rating = rating_update.rating
            db_rating.timestamp = rating_update.timestamp
            db.commit()
            db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def delete_rating(db: Session, user_id: int, movie_id: int) -> bool:
        """Supprime une note"""
        db_rating = db.query(models.Rating)\
                      .filter(
                          and_(
                              models.Rating.userId == user_id,
                              models.Rating.movieId == movie_id
                          )
                      )\
                      .first()
        if db_rating:
            db.delete(db_rating)
            db.commit()
            return True
        return False

# voici mon models  pour les  Tags

class TagCRUD:
    @staticmethod
    def get_tag(db: Session, user_id: int, movie_id: int, tag: str) -> Optional[models.Tag]:
        """Récupère un tag spécifique"""
        return db.query(models.Tag)\
                 .filter(
                     and_(
                         models.Tag.userId == user_id,
                         models.Tag.movieId == movie_id,
                         models.Tag.tag == tag
                     )
                 )\
                 .first()
    
    @staticmethod
    def get_tags_by_movie(
        db: Session, 
        movie_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Tag]:
        """Récupère tous les tags d'un film"""
        return db.query(models.Tag)\
                 .filter(models.Tag.movieId == movie_id)\
                 .offset(skip).limit(limit)\
                 .all()
    
    @staticmethod
    def create_tag(db: Session, tag: schemas.TagBase) -> models.Tag:
        """Crée un nouveau tag"""
        db_tag = models.Tag(**tag.model_dump())
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    
    @staticmethod
    def delete_tag(db: Session, user_id: int, movie_id: int, tag: str) -> bool:
        """Supprime un tag"""
        db_tag = db.query(models.Tag)\
                   .filter(
                       and_(
                           models.Tag.userId == user_id,
                           models.Tag.movieId == movie_id,
                           models.Tag.tag == tag
                       )
                   )\
                   .first()
        if db_tag:
            db.delete(db_tag)
            db.commit()
            return True
        return False

# = CRUD pour Links 

class LinkCRUD:
    @staticmethod
    def get_link(db: Session, movie_id: int) -> Optional[models.Link]:
        """Récupère le lien d'un film"""
        return db.query(models.Link)\
                 .filter(models.Link.movieId == movie_id)\
                 .first()
    
    @staticmethod
    def create_link(db: Session, link: schemas.LinkSimple) -> models.Link:
        """Crée un nouveau lien"""
        db_link = models.Link(**link.model_dump())
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return db_link
    
    @staticmethod
    def update_link(
        db: Session, 
        movie_id: int, 
        link_update: schemas.LinkSimple
    ) -> Optional[models.Link]:
        """Met à jour un lien"""
        db_link = db.query(models.Link)\
                    .filter(models.Link.movieId == movie_id)\
                    .first()
        if db_link:
            if link_update.imdbId is not None:
                db_link.imdbId = link_update.imdbId
            if link_update.tmdbId is not None:
                db_link.tmdbId = link_update.tmdbId
            db.commit()
            db.refresh(db_link)
        return db_link
    
    @staticmethod
    def delete_link(db: Session, movie_id: int) -> bool:
        """Supprime un lien"""
        db_link = db.query(models.Link)\
                    .filter(models.Link.movieId == movie_id)\
                    .first()
        if db_link:
            db.delete(db_link)
            db.commit()
            return True
        return False

#  Statistiques et recherches avancées 

class StatsCRUD:
    @staticmethod
    def get_movie_stats(db: Session, movie_id: int) -> Dict[str, Any]:
        """Statistiques pour un film spécifique"""
        ratings = db.query(models.Rating)\
                    .filter(models.Rating.movieId == movie_id)\
                    .all()
        
        if not ratings:
            return {
                "movie_id": movie_id,
                "avg_rating": None,
                "total_ratings": 0,
                "total_tags": 0
            }
        
        avg_rating = sum(r.rating for r in ratings) / len(ratings)
        total_tags = db.query(models.Tag)\
                       .filter(models.Tag.movieId == movie_id)\
                       .count()
        
        return {
            "movie_id": movie_id,
            "avg_rating": round(avg_rating, 2),
            "total_ratings": len(ratings),
            "total_tags": total_tags
        }
    
    @staticmethod
    def get_top_rated_movies(
        db: Session, 
        min_ratings: int = 5,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Récupère les films les mieux notés (avec minimum de notes)"""
        from sqlalchemy import func
        
        results = db.query(
            models.Movie.movieId,
            models.Movie.title,
            func.avg(models.Rating.rating).label('avg_rating'),
            func.count(models.Rating.rating).label('num_ratings')
        ).join(models.Rating)\
         .group_by(models.Movie.movieId)\
         .having(func.count(models.Rating.rating) >= min_ratings)\
         .order_by(func.avg(models.Rating.rating).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                "movie_id": r.movieId,
                "title": r.title,
                "avg_rating": round(r.avg_rating, 2),
                "num_ratings": r.num_ratings
            }
            for r in results ]