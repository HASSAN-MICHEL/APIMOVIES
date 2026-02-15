# test_db.py
from app.database import SessionLocal, engine
from app.models import Base, Movie

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer une session
db = SessionLocal()

try:
    # Créer un film test
    test_movie = Movie(
        movieId=999,
        title="Film Test",
        genres="Test"
    )
    
    # Ajouter et commiter
    db.add(test_movie)
    db.commit()
    db.refresh(test_movie)
    
    print(f"✅ Film créé avec ID: {test_movie.movieId}")
    
    # Vérifier qu'il est bien là
    movie = db.query(Movie).filter(Movie.movieId == 999).first()
    print(f"✅ Film trouvé: {movie.title}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    db.rollback()
finally:
    db.close()