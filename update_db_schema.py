"""
Script to update the database schema with new models
"""
from app import app, db
from models import (User, Product, FarmingTip, NewsArticle, WeatherAlert, 
                   ChatHistory, MediaResource, FarmerChatMessage, FarmerChatRoom,
                   SoilAnalysis, CropCalendar, tip_resource_association, chat_room_participants)

def update_schema():
    """Update the database schema with new models and fields"""
    with app.app_context():
        # Create tables for new models
        db.create_all()
        
        # Add new columns to existing tables if they don't exist
        from sqlalchemy import text
        
        # Check if farm_type exists in FarmingTip
        try:
            db.session.execute(text("SELECT farm_type FROM farming_tip LIMIT 1"))
            print("farm_type column already exists in farming_tip table")
        except:
            print("Adding farm_type column to farming_tip table")
            db.session.execute(text("ALTER TABLE farming_tip ADD COLUMN farm_type VARCHAR(100)"))
        
        # Check if image_url exists in FarmingTip
        try:
            db.session.execute(text("SELECT image_url FROM farming_tip LIMIT 1"))
            print("image_url column already exists in farming_tip table")
        except:
            print("Adding image_url column to farming_tip table")
            db.session.execute(text("ALTER TABLE farming_tip ADD COLUMN image_url VARCHAR(500)"))
        
        # Check if additional fields exist in User
        for field in ['phone_number', 'bio', 'is_extension_officer', 'is_buyer']:
            try:
                db.session.execute(text(f"SELECT {field} FROM user LIMIT 1"))
                print(f"{field} column already exists in user table")
            except:
                print(f"Adding {field} column to user table")
                if field in ['is_extension_officer', 'is_buyer']:
                    db.session.execute(text(f"ALTER TABLE user ADD COLUMN {field} BOOLEAN DEFAULT 0"))
                elif field == 'bio':
                    db.session.execute(text(f"ALTER TABLE user ADD COLUMN {field} TEXT"))
                else:
                    db.session.execute(text(f"ALTER TABLE user ADD COLUMN {field} VARCHAR(100)"))
        
        # Check if additional fields exist in Product
        for field in ['certification', 'harvest_date', 'expiry_date']:
            try:
                db.session.execute(text(f"SELECT {field} FROM product LIMIT 1"))
                print(f"{field} column already exists in product table")
            except:
                print(f"Adding {field} column to product table")
                if field in ['harvest_date', 'expiry_date']:
                    db.session.execute(text(f"ALTER TABLE product ADD COLUMN {field} DATETIME"))
                else:
                    db.session.execute(text(f"ALTER TABLE product ADD COLUMN {field} VARCHAR(100)"))
        
        # Check if additional fields exist in NewsArticle
        for field in ['farm_type', 'author', 'thumbnail_url']:
            try:
                db.session.execute(text(f"SELECT {field} FROM news_article LIMIT 1"))
                print(f"{field} column already exists in news_article table")
            except:
                print(f"Adding {field} column to news_article table")
                if field == 'thumbnail_url':
                    db.session.execute(text(f"ALTER TABLE news_article ADD COLUMN {field} VARCHAR(500)"))
                else:
                    db.session.execute(text(f"ALTER TABLE news_article ADD COLUMN {field} VARCHAR(100)"))
        
        # Commit all changes
        db.session.commit()
        print("Database schema updated successfully!")

if __name__ == "__main__":
    update_schema()