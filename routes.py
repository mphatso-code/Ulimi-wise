from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import (User, Product, FarmingTip, NewsArticle, WeatherAlert, ChatHistory,
                   MediaResource, FarmerChatMessage, FarmerChatRoom, SoilAnalysis, 
                   CropCalendar, chat_room_participants)
from chatbot import process_message
from weather import get_weather_for_location, get_weather_recommendations
from translations import get_translation, get_available_languages
from utils import is_valid_email, allowed_file, save_file
import logging
from datetime import datetime


@app.route('/')
def index():
    """Home page with introduction to Ulimi Wise"""
    # Get the user's preferred language or use the session language
    lang = session.get('language', 'en')
    if current_user.is_authenticated and current_user.preferred_language:
        lang = current_user.preferred_language
        
    # Get latest tips, limited to 3
    latest_tips = FarmingTip.query.order_by(FarmingTip.created_at.desc()).limit(3).all()
    
    # Get latest news, limited to 4
    latest_news = NewsArticle.query.order_by(NewsArticle.created_at.desc()).limit(4).all()
    
    return render_template('index.html', 
                          tips=latest_tips, 
                          news=latest_news, 
                          lang=lang,
                          title=get_translation("Welcome to Ulimi Wise", lang))


@app.route('/set_language/<lang>')
def set_language(lang):
    """Set the language for the current session"""
    session['language'] = lang
    
    # If user is logged in, update their preferred language
    if current_user.is_authenticated:
        current_user.preferred_language = lang
        db.session.commit()
        
    # Redirect back to the referring page or to home if none
    return redirect(request.referrer or url_for('index'))


@app.route('/languages')
def languages():
    """Return available languages as JSON"""
    return jsonify(get_available_languages())


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and form submission"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    lang = session.get('language', 'en')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash(get_translation('Invalid email or password', lang), 'danger')
    
    return render_template('login.html', 
                           lang=lang, 
                           title=get_translation("Login", lang))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page and form submission"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    lang = session.get('language', 'en')
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        language = request.form.get('language', 'en')
        location = request.form.get('location')
        farm_type = request.form.get('farm_type')
        
        # Validate email format
        if not is_valid_email(email):
            flash(get_translation('Invalid email format', lang), 'danger')
            return render_template('register.html', lang=lang)
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash(get_translation('Username or email already in use', lang), 'danger')
            return render_template('register.html', lang=lang)
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            preferred_language=language,
            location=location,
            farm_type=farm_type
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(get_translation('Registration successful! Please login.', lang), 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', 
                           lang=lang, 
                           languages=get_available_languages(),
                           title=get_translation("Register", lang))


@app.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with personalized content"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    # Get weather for user's location
    weather_data = {}
    weather_recommendations = []
    if current_user.location:
        weather_data = get_weather_for_location(current_user.location)
        weather_recommendations = get_weather_recommendations(weather_data, current_user.farm_type, lang)
    
    # Get user's weather alerts
    alerts = WeatherAlert.query.filter_by(user_id=current_user.id, is_read=False).all()
    
    # Get farming tips relevant to user
    relevant_tips = FarmingTip.query.filter_by(category=current_user.farm_type).limit(5).all() if current_user.farm_type else FarmingTip.query.limit(5).all()
    
    # Get user's marketplace listings
    user_products = Product.query.filter_by(seller_id=current_user.id).all()
    
    return render_template('dashboard.html',
                          lang=lang,
                          weather=weather_data,
                          weather_recommendations=weather_recommendations,
                          alerts=alerts,
                          tips=relevant_tips,
                          products=user_products,
                          title=get_translation("Dashboard", lang))


@app.route('/marketplace')
def marketplace():
    """Marketplace for buying and selling agricultural products"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    # Get all available products
    products = Product.query.filter_by(is_available=True).order_by(Product.created_at.desc()).all()
    
    # Get product categories for filtering
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('marketplace.html',
                          lang=lang,
                          products=products,
                          categories=categories,
                          title=get_translation("Marketplace", lang))


@app.route('/marketplace/add', methods=['POST'])
@login_required
def add_product():
    """Add a new product to the marketplace"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    unit = request.form.get('unit')
    category = request.form.get('category')
    
    # Validate inputs
    if not all([name, price, quantity, unit, category]):
        flash(get_translation('All fields marked with * are required', lang), 'danger')
        return redirect(url_for('marketplace'))
    
    try:
        price = float(price)
        quantity = float(quantity)
    except ValueError:
        flash(get_translation('Price and quantity must be numeric values', lang), 'danger')
        return redirect(url_for('marketplace'))
    
    # Create new product
    new_product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        unit=unit,
        category=category,
        seller_id=current_user.id
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    flash(get_translation('Product added successfully', lang), 'success')
    return redirect(url_for('marketplace'))


