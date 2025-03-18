import os
import json
import logging

# Supported languages
LANGUAGES = {
    'en': 'English',
    'fr': 'Français',
    'es': 'Español',
    'sw': 'Kiswahili',
    'zh': '中文',
    'hi': 'हिन्दी',
    'ar': 'العربية',
    'pt': 'Português'
}

# Dictionary to store translations
translations = {}

# Basic translations for common phrases
# This can be extended or replaced with a more comprehensive translation system
BASIC_TRANSLATIONS = {
    'en': {
        'Welcome to Ulimi Wise': 'Welcome to Ulimi Wise',
        'Login': 'Login',
        'Register': 'Register',
        'Logout': 'Logout',
        'Dashboard': 'Dashboard',
        'Marketplace': 'Marketplace',
        'Farming Tips': 'Farming Tips',
        'Agricultural News': 'Agricultural News',
        'My Profile': 'My Profile',
        'Agricultural Assistant': 'Agricultural Assistant',
        'Weather': 'Weather',
        'Language': 'Language',
        'Search': 'Search',
        'Products': 'Products',
        'Add Product': 'Add Product',
        'Category': 'Category',
        'Price': 'Price',
        'Quantity': 'Quantity',
        'Seller': 'Seller',
        'Actions': 'Actions',
        'Edit': 'Edit',
        'Delete': 'Delete',
        'Save': 'Save',
        'Cancel': 'Cancel',
        'Submit': 'Submit',
        'Username': 'Username',
        'Email': 'Email',
        'Password': 'Password',
        'Confirm Password': 'Confirm Password',
        'Location': 'Location',
        'Farm Type': 'Farm Type',
        'Current Weather': 'Current Weather',
        'Temperature': 'Temperature',
        'Humidity': 'Humidity',
        'Wind': 'Wind',
        'Conditions': 'Conditions',
        'News': 'News',
        'Videos': 'Videos',
        'Podcasts': 'Podcasts',
        'Articles': 'Articles',
        'Read More': 'Read More',
        'Watch': 'Watch',
        'Listen': 'Listen',
        'No results found': 'No results found',
        'Loading...': 'Loading...',
        'Type your message here...': 'Type your message here...',
        'Send': 'Send',
        'Speak': 'Speak',
        'Invalid email or password': 'Invalid email or password',
        'Registration successful! Please login.': 'Registration successful! Please login.',
        'Profile updated successfully': 'Profile updated successfully',
        'Product added successfully': 'Product added successfully',
        'Product updated successfully': 'Product updated successfully',
        'Product deleted successfully': 'Product deleted successfully',
        'Invalid email format': 'Invalid email format',
        'Username or email already in use': 'Username or email already in use',
        'All fields marked with * are required': 'All fields marked with * are required',
        'Price and quantity must be numeric values': 'Price and quantity must be numeric values',
        'You can only update your own products': 'You can only update your own products',
        'You can only delete your own products': 'You can only delete your own products',
        'Current password is incorrect': 'Current password is incorrect',
        'No message provided': 'No message provided',
        'No text provided': 'No text provided',
        'No location provided': 'No location provided',
        'Weather data is not available. Please check your location settings.': 'Weather data is not available. Please check your location settings.'
    },
    'fr': {
        'Welcome to Ulimi Wise': 'Bienvenue sur Ulimi Wise',
        'Login': 'Connexion',
        'Register': 'S\'inscrire',
        'Logout': 'Déconnexion',
        'Dashboard': 'Tableau de bord',
        'Marketplace': 'Marché',
        'Farming Tips': 'Conseils agricoles',
        'Agricultural News': 'Actualités agricoles',
        'My Profile': 'Mon profil',
        'Agricultural Assistant': 'Assistant agricole',
        'Weather': 'Météo',
        'Language': 'Langue',
        'Search': 'Rechercher',
        'Products': 'Produits',
        'Add Product': 'Ajouter un produit',
        'Category': 'Catégorie',
        'Price': 'Prix',
        'Quantity': 'Quantité',
        'Seller': 'Vendeur',
        'Actions': 'Actions',
        'Edit': 'Modifier',
        'Delete': 'Supprimer',
        'Save': 'Enregistrer',
        'Cancel': 'Annuler',
        'Submit': 'Soumettre',
        'Username': 'Nom d\'utilisateur',
        'Email': 'Email',
        'Password': 'Mot de passe',
        'Confirm Password': 'Confirmer le mot de passe',
        'Location': 'Emplacement',
        'Farm Type': 'Type de ferme',
        'Current Weather': 'Météo actuelle',
        'Temperature': 'Température',
        'Humidity': 'Humidité',
        'Wind': 'Vent',
        'Conditions': 'Conditions',
        'News': 'Actualités',
        'Videos': 'Vidéos',
        'Podcasts': 'Podcasts',
        'Articles': 'Articles',
        'Read More': 'Lire plus',
        'Watch': 'Regarder',
        'Listen': 'Écouter',
        'No results found': 'Aucun résultat trouvé',
        'Loading...': 'Chargement...',
        'Type your message here...': 'Tapez votre message ici...',
        'Send': 'Envoyer',
        'Speak': 'Parler',
        'Invalid email or password': 'Email ou mot de passe invalide',
        'Registration successful! Please login.': 'Inscription réussie! Veuillez vous connecter.',
        'Profile updated successfully': 'Profil mis à jour avec succès',
        'Product added successfully': 'Produit ajouté avec succès',
        'Product updated successfully': 'Produit mis à jour avec succès',
        'Product deleted successfully': 'Produit supprimé avec succès',
        'Invalid email format': 'Format d\'email invalide',
        'Username or email already in use': 'Nom d\'utilisateur ou email déjà utilisé',
        'All fields marked with * are required': 'Tous les champs marqués d\'un * sont obligatoires',
        'Price and quantity must be numeric values': 'Le prix et la quantité doivent être des valeurs numériques',
        'You can only update your own products': 'Vous ne pouvez mettre à jour que vos propres produits',
        'You can only delete your own products': 'Vous ne pouvez supprimer que vos propres produits',
        'Current password is incorrect': 'Le mot de passe actuel est incorrect',
        'No message provided': 'Aucun message fourni',
        'No text provided': 'Aucun texte fourni',
        'No location provided': 'Aucun emplacement fourni',
        'Weather data is not available. Please check your location settings.': 'Les données météo ne sont pas disponibles. Veuillez vérifier vos paramètres de localisation.'
    },
    'es': {
        'Welcome to Ulimi Wise': 'Bienvenido a Ulimi Wise',
        'Login': 'Iniciar sesión',
        'Register': 'Registrarse',
        'Logout': 'Cerrar sesión',
        'Dashboard': 'Panel de control',
        'Marketplace': 'Mercado',
        'Farming Tips': 'Consejos agrícolas',
        'Agricultural News': 'Noticias agrícolas',
        'My Profile': 'Mi perfil',
        'Agricultural Assistant': 'Asistente agrícola',
        'Weather': 'Clima',
        'Language': 'Idioma',
        'Search': 'Buscar',
        'Products': 'Productos',
        'Add Product': 'Añadir producto',
        'Category': 'Categoría',
        'Price': 'Precio',
        'Quantity': 'Cantidad',
        'Seller': 'Vendedor',
        'Actions': 'Acciones',
        'Edit': 'Editar',
        'Delete': 'Eliminar',
        'Save': 'Guardar',
        'Cancel': 'Cancelar',
        'Submit': 'Enviar',
        'Username': 'Nombre de usuario',
        'Email': 'Correo electrónico',
        'Password': 'Contraseña',
        'Confirm Password': 'Confirmar contraseña',
        'Location': 'Ubicación',
        'Farm Type': 'Tipo de granja',
        'Current Weather': 'Clima actual',
        'Temperature': 'Temperatura',
        'Humidity': 'Humedad',
        'Wind': 'Viento',
        'Conditions': 'Condiciones',
        'News': 'Noticias',
        'Videos': 'Videos',
        'Podcasts': 'Podcasts',
        'Articles': 'Artículos',
        'Read More': 'Leer más',
        'Watch': 'Ver',
        'Listen': 'Escuchar',
        'No results found': 'No se encontraron resultados',
        'Loading...': 'Cargando...',
        'Type your message here...': 'Escribe tu mensaje aquí...',
        'Send': 'Enviar',
        'Speak': 'Hablar',
        'Invalid email or password': 'Correo o contraseña inválidos',
        'Registration successful! Please login.': '¡Registro exitoso! Por favor inicie sesión.',
        'Profile updated successfully': 'Perfil actualizado con éxito',
        'Product added successfully': 'Producto añadido con éxito',
        'Product updated successfully': 'Producto actualizado con éxito',
        'Product deleted successfully': 'Producto eliminado con éxito',
        'Invalid email format': 'Formato de correo electrónico inválido',
        'Username or email already in use': 'Nombre de usuario o correo electrónico ya en uso',
        'All fields marked with * are required': 'Todos los campos marcados con * son obligatorios',
        'Price and quantity must be numeric values': 'El precio y la cantidad deben ser valores numéricos',
        'You can only update your own products': 'Solo puedes actualizar tus propios productos',
        'You can only delete your own products': 'Solo puedes eliminar tus propios productos',
        'Current password is incorrect': 'La contraseña actual es incorrecta',
        'No message provided': 'No se proporcionó ningún mensaje',
        'No text provided': 'No se proporcionó ningún texto',
        'No location provided': 'No se proporcionó ninguna ubicación',
        'Weather data is not available. Please check your location settings.': 'Los datos meteorológicos no están disponibles. Por favor verifica tu configuración de ubicación.'
    },
    'sw': {
        'Welcome to Ulimi Wise': 'Karibu kwenye Ulimi Wise',
        'Login': 'Ingia',
        'Register': 'Jisajili',
        'Logout': 'Toka',
        'Dashboard': 'Dashibodi',
        'Marketplace': 'Soko',
        'Farming Tips': 'Vidokezo vya Kilimo',
        'Agricultural News': 'Habari za Kilimo',
        'My Profile': 'Wasifu Wangu',
        'Agricultural Assistant': 'Msaidizi wa Kilimo',
        'Weather': 'Hali ya Hewa',
        'Language': 'Lugha',
        'Search': 'Tafuta',
        'Products': 'Bidhaa',
        'Add Product': 'Ongeza Bidhaa',
        'Category': 'Kategoria',
        'Price': 'Bei',
        'Quantity': 'Kiasi',
        'Seller': 'Muuzaji',
        'Actions': 'Vitendo',
        'Edit': 'Hariri',
        'Delete': 'Futa',
        'Save': 'Hifadhi',
        'Cancel': 'Ghairi',
        'Submit': 'Wasilisha',
        'Username': 'Jina la mtumiaji',
        'Email': 'Barua pepe',
        'Password': 'Nywila',
        'Confirm Password': 'Thibitisha Nywila',
        'Location': 'Mahali',
        'Farm Type': 'Aina ya Shamba',
        'Current Weather': 'Hali ya Hewa ya Sasa',
        'Temperature': 'Joto',
        'Humidity': 'Unyevu',
        'Wind': 'Upepo',
        'Conditions': 'Hali',
        'News': 'Habari',
        'Videos': 'Video',
        'Podcasts': 'Podikasti',
        'Articles': 'Makala',
        'Read More': 'Soma Zaidi',
        'Watch': 'Tazama',
        'Listen': 'Sikiliza',
        'No results found': 'Hakuna matokeo yaliyopatikana',
        'Loading...': 'Inapakia...',
        'Type your message here...': 'Andika ujumbe wako hapa...',
        'Send': 'Tuma',
        'Speak': 'Ongea',
        'Invalid email or password': 'Barua pepe au nywila si sahihi',
        'Registration successful! Please login.': 'Usajili umefanikiwa! Tafadhali ingia.',
        'Profile updated successfully': 'Wasifu umesasishwa kwa mafanikio',
        'Product added successfully': 'Bidhaa imeongezwa kwa mafanikio',
        'Product updated successfully': 'Bidhaa imesasishwa kwa mafanikio',
        'Product deleted successfully': 'Bidhaa imefutwa kwa mafanikio',
        'Invalid email format': 'Muundo wa barua pepe si sahihi',
        'Username or email already in use': 'Jina la mtumiaji au barua pepe tayari inatumika',
        'All fields marked with * are required': 'Sehemu zote zilizowekwa alama ya * zinahitajika',
        'Price and quantity must be numeric values': 'Bei na kiasi lazima viwe ni nambari',
        'You can only update your own products': 'Unaweza kuhariri bidhaa zako tu',
        'You can only delete your own products': 'Unaweza kufuta bidhaa zako tu',
        'Current password is incorrect': 'Nywila ya sasa si sahihi',
        'No message provided': 'Hakuna ujumbe uliotolewa',
        'No text provided': 'Hakuna maandishi yaliyotolewa',
        'No location provided': 'Hakuna mahali palipotolewa',
        'Weather data is not available. Please check your location settings.': 'Data ya hali ya hewa haipatikani. Tafadhali angalia mpangilio wako wa mahali.'
    }
}


