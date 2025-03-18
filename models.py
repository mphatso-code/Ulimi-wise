from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    preferred_language = db.Column(db.String(10), default='en')
    location = db.Column(db.String(200))
    farm_type = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    bio = db.Column(db.Text)
    is_extension_officer = db.Column(db.Boolean, default=False)
    is_buyer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='seller', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, liters, units, etc.
    category = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)
    certification = db.Column(db.String(100))  # organic, fair trade, etc.
    harvest_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    

class FarmingTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # crop type, animal husbandry, etc.
    season = db.Column(db.String(20))  # spring, summer, fall, winter or null if applicable year-round
    region = db.Column(db.String(50))  # continent, country or null if applicable globally
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    farm_type = db.Column(db.String(100))  # Related farm type
    image_url = db.Column(db.String(500))  # URL to related image
    
    # Relationships
    related_resources = db.relationship('MediaResource', secondary='tip_resource_association', 
                                       back_populates='related_tips')


class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    media_type = db.Column(db.String(20), nullable=False)  # article, video, podcast
    media_url = db.Column(db.String(500))  # for videos and podcasts
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    farm_type = db.Column(db.String(100))  # Related farm type
    author = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(500))


class WeatherAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # rain, drought, frost, etc.
    message = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = db.relationship('User', backref=db.backref('weather_alerts', lazy=True))


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = db.relationship('User', backref=db.backref('chat_history', lazy=True))


# New Models for Enhanced Features

class MediaResource(db.Model):
    """Media resources for agricultural content - articles, videos, podcasts"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(20), nullable=False)  # article, video, podcast
    url = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(100))
    author = db.Column(db.String(100))
    farm_type = db.Column(db.String(100))  # Related farm type
    thumbnail_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    related_tips = db.relationship('FarmingTip', secondary='tip_resource_association',
                                 back_populates='related_resources')


# Association table for FarmingTip and MediaResource many-to-many relationship
tip_resource_association = db.Table('tip_resource_association',
    db.Column('tip_id', db.Integer, db.ForeignKey('farming_tip.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('media_resource.id'), primary_key=True)
)


class FarmerChatMessage(db.Model):
    """Messages for farmer community chat"""
    id = db.Column(db.Integer, primary_key=True)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('farmer_chat_room.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    # Relationships
    sender = db.relationship('User', backref=db.backref('sent_messages', lazy=True))
    chat_room = db.relationship('FarmerChatRoom', backref=db.backref('messages', lazy=True))


class FarmerChatRoom(db.Model):
    """Chat rooms for farmer community communication"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_group = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String(100))  # Topic of discussion
    
    # Relationships
    creator = db.relationship('User', backref=db.backref('created_rooms', lazy=True))
    participants = db.relationship('User', secondary='chat_room_participants', 
                                lazy='subquery', backref=db.backref('chat_rooms', lazy=True))


# Association table for FarmerChatRoom and User many-to-many relationship
chat_room_participants = db.Table('chat_room_participants',
    db.Column('room_id', db.Integer, db.ForeignKey('farmer_chat_room.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class SoilAnalysis(db.Model):
    """Soil analysis data for farms"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    ph_level = db.Column(db.Float)
    nitrogen_level = db.Column(db.Float)
    phosphorus_level = db.Column(db.Float)
    potassium_level = db.Column(db.Float)
    organic_matter = db.Column(db.Float)
    moisture_content = db.Column(db.Float)
    soil_type = db.Column(db.String(50))
    recommendations = db.Column(db.Text)
    
    # Relationship with user
    user = db.relationship('User', backref=db.backref('soil_analyses', lazy=True))


class IoTSensor(db.Model):
    """IoT sensors deployed on farms"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # soil_moisture, temperature, humidity, etc.
    location = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    last_reading = db.Column(db.Float)
    last_reading_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = db.relationship('User', backref=db.backref('sensors', lazy=True))
    # Relationship with readings
    readings = db.relationship('SensorReading', backref='sensor', lazy=True)


class SensorReading(db.Model):
    """Readings from IoT sensors"""
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('io_t_sensor.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    battery_level = db.Column(db.Float)
    signal_strength = db.Column(db.Float)


class CropCalendar(db.Model):
    """Calendar for crop planting and harvesting based on region"""
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    planting_start = db.Column(db.String(20))  # Month or season to start planting
    planting_end = db.Column(db.String(20))    # Month or season to end planting
    harvesting_start = db.Column(db.String(20)) # Month or season to start harvesting
    harvesting_end = db.Column(db.String(20))   # Month or season to end harvesting
    growing_period = db.Column(db.Integer)      # Days until harvest
    water_requirements = db.Column(db.Text)
    soil_requirements = db.Column(db.Text)
    notes = db.Column(db.Text)
