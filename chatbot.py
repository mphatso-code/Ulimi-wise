import re
import random
import logging
from translations import get_translation

# Dictionary of keywords and responses for common farming questions
FARMING_RESPONSES = {
    'crop': {
        'plant': "The best time to plant {crop} is during {season}. Make sure soil is {soil_condition} and provide adequate {water_condition}.",
        'fertilize': "For {crop}, use {fertilizer_type} fertilizer. Apply every {frequency} for best results.",
        'pest': "Common pests for {crop} include {pests}. Use {solution} to manage them effectively.",
        'harvest': "Harvest {crop} when {harvest_condition}. Store in {storage_condition} for optimal freshness."
    },
    'soil': {
        'type': "There are several soil types including sandy, clay, silt, loamy, and chalky. Each has different characteristics for farming.",
        'improve': "Improve your soil by adding organic matter, proper drainage, and regular testing. Crop rotation also helps maintain soil health.",
        'test': "Soil testing helps determine pH, nutrient levels, and organic content. It's recommended to test your soil annually."
    },
    'water': {
        'irrigation': "Irrigation methods include drip, sprinkler, furrow, and flood. Choose based on your crop, soil type, and water availability.",
        'conservation': "Conserve water through mulching, rainwater harvesting, and efficient irrigation scheduling.",
        'quality': "Water quality affects crop growth. Check for salt content, pH, and contaminants regularly."
    },
    'livestock': {
        'feed': "Proper livestock feed should include balanced nutrition with proteins, carbohydrates, vitamins, and minerals.",
        'shelter': "Livestock shelter should protect from extreme weather, predators, and provide adequate ventilation.",
        'health': "Regular health checks, vaccinations, and good sanitation are essential for livestock well-being."
    },
    'market': {
        'price': "Market prices fluctuate based on supply, demand, season, and quality. Check local agricultural boards for current rates.",
        'sell': "Consider direct marketing, farmers markets, cooperatives, or contracts with processors for selling your produce.",
        'storage': "Proper storage extends shelf life. Different products require specific temperature, humidity, and handling."
    },
    'organic': {
        'certification': "Organic certification requires following specific standards, documentation, and inspection by authorized agencies.",
        'practice': "Organic practices include natural pest control, composting, crop rotation, and avoiding synthetic chemicals.",
        'benefits': "Benefits of organic farming include soil health, biodiversity, reduced chemical exposure, and potential premium prices."
    }
}

# Common crop types and their specific information
CROP_INFO = {
    'maize': {
        'season': 'spring or early summer',
        'soil_condition': 'well-drained and fertile',
        'water_condition': 'regular watering, especially during tasseling and silking',
        'fertilizer_type': 'nitrogen-rich',
        'frequency': '2-3 weeks',
        'pests': 'corn borers, armyworms, and rootworms',
        'solution': 'integrated pest management and resistant varieties',
        'harvest_condition': 'the husks are dry and kernels are firm'
    },
    'rice': {
        'season': 'wet season or with irrigation',
        'soil_condition': 'clay-rich with good water retention',
        'water_condition': 'flooded conditions for most varieties',
        'fertilizer_type': 'balanced NPK',
        'frequency': 'before planting and at tillering stage',
        'pests': 'stem borers, plant hoppers, and rice bugs',
        'solution': 'crop rotation and timely application of appropriate pesticides',
        'harvest_condition': 'the grains are golden yellow and moisture content is around 20-25%'
    },
    'wheat': {
        'season': 'fall for winter wheat, spring for spring wheat',
        'soil_condition': 'loamy and well-drained',
        'water_condition': 'moderate moisture throughout growing season',
        'fertilizer_type': 'nitrogen with some phosphorus and potassium',
        'frequency': 'at planting and jointing stages',
        'pests': 'aphids, Hessian flies, and various rusts',
        'solution': 'resistant varieties and appropriate fungicides',
        'harvest_condition': 'the stalks turn golden and grain is hard'
    },
    'tomato': {
        'season': 'after last frost when soil is warm',
        'soil_condition': 'rich, well-drained with pH 6.0-6.8',
        'water_condition': 'consistent moisture, avoid wetting foliage',
        'fertilizer_type': 'phosphorus-rich at flowering',
        'frequency': 'every 4-6 weeks',
        'pests': 'hornworms, whiteflies, and early blight',
        'solution': 'crop rotation, stakes for air circulation, and appropriate fungicides',
        'harvest_condition': 'fruits are firm and fully colored'
    },
    'potato': {
        'season': 'early spring or fall in warmer regions',
        'soil_condition': 'loose, well-drained, slightly acidic',
        'water_condition': 'consistent moisture, especially during tuber formation',
        'fertilizer_type': 'balanced with higher potassium',
        'frequency': 'at planting and hilling',
        'pests': 'Colorado potato beetles, wireworms, and late blight',
        'solution': 'crop rotation, healthy seed potatoes, and proper hilling',
        'harvest_condition': 'vines have died back and skins are set'
    }
}

# Default responses when no match is found
DEFAULT_RESPONSES = [
    "I'm sorry, I don't have information about that farming topic. Could you ask about crops, soil, water, livestock, market prices, or organic farming?",
    "I'm not sure I understood your farming question. Can you rephrase it or ask about a specific crop or farming practice?",
    "I don't have data on that topic yet. Would you like information about planting, fertilizing, pest control, or harvesting specific crops?"
]