def load_translations():
    """
    Load translations from file or initialize with basic translations
    """
    global translations
    
    try:
        # Try to load translations from file
        if os.path.exists('translations.json'):
            with open('translations.json', 'r', encoding='utf-8') as f:
                translations = json.load(f)
                logging.info("Translations loaded from file")
        else:
            # Use basic translations
            translations = BASIC_TRANSLATIONS
            logging.info("Using basic translations")
    except Exception as e:
        logging.error(f"Error loading translations: {str(e)}")
        translations = BASIC_TRANSLATIONS


def get_translation(text, lang_code='en'):
    """
    Get the translation of a text in the specified language
    
    Args:
        text (str): Text to translate
        lang_code (str): Language code
    
    Returns:
        str: Translated text or original text if translation not found
    """
    # Ensure translations are loaded
    if not translations:
        load_translations()
    
    # Default to English if the language is not supported
    if lang_code not in LANGUAGES:
        lang_code = 'en'
    
    # Return the translation if available, otherwise return the original text
    if lang_code in translations and text in translations[lang_code]:
        return translations[lang_code][text]
    else:
        return text


def get_available_languages():
    """
    Get the list of available languages
    
    Returns:
        dict: Dictionary of language codes and names
    """
    return LANGUAGES


# Load translations when module is imported
load_translations()
