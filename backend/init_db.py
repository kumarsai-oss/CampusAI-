#!/usr/bin/env python
"""Database initialization and migration script"""

from app.database import init_db, SessionLocal
from app.models.user import User, UserRole
from app.security import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_admin_user():
    """Create a default admin user"""
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            logger.info("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@campusai.com",
            full_name="System Administrator",
            hashed_password=hash_password("admin123456"),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        
        db.add(admin_user)
        db.commit()
        logger.info("Admin user created successfully")
        logger.info("Username: admin, Password: admin123456")
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database tables created")
    
    logger.info("Seeding admin user...")
    seed_admin_user()
    
    logger.info("Database initialization complete!")