@app.route('/marketplace/update/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    """Update an existing product"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    product = Product.query.get_or_404(product_id)
    
    # Check if the current user is the owner of the product
    if product.seller_id != current_user.id:
        flash(get_translation('You can only update your own products', lang), 'danger')
        return redirect(url_for('marketplace'))
    
    # Update product details
    product.name = request.form.get('name', product.name)
    product.description = request.form.get('description', product.description)
    product.price = float(request.form.get('price', product.price))
    product.quantity = float(request.form.get('quantity', product.quantity))
    product.unit = request.form.get('unit', product.unit)
    product.category = request.form.get('category', product.category)
    product.is_available = 'is_available' in request.form
    
    db.session.commit()
    
    flash(get_translation('Product updated successfully', lang), 'success')
    return redirect(url_for('marketplace'))


@app.route('/marketplace/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a product from the marketplace"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    product = Product.query.get_or_404(product_id)
    
    # Check if the current user is the owner of the product
    if product.seller_id != current_user.id:
        flash(get_translation('You can only delete your own products', lang), 'danger')
        return redirect(url_for('marketplace'))
    
    db.session.delete(product)
    db.session.commit()
    
    flash(get_translation('Product deleted successfully', lang), 'success')
    return redirect(url_for('marketplace'))


@app.route('/tips')
def tips():
    """Farming tips page"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    # Get filter parameters
    farm_type = request.args.get('farm_type')
    
    # Get all tips
    if farm_type and farm_type != 'all':
        all_tips = FarmingTip.query.filter_by(farm_type=farm_type).order_by(FarmingTip.created_at.desc()).all()
    else:
        all_tips = FarmingTip.query.order_by(FarmingTip.created_at.desc()).all()
    
    # Get categories for filtering
    categories = db.session.query(FarmingTip.category).distinct().all()
    categories = [c[0] for c in categories]
    
    # Get seasons for filtering
    seasons = db.session.query(FarmingTip.season).distinct().all()
    seasons = [s[0] for s in seasons if s[0]]
    
    # Get farm types for filtering
    farm_types = db.session.query(FarmingTip.farm_type).distinct().all()
    farm_types = [f[0] for f in farm_types if f[0]]
    
    return render_template('tips.html',
                          lang=lang,
                          tips=all_tips,
                          categories=categories,
                          seasons=seasons,
                          farm_types=farm_types,
                          title=get_translation("Farming Tips", lang))


@app.route('/api/tips/<int:tip_id>/resources')
def get_tip_resources(tip_id):
    """Get resources related to a specific farming tip"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    tip = FarmingTip.query.get_or_404(tip_id)
    resources = tip.related_resources
    
    resource_list = []
    for resource in resources:
        resource_list.append({
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'resource_type': resource.resource_type,
            'url': resource.url,
            'source': resource.source,
            'author': resource.author,
            'thumbnail_url': resource.thumbnail_url
        })
    
    return jsonify({'resources': resource_list})


@app.route('/news')
def news():
    """News hub for agricultural content"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    # Get all news articles
    all_news = NewsArticle.query.order_by(NewsArticle.created_at.desc()).all()
    
    # Filter by media type if specified
    media_type = request.args.get('type')
    if media_type:
        all_news = [n for n in all_news if n.media_type == media_type]
    
    return render_template('news.html',
                          lang=lang,
                          news=all_news,
                          title=get_translation("Agricultural News", lang))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page for viewing and updating personal information"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    if request.method == 'POST':
        # Update user profile
        current_user.username = request.form.get('username', current_user.username)
        current_user.email = request.form.get('email', current_user.email)
        current_user.preferred_language = request.form.get('language', current_user.preferred_language)
        current_user.location = request.form.get('location', current_user.location)
        current_user.farm_type = request.form.get('farm_type', current_user.farm_type)
        
        # Change password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if not current_user.check_password(current_password):
                flash(get_translation('Current password is incorrect', lang), 'danger')
                return redirect(url_for('profile'))
            current_user.set_password(new_password)
        
        db.session.commit()
        flash(get_translation('Profile updated successfully', lang), 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html',
                          lang=lang,
                          languages=get_available_languages(),
                          title=get_translation("My Profile", lang))


@app.route('/chatbot')
def chatbot_page():
    """Voice-enabled chatbot page"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    # Get chat history if user is logged in
    chat_history = []
    if current_user.is_authenticated:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.created_at.desc()).limit(10).all()
        chat_history.reverse()  # Show oldest messages first
    
    return render_template('chatbot.html',
                          lang=lang,
                          chat_history=chat_history,
                          title=get_translation("Agricultural Assistant", lang))


@app.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    """API endpoint for chatbot messages"""
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    message = request.form.get('message', '')
    if not message:
        return jsonify({'error': get_translation('No message provided', lang)}), 400
    
    # Get response from chatbot
    response = process_message(message, lang)
    
    # Save chat history if user is logged in
    if current_user.is_authenticated:
        chat_entry = ChatHistory(
            user_id=current_user.id,
            user_message=message,
            bot_response=response
        )
        db.session.add(chat_entry)
        db.session.commit()
    
    return jsonify({
        'response': response,
        'voice_url': f"/chatbot/voice?text={response}&lang={lang}"
    })


@app.route('/chatbot/voice')
def chatbot_voice():
    """Generate voice response for chatbot"""
    from gtts import gTTS
    import tempfile
    import os
    from flask import send_file
    
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'en')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Create temporary file for audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.close()
    
    # Generate speech from text
    tts = gTTS(text=text, lang=lang[:2])  # Using first 2 chars of language code
    tts.save(temp_file.name)
    
    # Send the audio file
    return send_file(temp_file.name, mimetype='audio/mp3')