def process_message(message, lang='en'):
    """
    Process the user message and return an appropriate response
    
    Args:
        message (str): User's message/question
        lang (str): Language code for translation
    
    Returns:
        str: Response to the user's message
    """
    message = message.lower()
    
    # Check for greetings
    if any(greeting in message for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return get_translation("Hello! I'm your agricultural assistant. How can I help with your farming questions today?", lang)
    
    # Check for thanks
    if any(thanks in message for thanks in ['thank', 'thanks', 'appreciate']):
        return get_translation("You're welcome! Feel free to ask if you have any other farming questions.", lang)
    
    # Check for goodbye
    if any(bye in message for bye in ['bye', 'goodbye', 'see you']):
        return get_translation("Goodbye! Happy farming and come back anytime you need agricultural advice.", lang)
    
    # Check for weather-related questions
    if any(weather in message for weather in ['weather', 'rain', 'temperature', 'forecast']):
        return get_translation("For weather information, please check the weather section on your dashboard. I can help with farming advice based on weather conditions.", lang)
    
    # Check for marketplace questions
    if any(market in message for market in ['buy', 'sell', 'price', 'market']):
        if 'buy' in message or 'sell' in message:
            return get_translation("You can buy or sell agricultural products in our marketplace section. Check it out to list your products or find what you need.", lang)
        else:
            return get_translation(FARMING_RESPONSES['market']['price'], lang)
    
    # Check for specific crop information
    for crop in CROP_INFO.keys():
        if crop in message:
            if 'plant' in message or 'grow' in message:
                response = FARMING_RESPONSES['crop']['plant'].format(
                    crop=crop,
                    season=CROP_INFO[crop]['season'],
                    soil_condition=CROP_INFO[crop]['soil_condition'],
                    water_condition=CROP_INFO[crop]['water_condition']
                )
                return get_translation(response, lang)
            elif 'fertilize' in message or 'nutrient' in message:
                response = FARMING_RESPONSES['crop']['fertilize'].format(
                    crop=crop,
                    fertilizer_type=CROP_INFO[crop]['fertilizer_type'],
                    frequency=CROP_INFO[crop]['frequency']
                )
                return get_translation(response, lang)
            elif 'pest' in message or 'disease' in message or 'insect' in message:
                response = FARMING_RESPONSES['crop']['pest'].format(
                    crop=crop,
                    pests=CROP_INFO[crop]['pests'],
                    solution=CROP_INFO[crop]['solution']
                )
                return get_translation(response, lang)
            elif 'harvest' in message or 'collect' in message:
                response = FARMING_RESPONSES['crop']['harvest'].format(
                    crop=crop,
                    harvest_condition=CROP_INFO[crop]['harvest_condition'],
                    storage_condition="a cool, dry place"  # Default storage condition
                )
                return get_translation(response, lang)
            else:
                # General information about the crop
                response = f"I have information about {crop}. You can ask about planting, fertilizing, pest control, or harvesting this crop."
                return get_translation(response, lang)
    
    # Check for soil-related questions
    if 'soil' in message:
        if any(word in message for word in ['type', 'kind', 'different']):
            return get_translation(FARMING_RESPONSES['soil']['type'], lang)
        elif any(word in message for word in ['improve', 'better', 'enhance']):
            return get_translation(FARMING_RESPONSES['soil']['improve'], lang)
        elif any(word in message for word in ['test', 'analyze', 'check']):
            return get_translation(FARMING_RESPONSES['soil']['test'], lang)
        else:
            return get_translation("Soil health is fundamental to successful farming. What specific aspect of soil management would you like to know about?", lang)
    
    # Check for water-related questions
    if any(word in message for word in ['water', 'irrigation', 'moisture']):
        if 'irrigation' in message or 'system' in message or 'method' in message:
            return get_translation(FARMING_RESPONSES['water']['irrigation'], lang)
        elif any(word in message for word in ['save', 'conserve', 'shortage']):
            return get_translation(FARMING_RESPONSES['water']['conservation'], lang)
        elif any(word in message for word in ['quality', 'pure', 'clean']):
            return get_translation(FARMING_RESPONSES['water']['quality'], lang)
        else:
            return get_translation("Water management is crucial for crop success. Would you like to know about irrigation methods, water conservation, or water quality?", lang)
    
    # Check for livestock-related questions
    if any(word in message for word in ['animal', 'livestock', 'cattle', 'poultry', 'pig', 'sheep', 'goat']):
        if any(word in message for word in ['feed', 'food', 'nutrition']):
            return get_translation(FARMING_RESPONSES['livestock']['feed'], lang)
        elif any(word in message for word in ['house', 'shelter', 'barn', 'pen']):
            return get_translation(FARMING_RESPONSES['livestock']['shelter'], lang)
        elif any(word in message for word in ['health', 'disease', 'sick', 'veterinary']):
            return get_translation(FARMING_RESPONSES['livestock']['health'], lang)
        else:
            return get_translation("I can provide information about livestock care. What specific aspect do you want to know about - feeding, shelter, or health?", lang)
    
    # Check for organic farming questions
    if 'organic' in message:
        if any(word in message for word in ['certify', 'certification', 'certified']):
            return get_translation(FARMING_RESPONSES['organic']['certification'], lang)
        elif any(word in message for word in ['practice', 'method', 'how to']):
            return get_translation(FARMING_RESPONSES['organic']['practice'], lang)
        elif any(word in message for word in ['benefit', 'advantage', 'why']):
            return get_translation(FARMING_RESPONSES['organic']['benefits'], lang)
        else:
            return get_translation("Organic farming focuses on ecological balance and minimal synthetic inputs. What specific aspect of organic farming are you interested in?", lang)
    
    # Default response if no pattern matches
    return get_translation(random.choice(DEFAULT_RESPONSES), lang)