@app.route('/weather')
def weather():
    """Get weather information for a location"""
    location = request.args.get('location', '')
    if not location:
        if current_user.is_authenticated and current_user.location:
            location = current_user.location
        else:
            return jsonify({'error': 'No location provided'}), 400
    
    weather_data = get_weather_for_location(location)
    
    # Get language for recommendations
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    
    # Get farm type for targeted recommendations
    farm_type = None
    if current_user.is_authenticated:
        farm_type = current_user.farm_type
    
    recommendations = get_weather_recommendations(weather_data, farm_type, lang)
    
    return jsonify({
        'weather': weather_data,
        'recommendations': recommendations
    })


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    return render_template('404.html', lang=lang), 404


@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {e}")
    lang = session.get('language', 'en')
    if current_user.is_authenticated:
        lang = current_user.preferred_language or lang
    return render_template('500.html', lang=lang), 500


#
# Farmer Chat (Community Chat) Routes
#

@app.route('/community-chat')
@login_required
def community_chat():
    """Farmer community chat page"""
    lang = current_user.preferred_language or session.get('language', 'en')
    
    # Get user's chat rooms
    user_rooms = current_user.chat_rooms
    
    # Get public chat rooms
    public_rooms = FarmerChatRoom.query.filter_by(is_group=True).all()
    
    # Get extension officers
    extension_officers = User.query.filter_by(is_extension_officer=True).all()
    
    # Get buyers/aggregators
    buyers = User.query.filter_by(is_buyer=True).all()
    
    return render_template('community_chat.html',
                          lang=lang,
                          user_rooms=user_rooms,
                          public_rooms=public_rooms,
                          extension_officers=extension_officers,
                          buyers=buyers,
                          title=get_translation("Farmer Community Chat", lang))


@app.route('/community-chat/rooms', methods=['GET'])
@login_required
def get_chat_rooms():
    """Get chat rooms for the current user"""
    user_rooms = current_user.chat_rooms
    
    rooms_list = []
    for room in user_rooms:
        # Get the last message in the room
        last_message = FarmerChatMessage.query.filter_by(chat_room_id=room.id).order_by(FarmerChatMessage.created_at.desc()).first()
        
        # Get other participants for private chats
        other_participants = []
        if not room.is_group:
            other_participants = [user for user in room.participants if user.id != current_user.id]
        
        rooms_list.append({
            'id': room.id,
            'name': room.name,
            'is_group': room.is_group,
            'topic': room.topic,
            'created_at': room.created_at.strftime('%Y-%m-%d %H:%M'),
            'last_message': last_message.message[:50] + '...' if last_message and len(last_message.message) > 50 else (last_message.message if last_message else None),
            'last_message_time': last_message.created_at.strftime('%Y-%m-%d %H:%M') if last_message else None,
            'participants': [{'id': user.id, 'username': user.username} for user in other_participants] if not room.is_group else None
        })
    
    return jsonify({'rooms': rooms_list})


@app.route('/community-chat/rooms/<int:room_id>/messages', methods=['GET'])
@login_required
def get_chat_messages(room_id):
    """Get messages for a specific chat room"""
    # Check if user is a participant in the room
    room = FarmerChatRoom.query.get_or_404(room_id)
    if current_user not in room.participants:
        return jsonify({'error': 'You are not a participant in this chat room'}), 403
    
    # Get messages in the room
    messages = FarmerChatMessage.query.filter_by(chat_room_id=room_id).order_by(FarmerChatMessage.created_at).all()
    
    messages_list = []
    for message in messages:
        messages_list.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_name': message.sender.username,
            'message': message.message,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_mine': message.sender_id == current_user.id
        })
    
    return jsonify({
        'messages': messages_list,
        'room': {
            'id': room.id,
            'name': room.name,
            'is_group': room.is_group,
            'topic': room.topic,
            'participants': [{'id': user.id, 'username': user.username} for user in room.participants]
        }
    })


@app.route('/community-chat/rooms/<int:room_id>/messages', methods=['POST'])
@login_required
def send_chat_message(room_id):
    """Send a message to a chat room"""
    # Check if user is a participant in the room
    room = FarmerChatRoom.query.get_or_404(room_id)
    if current_user not in room.participants:
        return jsonify({'error': 'You are not a participant in this chat room'}), 403
    
    message_text = request.form.get('message', '')
    if not message_text:
        return jsonify({'error': 'No message provided'}), 400
    
    # Create new message
    new_message = FarmerChatMessage(
        chat_room_id=room_id,
        sender_id=current_user.id,
        message=message_text,
        created_at=datetime.utcnow(),
        is_read=False
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': {
            'id': new_message.id,
            'sender_id': new_message.sender_id,
            'sender_name': current_user.username,
            'message': new_message.message,
            'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_mine': True
        }
    })


@app.route('/community-chat/rooms', methods=['POST'])
@login_required
def create_chat_room():
    """Create a new chat room"""
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    is_group = request.form.get('is_group', 'false').lower() == 'true'
    topic = request.form.get('topic', '')
    participant_ids = request.form.getlist('participants[]')
    
    if not name:
        return jsonify({'error': 'Room name is required'}), 400
    
    # Create new chat room
    new_room = FarmerChatRoom(
        name=name,
        description=description,
        is_group=is_group,
        created_at=datetime.utcnow(),
        created_by_id=current_user.id,
        topic=topic
    )
    
    # Add current user as participant
    new_room.participants.append(current_user)
    
    # Add other participants
    if participant_ids:
        for user_id in participant_ids:
            user = User.query.get(int(user_id))
            if user and user != current_user:
                new_room.participants.append(user)
    
    db.session.add(new_room)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'room': {
            'id': new_room.id,
            'name': new_room.name,
            'is_group': new_room.is_group,
            'topic': new_room.topic,
            'created_at': new_room.created_at.strftime('%Y-%m-%d %H:%M'),
            'participants': [{'id': user.id, 'username': user.username} for user in new_room.participants]
        }
    })


@app.route('/community-chat/start-private-chat', methods=['POST'])
@login_required
def start_private_chat():
    """Start a private chat with another user"""
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    other_user = User.query.get_or_404(int(user_id))
    
    # Check if a private chat already exists between these users
    for room in current_user.chat_rooms:
        if not room.is_group and other_user in room.participants:
            return jsonify({
                'success': True,
                'room_id': room.id,
                'exists': True
            })
    
    # Create a new private chat room
    room_name = f"Chat with {other_user.username}"
    new_room = FarmerChatRoom(
        name=room_name,
        is_group=False,
        created_at=datetime.utcnow(),
        created_by_id=current_user.id
    )
    
    # Add both users as participants
    new_room.participants.append(current_user)
    new_room.participants.append(other_user)
    
    db.session.add(new_room)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'room_id': new_room.id,
        'exists': False
    })


@app.route('/users/extension-officers')
@login_required
def get_extension_officers():
    """Get a list of extension officers"""
    officers = User.query.filter_by(is_extension_officer=True).all()
    
    officers_list = []
    for officer in officers:
        officers_list.append({
            'id': officer.id,
            'username': officer.username,
            'location': officer.location
        })
    
    return jsonify({'officers': officers_list})


@app.route('/users/buyers')
@login_required
def get_buyers():
    """Get a list of agricultural buyers/aggregators"""
    buyers = User.query.filter_by(is_buyer=True).all()
    
    buyers_list = []
    for buyer in buyers:
        buyers_list.append({
            'id': buyer.id,
            'username': buyer.username,
            'location': buyer.location
        })
    
    return jsonify({'buyers': buyers_list})
