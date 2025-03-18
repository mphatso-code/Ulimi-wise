"""
Script to add farming tips for different farm types in Malawi
"""
from app import app, db
from models import FarmingTip, MediaResource, CropCalendar
from datetime import datetime

def add_crop_farming_tips():
    """Add tips for crop farming in Malawi"""
    tips = [
        {
            'title': 'Conservation Agriculture for Maize in Malawi',
            'content': """Conservation agriculture is a sustainable approach to maize farming in Malawi that can improve soil health and crop yields while reducing labor requirements.

1. Land Preparation: 
Adopt minimum tillage practices instead of conventional plowing. Create planting stations or basins using a hoe, disturbing only the soil where seeds will be planted. This preserves soil structure and reduces erosion.

2. Crop Residue Management:
Leave at least 30% of crop residues on the field after harvest. This creates a protective layer that conserves soil moisture, suppresses weeds, adds organic matter, and reduces erosion.

3. Crop Rotation:
Rotate maize with legumes such as groundnuts, soybeans, or pigeon peas. Legumes fix nitrogen in the soil, reducing the need for fertilizers and breaking pest and disease cycles.

4. Timely Planting:
Plant with the first effective rains (typically November-December) to maximize growing season length. Early planted maize often yields better than late-planted crops.

5. Proper Spacing:
For improved varieties, use 75cm between rows and 25cm between plants with one seed per station. This optimal spacing ensures better utilization of sunlight, water, and nutrients.

6. Fertilizer Application:
Apply basal fertilizer (NPK) during planting, placing it 5cm away from the seed. Apply top dressing (urea) when maize is knee-high, placing it 5cm from the plant and covering lightly with soil. Follow recommended rates based on soil type.

7. Weed Management:
Control weeds early when they are small. Use targeted hoeing around planting stations rather than disturbing the entire field. Consider mulching to suppress weed growth.

8. Pest Management:
Regularly scout fields for fall armyworm, a major threat to maize in Malawi. Apply recommended pesticides when necessary, following safety guidelines and proper application rates.

9. Harvest and Storage:
Harvest when grain is mature (black layer formed at base of kernels). Ensure proper drying to 12-13% moisture before storage to prevent mold. Use improved storage structures like metal silos to reduce post-harvest losses.

10. Market Considerations:
Consider joining farmer cooperatives to access better markets and negotiate higher prices. Explore value addition options like processing maize into flour to increase profits.""",
            'category': 'maize',
            'season': 'rainy',
            'region': 'Malawi',
            'farm_type': 'crops',
            'image_url': '/static/images/crops/maize.svg'
        },
        {
            'title': 'Sustainable Rice Farming Practices for Malawi',
            'content': """Rice is an important food security crop in Malawi, particularly in lowland areas with adequate water. Here are sustainable practices for successful rice farming:

1. Variety Selection:
Choose varieties suited to your specific growing conditions. For rainfed lowland areas, varieties like Kilombero and Faya are popular. For irrigated systems, consider high-yielding varieties developed by the Africa Rice Center.

2. Nursery Preparation:
Prepare a raised seedbed in a sunny location. Mix soil with well-decomposed compost. Soak seeds for 24 hours before sowing. Maintain adequate moisture in the nursery.

3. Land Preparation:
Level the field properly to ensure uniform water distribution. For lowland rice, puddle the soil to reduce water percolation and create ideal conditions for rice growth.

4. Transplanting:
Transplant seedlings when they are 21-25 days old. Use 2-3 seedlings per hill with spacing of 20cm between hills and 25cm between rows. Transplant in straight rows to facilitate weeding and other operations.

5. Water Management:
Maintain 2-5cm water depth during the vegetative and reproductive stages. Practice alternate wetting and drying to save water while maintaining yields.

6. Nutrient Management:
Apply basal fertilizer (NPK) before transplanting. Apply nitrogen fertilizer in split doses - at transplanting, tillering, and panicle initiation stages. Consider incorporating green manure crops or compost to improve soil fertility.

7. Weed Management:
Ensure proper land preparation and water management to suppress weeds. Hand weed within 20-30 days after transplanting. Consider using rotary weeders in rows for more efficient weeding.

8. Pest and Disease Management:
Monitor fields regularly for rice stem borers, African rice gall midge, and blast disease. Practice field sanitation and crop rotation to reduce pest pressure. Apply recommended pesticides only when necessary.

9. Harvesting:
Harvest when 80-85% of grains are golden yellow. Cut the crop close to the ground, then threshed and cleaned properly. Dry rice to 14% moisture content for safe storage.

10. Post-harvest Handling:
Use improved storage facilities to prevent moisture absorption and pest infestation. Consider parboiling rice to improve nutritional value and reduce breakage during milling.""",
            'category': 'rice',
            'season': 'rainy',
            'region': 'Malawi',
            'farm_type': 'crops',
            'image_url': '/static/images/crops/rice.svg'
        },
        {
            'title': 'Groundnut Farming Best Practices for Malawi',
            'content': """Groundnuts (peanuts) are an important legume crop in Malawi, providing both food security and income. Here are best practices for successful groundnut cultivation:

1. Land Selection and Preparation:
Choose well-drained, sandy loam or loamy soils with pH 5.5-7.0. Avoid fields where groundnuts were grown in the previous season. Prepare a fine tilth with adequate soil moisture for good germination.

2. Variety Selection:
Select improved varieties suited to your region. In Malawi, popular varieties include CG7, Nsinjiro, and Chalimbana, which offer higher yields and disease resistance. Select seed from certified sources.

3. Planting:
Plant at the onset of consistent rains (November-December). Use spacing of 75cm between ridges and 15cm between plants. Plant seeds 3-5cm deep. Shell groundnuts just before planting to maintain viability.

4. Soil Fertility Management:
Groundnuts fix nitrogen but require adequate phosphorus and calcium. Apply single superphosphate or NPK (23:21:0+4S) at planting. Avoid excessive nitrogen which promotes vegetative growth at the expense of pod development.

5. Weed Management:
Keep fields weed-free, especially during the first 6-8 weeks. Hand weed carefully to avoid damaging developing pegs and pods. Consider using pre-emergence herbicides in larger fields.

6. Earthing Up:
Perform earthing up (adding soil to the base of plants) at flowering to provide loose soil for pegging and pod development. This enhances pod filling and reduces pod rot.

7. Pest and Disease Management:
Monitor for aphids, thrips, and leaf spots. Practice crop rotation to reduce disease pressure. Remove and destroy infected plants. Rosette virus, spread by aphids, is a major threat - control aphids early and use resistant varieties.

8. Harvest Management:
Harvest when plants show maturity signs: yellowing leaves, pods with visible veins, and darkened inner pod walls. Dig carefully to avoid leaving pods in the soil. Dry pods thoroughly to 8-10% moisture for safe storage.

9. Post-harvest Handling:
Dry harvested plants with pods attached for 3-5 days. Strip pods and continue drying until they rattle when shaken. Store in dry, well-ventilated conditions to prevent aflatoxin contamination.

10. Value Addition:
Consider processing groundnuts into peanut butter, oil, or flour to increase profits. Join farmer groups to access better markets and processing equipment.""",
            'category': 'groundnuts',
            'season': 'rainy',
            'region': 'Malawi',
            'farm_type': 'crops',
            'image_url': '/static/images/crops/groundnuts.svg'
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} crop farming tips")


def add_livestock_farming_tips():
    """Add tips for livestock farming in Malawi"""
    tips = [
        {
            'title': 'Sustainable Dairy Farming in Malawi',
            'content': """Dairy farming offers significant opportunities for smallholder farmers in Malawi to generate regular income while improving household nutrition. Here are key practices for successful dairy farming:

1. Breed Selection:
Choose appropriate breeds based on your resources and climate. Holstein-Friesian and Jersey crosses with local breeds offer good milk production while maintaining some resistance to local conditions. Pure exotic breeds require more intensive management.

2. Housing:
Construct a well-ventilated, clean shelter with proper drainage. The housing should protect animals from extreme weather while allowing adequate airflow. Provide at least 4 square meters per animal with access to an exercise yard.

3. Feeding Management:
Provide adequate nutrition through a combination of:
- High-quality forage (Napier grass, Rhodes grass, or natural pasture)
- Protein supplements (legume fodder like Leucaena or Calliandra)
- Concentrate feeds for lactating cows (16-18% protein)
- Mineral supplements and clean water at all times

4. Fodder Establishment:
Establish fodder plots on your farm to ensure year-round feed supply. Plant Napier grass in rows 90cm apart. Harvest when 1-1.5m tall for optimal nutrition. Consider silage making for dry season feeding.

5. Breeding:
Use artificial insemination for genetic improvement when available. Keep records of heat cycles (typically every 21 days). Inseminate cows 12-18 hours after onset of standing heat. Maintain a calving interval of 12-14 months for optimal production.

6. Calf Rearing:
Ensure calves receive colostrum within the first 6 hours after birth. Feed calves 4-5 liters of milk daily for the first 2-3 months. Introduce calf starter feed from week 2 and good quality forage from week 3. Wean gradually between 3-4 months.

7. Milking Hygiene:
Practice clean milking procedures:
- Wash hands before milking
- Clean the udder with warm water
- Dry udder with clean cloth
- Use strip cup to check for mastitis
- Apply post-milking teat dip
- Filter milk immediately after collection
- Cool milk quickly to 4°C if not sold immediately

8. Health Management:
Implement a regular vaccination program for common diseases (anthrax, black quarter, foot and mouth disease). Deworm animals every 3-4 months. Monitor for mastitis by regular udder checks. Isolate sick animals promptly.

9. Record Keeping:
Maintain records of milk production, breeding dates, health treatments, and expenses. This helps in monitoring performance and making management decisions.

10. Marketing:
Consider joining dairy cooperatives for reliable milk collection and better prices. Explore value addition through production of yogurt, cheese, or cultured milk to increase profitability.""",
            'category': 'dairy cattle',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'livestock',
            'image_url': None
        },
        {
            'title': 'Goat Rearing Best Practices for Malawi',
            'content': """Goat farming is particularly suitable for smallholder farmers in Malawi due to goats' adaptability, lower feed requirements, and faster reproduction rate compared to cattle. Here are essential practices for successful goat rearing:

1. Breed Selection:
Choose breeds based on your production goals and resources. For meat production, Boer goats or their crosses perform well. For milk, consider Saanen or Alpine breeds. Local breeds like Malawi goats are hardy but have lower production.

2. Housing:
Construct a simple raised shelter (0.5m above ground) with slatted floors for easy cleaning. Allow 1.5-2 square meters per adult goat. Ensure good ventilation, protection from rain, and security from predators. Orient the shelter with openings away from prevailing winds.

3. Feeding Management:
Provide a combination of:
- Browse plants (goats prefer browsing on shrubs and tree leaves)
- Forage/pasture access for 4-6 hours daily
- Supplementary feeds for pregnant and lactating does
- Mineral licks or salt blocks
- Clean water at all times

Establish fodder trees like Leucaena, Sesbania, and Gliricidia on farm boundaries for sustainable feed supply.

4. Breeding:
Introduce bucks to does when does reach 7-8 months of age (or 60% of adult weight). Keep one buck for 20-25 does. Separate bucks from does when not breeding to avoid unplanned pregnancies. Does come into heat every 21 days, with pregnancy lasting about 150 days.

5. Kid Management:
Ensure kids receive colostrum within 1 hour of birth. Provide adequate nutrition to nursing does to support milk production. Introduce solid feed to kids from 2 weeks of age. Wean kids at 3-4 months of age.

6. Health Management:
Implement a regular vaccination program for common diseases like Peste des Petits Ruminants (PPR) and Contagious Caprine Pleuropneumonia (CCPP). Deworm every 3-4 months, more frequently for kids. Check hooves regularly and trim when necessary to prevent foot rot.

7. Parasite Control:
External parasites like ticks and mites are common in goats. Regularly inspect animals and treat with appropriate parasiticides. Rotate grazing areas to reduce internal parasite loads. Consider strategic deworming before rainy seasons.

8. Disease Prevention:
Practice good biosecurity:
- Quarantine new animals for 2-3 weeks before introducing to the flock
- Clean housing regularly
- Isolate sick animals promptly
- Disinfect equipment
- Control visitors to goat pens

9. Record Keeping:
Maintain records of breeding dates, kidding, health treatments, and weights. This helps track performance and identify productive animals for breeding stock.

10. Marketing:
Time sales to coincide with periods of peak demand (religious festivals, holiday seasons). Consider value addition such as processing goat meat into products like sausages or smoked meat. Explore dairy goat farming for milk production which can yield premium prices.""",
            'category': 'goats',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'livestock',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} livestock farming tips")


def add_poultry_farming_tips():
    """Add tips for poultry farming in Malawi"""
    tips = [
        {
            'title': 'Profitable Chicken Rearing in Malawi',
            'content': """Poultry farming offers Malawian farmers a relatively low-investment opportunity with quick returns. Here are key practices for successful chicken production:

1. Poultry System Selection:
Choose a production system based on your resources and goals:
- Free-range/village system: Low input, using local breeds, suitable for rural households
- Semi-intensive: Chickens housed at night but allowed outside during day, medium production
- Intensive: Full confinement with complete feeds, higher production costs but better returns

2. Breed Selection:
For meat (broilers): Cobb, Ross, or Hubbard breeds grow rapidly, reaching market weight in 6-8 weeks.
For eggs (layers): White Leghorn, Isa Brown, or Lohmann Brown produce 250-300 eggs annually.
For dual-purpose: Rhode Island Red, Black Australorp, or Kuroiler perform well in semi-intensive systems.
For local production: Consider improved local breeds that maintain some hardiness while offering better production.

3. Housing:
Construct housing facing east-west to minimize sun exposure. Allow adequate space:
- Layers: 4-5 birds per square meter
- Broilers: 8-10 birds per square meter initially, reducing to 5-7 as they grow
Ensure good ventilation, protection from predators, and easy cleaning. Provide appropriate perches and nesting boxes for layers.

4. Feeding:
Different stages require specific feeds:
- Chicks (0-8 weeks): Starter feed (20-22% protein)
- Growers (8-18 weeks): Grower feed (16-18% protein)
- Layers (18+ weeks): Layer feed (16-18% protein with added calcium)
- Broilers: Starter (22-24% protein) followed by finisher (18-20% protein)

Supplement commercial feeds with locally available ingredients when possible. Always provide clean, fresh water.

5. Day-Old Chick Management:
Prepare brooding area with:
- Temperature of 32-35°C in first week, reducing by 3°C weekly until reaching ambient temperature
- Clean, dry litter material (wood shavings, rice hulls)
- Proper lighting (24 hours initially, then reduced gradually for broilers)
- Adequate feeders and drinkers (one feeder per 25 chicks, one drinker per 50 chicks)

6. Health Management:
Implement a vaccination program against:
- Newcastle disease (most critical in Malawi)
- Infectious bronchitis
- Gumboro disease
- Fowl pox
- Fowl typhoid

Maintain strict biosecurity:
- Control visitor access
- Use footbaths with disinfectant
- Change clothes before handling birds
- Quarantine new birds for 2 weeks

7. Disease Prevention:
Practice all-in, all-out system where possible. Clean and disinfect housing between flocks. Remove sick or dead birds promptly. Maintain proper ventilation and avoid overcrowding.

8. Record Keeping:
Keep detailed records of:
- Feed consumption
- Egg production
- Mortality
- Vaccination schedule
- Costs and income

9. Marketing:
Develop reliable markets before scaling up production. Consider direct marketing to local hotels, restaurants, and households. Form producer groups to access larger markets and negotiate better prices.

10. Value Addition:
Consider processing chickens (dressing, packaging) or eggs (grading, packaging) to increase profit margins. Explore producing chicken manure compost as an additional income stream.""",
            'category': 'chicken',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'poultry',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} poultry farming tips")


def add_fish_farming_tips():
    """Add tips for fish farming in Malawi"""
    tips = [
        {
            'title': 'Sustainable Fish Farming in Malawi',
            'content': """Fish farming presents an excellent opportunity for Malawian farmers to improve food security and generate income. Lake Malawi's rich fish diversity provides unique aquaculture opportunities. Here are key practices for successful fish farming:

1. Site Selection:
Choose a location with:
- Reliable water supply year-round
- Gently sloping land (1-2%) for gravity drainage
- Clay or clay-loam soils that hold water
- Protection from flooding
- Accessibility for management and marketing
- Security from theft

2. Species Selection:
Choose appropriate fish species based on your farming goals:
- Tilapia (Oreochromis shiranus, O. karongae): Fast-growing, hardy, suitable for most systems
- Catfish (Clarias gariepinus): Tolerates poor water quality, high stocking densities
- Common carp: Omnivorous, good growth in fertilized ponds
Consider polyculture (multiple species) to maximize productivity.

3. Pond Construction:
For earthen ponds:
- Size: 200-500 m² for beginners
- Depth: 1m at shallow end, 1.5-2m at deep end
- Embankment: 1m wide at top, with 2:1 slope
- Include proper inlet and outlet structures
- Install anti-seepage measures if soil is porous
- Include anti-predator measures (fencing, netting)

4. Water Quality Management:
Maintain optimal conditions:
- Dissolved oxygen: Above 5 mg/L
- pH: 6.5-9.0
- Temperature: 25-30°C for tilapia
- Avoid excessive algae blooms through proper fertilization
- Monitor water color (greenish is ideal)
- Change 10-15% of water weekly or when needed

5. Stocking:
Follow recommended stocking rates:
- Tilapia: 2-3 fish/m² in fertilized ponds without supplementary feeding
- Tilapia: 5-10 fish/m² with regular supplementary feeding
- Catfish: 5-10 fish/m² with proper feeding and aeration
Stock uniformly sized fingerlings (5-10g) from reliable hatcheries.

6. Feeding:
Options include:
- Pond fertilization with animal manure to promote natural food (plankton)
- Supplementary feeding with locally available ingredients (maize bran, rice bran, soybean meal)
- Commercial feeds for intensive systems
Feed 2-3 times daily, adjusting quantity based on fish biomass (3-5% of total fish weight).

7. Harvest and Post-harvest:
Harvest methods:
- Complete harvest by draining the pond
- Partial harvest using nets to select larger fish
Process fish promptly after harvest:
- Clean with potable water
- Remove gills and internal organs if not selling immediately
- Keep on ice if available
- Smoke or sun-dry for preservation

8. Record Keeping:
Maintain records of:
- Stocking dates and quantities
- Feeding schedule and amounts
- Water quality parameters
- Growth sampling results
- Harvest data
- Costs and income

9. Marketing:
Develop marketing strategies:
- Time harvests for periods of high demand
- Build relationships with consistent buyers
- Consider value addition (smoking, filleting)
- Form marketing groups with other farmers

10. Integrated Aquaculture:
Consider integrating fish farming with:
- Vegetable production using pond water for irrigation
- Poultry with houses built over ponds
- Rice-fish culture in suitable areas
These integrated systems improve resource use efficiency and provide multiple income streams.""",
            'category': 'fish',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'fish',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} fish farming tips")


def add_fruit_farming_tips():
    """Add tips for fruit farming in Malawi"""
    tips = [
        {
            'title': 'Profitable Banana Cultivation in Malawi',
            'content': """Bananas are among the most important fruit crops in Malawi, offering farmers a steady income stream with year-round production. Here are key practices for successful banana cultivation:

1. Site Selection:
Choose a location with:
- Deep, well-drained loamy soils with pH 5.5-7.0
- Protection from strong winds
- Good access to water
- Temperatures between 20-35°C
- Rainfall of 1,200-2,500mm annually (or irrigation access)
- Altitude below 1,800m

2. Variety Selection:
Choose varieties based on your market and growing conditions:
- Cooking types: Harare, Zambia, Uganda Green
- Dessert types: Williams, Giant Cavendish, Grand Nain
- Beer types: Mzuzu Green, FHIA-25
Consider disease-resistant varieties where available.

3. Land Preparation:
Clear land of all weeds and debris. Dig planting holes:
- 60cm x 60cm x 60cm for good soils
- 90cm x 90cm x 90cm for poor soils
Space holes 3m x 3m for tall varieties and 2.5m x 2.5m for dwarf varieties.
Mix topsoil with 20kg well-decomposed manure or compost per hole.

4. Planting Material:
Use disease-free planting materials:
- Sword suckers (young plants with narrow leaves)
- Tissue culture plantlets from reputable nurseries
For sword suckers, trim off roots and any diseased parts, dip in insecticide solution before planting.
For tissue culture plantlets, harden them properly before field planting.

5. Planting:
Plant at the beginning of the rainy season for rainfed systems. Plant during any time of year if irrigation is available. Place the sucker/plantlet in the hole with the corm just below soil level. Compact soil around the plant. Water immediately after planting if soil is dry.

6. Water Management:
Bananas require consistent moisture:
- In rainfed systems, mulch heavily to conserve moisture
- In irrigated systems, provide 30-40 liters per plant weekly during dry periods
- Use drip irrigation where possible for efficiency
- Avoid waterlogging as it causes root rot

7. Sucker Management:
Maintain a mother-follower-grandchild system:
- Allow only one sucker (follower) to grow when the main plant (mother) is half-grown
- Allow a second sucker (grandchild) when the follower is half-grown
- Remove all other suckers to avoid competition
Select suckers growing opposite to the mother plant to establish a proper sequence.

8. Weed Control:
Keep a weed-free area 1m around each plant. Use mulch (dry grass, banana leaves) to suppress weeds and conserve moisture. Avoid deep cultivation near plants to prevent root damage.

9. Fertilizer Application:
Apply in split doses:
- Organic: 10-15kg of manure or compost per plant annually
- Inorganic: 250-300g of NPK (17:17:17) per plant in 3-4 split applications
- Apply additional 100g of urea when flower appears

10. Pest and Disease Management:
Monitor for banana weevil and nematodes. Practice field hygiene by removing old stems and fallen leaves. For bacterial wilt (a major threat), implement these measures:
- Use clean planting material
- Disinfect tools with bleach solution or flame
- Remove male flower buds with a forked stick
- Do not intercrop with crops that host the bacteria
- Remove and destroy infected plants immediately

11. Harvesting:
Harvest when fruits are mature but still green:
- Upper fruits show slight yellowing
- Angularity of fingers reduces
Cut the entire bunch, cushion during transportation to prevent bruising.

12. Marketing:
Consider direct marketing to local markets, hotels, and institutions. Join farmer groups for better market access. Explore value-added products like banana flour, chips, or wine.""",
            'category': 'banana',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'fruits',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} fruit farming tips")


def add_vegetable_farming_tips():
    """Add tips for vegetable farming in Malawi"""
    tips = [
        {
            'title': 'High-Value Tomato Production in Malawi',
            'content': """Tomatoes are a high-value horticultural crop in Malawi with strong market demand. With proper management, tomato farming can provide significant income for smallholder farmers. Here are key practices for successful tomato production:

1. Site Selection:
Choose a location with:
- Well-drained, fertile soils with pH 5.5-7.0
- Full sunlight (at least 6 hours daily)
- Access to reliable water for irrigation
- Protection from strong winds
- Away from previously solanaceous crop fields (tomato, potato, pepper) to minimize disease

2. Variety Selection:
Choose varieties based on your market and growing conditions:
- Fresh market: Rodade, Money Maker, Rio Grande, Tengeru
- Processing: Roma VF, Heinz, Rio Grande
- Heat-tolerant: Heatmaster, Summer Star
- Disease-resistant: Varieties with resistance to bacterial wilt, fusarium wilt, and tomato yellow leaf curl virus

3. Nursery Management:
Start seeds in nursery beds or trays:
- Use sterilized soil mixture (topsoil, compost, sand in 3:2:1 ratio)
- Sow seeds 1-2cm apart in rows 10cm apart
- Cover lightly with soil and mulch until germination
- Water gently using a watering can
- Provide shade for young seedlings
- Harden seedlings by reducing water and increasing sun exposure 7-10 days before transplanting

4. Land Preparation:
Thoroughly plow and harrow soil to achieve fine tilth. Prepare ridges 90-100cm apart or raised beds 100cm wide. Incorporate well-decomposed manure or compost (5-10 tons/hectare) during land preparation.

5. Transplanting:
Transplant when seedlings are 3-4 weeks old (15-20cm tall) with 4-6 true leaves. Space plants 40-60cm apart on ridges. Transplant in the evening or on cloudy days to reduce transplant shock. Water immediately after transplanting.

6. Water Management:
Maintain consistent soil moisture:
- Irrigate regularly, especially during flowering and fruit development
- Avoid overhead irrigation (promotes leaf diseases)
- Use drip irrigation where possible
- Mulch with grass, straw, or plastic to conserve moisture and suppress weeds

7. Nutrient Management:
Apply fertilizer based on soil test recommendations:
- Basal application: 200-300kg/ha NPK (23:21:0+4S) before transplanting
- Top-dressing: 150-200kg/ha CAN in 2-3 split applications
For organic production, apply 20-30 tons/ha of well-decomposed manure or compost.

8. Pruning and Staking:
For indeterminate varieties:
- Prune to 1-2 main stems
- Remove suckers (side shoots) weekly
- Stake plants using wooden stakes or trellis system
- Tie plants loosely to stakes as they grow

9. Pest and Disease Management:
Practice integrated pest management:
- Crop rotation (3-year cycle away from solanaceous crops)
- Use disease-resistant varieties
- Remove and destroy infected plants
- Monitor for early blight, late blight, bacterial wilt, and virus diseases
- Scout for insect pests (whiteflies, aphids, tomato fruitworm)
- Apply appropriate fungicides preventatively during humid conditions
- Use biopesticides and organic controls where possible

10. Harvesting and Post-harvest:
Harvest at proper maturity stage:
- For local markets: Light red to red stage
- For distant markets: Mature green to breaker stage
Handle fruits carefully to avoid bruising. Grade and sort based on size and quality. Use clean crates for transportation. For longer shelf life, store at 10-15°C with good ventilation.

11. Marketing:
Research markets before planting. Consider direct selling to urban markets, hotels, and restaurants for better prices. Time production for periods of high demand and low supply (off-season production). Join farmer groups for better market access and negotiation power.""",
            'category': 'tomato',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'vegetables',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} vegetable farming tips")


def add_mixed_farming_tips():
    """Add tips for mixed farming in Malawi"""
    tips = [
        {
            'title': 'Integrated Crop-Livestock Farming in Malawi',
            'content': """Integrated crop-livestock farming combines crop cultivation with animal husbandry, creating a synergistic system that improves productivity, sustainability, and resilience. This approach is especially valuable for smallholder farmers in Malawi. Here are key practices for successful integrated farming:

1. System Design:
Plan your farm layout to facilitate integration:
- Allocate space for crops, livestock, and feed production
- Consider animal housing location for easy manure collection
- Design water harvesting systems to serve both crops and livestock
- Include rotational grazing areas where applicable
- Create compost production areas

2. Crop-Livestock Selection:
Choose complementary enterprises:
- Crops: Maize, legumes (groundnuts, soybeans, pigeon peas), vegetables, fodder crops
- Livestock: Dairy cattle, beef cattle, goats, sheep, chickens, pigs
Select crops and livestock adapted to your specific agroecological zone in Malawi.

3. Crop Residue Management:
Maximize the value of crop residues:
- Use maize stover, bean haulms, and groundnut tops as livestock feed
- Process crop residues (chopping, mixing with molasses) to improve palatability
- Return unpalatable residues to fields as mulch
- Use residues as bedding material in animal housing, later converting to manure

4. Manure Management:
Utilize livestock manure effectively:
- Collect manure daily from animal housing
- Compost manure with crop residues to reduce pathogens and weed seeds
- Apply composted manure to crops (5-10 tons/hectare)
- Consider biogas production from manure for cooking and lighting
- Apply manure strategically to high-value crops first

5. Fodder Production:
Integrate fodder production into the farming system:
- Establish leguminous fodder trees (Leucaena, Sesbania, Gliricidia) along boundaries and contours
- Grow improved forage grasses (Napier grass, Rhodes grass) on portions of cropland
- Plant dual-purpose legumes that provide both human food and animal feed
- Practice relay-cropping of fodder in food crop fields during late season

6. Rotational Grazing and Cropping:
Implement rotation systems:
- Rotate livestock through different grazing areas to prevent overgrazing
- Practice crop rotation including legumes to improve soil fertility
- Allow livestock to graze crop fields after harvest to feed on residues and add manure directly
- Consider paddock systems for controlled grazing

7. Soil and Water Conservation:
Implement conservation practices:
- Construct contour bunds to prevent erosion
- Plant vetiver grass or fodder trees on contours
- Practice minimum tillage to preserve soil structure
- Use mulching to conserve soil moisture
- Harvest rainwater from roofs and runoff for livestock and crop irrigation

8. Pest and Disease Management:
Use integrated approaches:
- Rotate crops to break pest cycles
- Use livestock to control weeds in fallow areas
- Practice proper sanitation in animal housing to reduce disease pressure
- Maintain appropriate distances between similar enterprises to reduce disease spread
- Use botanical pesticides where appropriate

9. Diversification for Risk Management:
Diversify within crops and livestock:
- Grow several crop varieties with different maturity periods
- Raise different types of livestock with varied market cycles
- Include perennial crops (fruits, fodder trees) for long-term stability
- Incorporate small livestock (poultry, rabbits) for quick returns and daily income

10. Market Orientation:
Align production with market opportunities:
- Research local demand for both crop and livestock products
- Coordinate production timing for optimal market prices
- Consider value addition (milk processing, grain storage for later sales)
- Join farmer groups for better market access and information

11. Record Keeping:
Maintain comprehensive records:
- Track inputs and outputs for each enterprise
- Monitor interactions between crop and livestock components
- Record yields, growth rates, and production cycles
- Document expenses and income
- Use records to improve future planning

12. Climate-Smart Practices:
Implement practices that build resilience:
- Plant drought-tolerant crops and keep hardy livestock breeds
- Establish agroforestry systems that provide shade, fodder, and windbreaks
- Practice water harvesting and conservation
- Maintain flexible stocking rates based on seasonal conditions"""
            ,
            'category': 'integrated farming',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'mixed',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} mixed farming tips")


def add_dairy_farming_tips():
    """Add tips for dairy farming in Malawi"""
    tips = [
        {
            'title': 'Commercial Dairy Farming Best Practices in Malawi',
            'content': """Commercial dairy farming can be highly profitable in Malawi, where demand for milk and dairy products exceeds supply. Here are comprehensive best practices for establishing and operating a successful commercial dairy farm:

1. Breed Selection for Commercial Production:
Choose appropriate dairy breeds based on your resources and management capacity:
- Pure exotic breeds (Holstein-Friesian, Jersey, Ayrshire): Highest production but require intensive management
- Crossbreeds (50-75% exotic blood): Good compromise between production and adaptability
- Multiple breeds: Consider keeping both high-producing Friesians and butterfat-rich Jerseys

2. Infrastructure Development:
Establish proper infrastructure:
- Milking parlor with concrete floor, good drainage, and washing facilities
- Feed storage facilities protected from moisture and pests
- Calf pens with proper ventilation and protection
- Isolation facilities for sick animals
- Clean water supply system with storage capacity
- Manure management system (collection pit, composting area)
- Cooling system for milk (refrigerator or milk cooling tank)

3. Advanced Feeding Systems:
Implement strategic feeding programs:
- Formulate total mixed rations (TMR) balanced for different production stages
- Establish year-round fodder production systems (irrigated Napier, Rhodes grass)
- Produce and properly store silage for dry season feeding
- Provide phase feeding based on lactation stage:
  * Early lactation (1-100 days): Higher protein (16-18%) and energy
  * Mid-lactation (100-200 days): Moderate protein (15-16%)
  * Late lactation (200-305 days): Lower protein (13-14%)
  * Dry period: Specific dry cow ration to prevent metabolic disorders

4. Reproduction Management:
Implement efficient breeding programs:
- Use artificial insemination with semen from proven bulls
- Maintain detailed heat detection records (3 times daily observations)
- Follow the "AM-PM rule" (inseminate in evening if heat observed in morning, and vice versa)
- Perform pregnancy diagnosis 60-90 days after insemination
- Maintain calving interval of 12-14 months
- Implement synchronization protocols for timed AI in larger herds

5. Calf Rearing for Replacement Stock:
Raise healthy replacement heifers:
- Feed colostrum (10% of body weight) within first 6 hours
- Follow specific feeding schedules:
  * Week 1-4: 4-6 liters of milk daily split into 2-3 feedings
  * Week 5-8: Gradually reduce milk while increasing calf starter
  * Week 9-12: Complete weaning, provide quality roughage and starter
- Target growth rates of 0.7-0.8 kg/day for heifers
- Breed heifers at 15-18 months when they reach 60% of mature weight

6. Milk Harvesting and Quality Control:
Maintain high milk quality standards:
- Implement proper pre-milking routines (clean udder, strip first milk, apply pre-dip)
- Milk with clean, well-maintained equipment
- Practice post-milking teat dipping with iodine solution
- Cool milk quickly to 4°C within 2 hours of milking
- Clean and sanitize all equipment after each use
- Test milk regularly for somatic cell count and bacterial content
- Implement HACCP principles for food safety

7. Health Management Program:
Establish comprehensive health protocols:
- Develop vaccination schedules with local veterinarian
- Implement strategic parasite control program
- Conduct regular screening for mastitis using California Mastitis Test
- Monitor body condition score throughout lactation cycle
- Implement foot care program including regular hoof trimming
- Maintain detailed health records for each animal
- Establish relationships with veterinary service providers

8. Waste Management and Environmental Considerations:
Implement sustainable waste handling:
- Construct proper waste storage facilities
- Compost manure for field application
- Consider biogas digester installation
- Implement nutrient management plan for crop fields
- Control runoff from animal housing areas
- Plant trees around farm perimeter as windbreaks and for shade

9. Record Keeping and Financial Management:
Maintain comprehensive records:
- Individual cow production records
- Feed consumption and costs
- Health treatments and outcomes
- Breeding data and calving records
- Income and expense tracking
- Milk quality parameters
- Use data for culling decisions and genetic improvement

10. Value Addition and Marketing:
Explore market opportunities:
- Direct marketing of fresh milk to consumers
- Processing into yogurt, cheese, cultured milk
- Establish contracts with processors and institutions
- Develop branded products for premium markets
- Join dairy cooperatives for collective marketing power

11. Human Resource Management:
Develop your farm team:
- Train staff in proper animal handling and welfare
- Provide clear standard operating procedures
- Implement incentive systems based on milk quality and production
- Conduct regular staff meetings and feedback sessions
- Invest in continuous education and skills development

12. Technology Adoption:
Consider appropriate technologies:
- Milking machines for herds larger than 10 cows
- Milk cooling systems
- Automated feeding systems for concentrate delivery
- Digital record keeping systems
- Heat detection aids (tail paint, pedometers)
- Solar water heaters for wash water"""
            ,
            'category': 'dairy cattle',
            'season': 'all',
            'region': 'Malawi',
            'farm_type': 'dairy',
            'image_url': None
        }
    ]
    
    for tip in tips:
        existing = FarmingTip.query.filter_by(title=tip['title']).first()
        if not existing:
            new_tip = FarmingTip(
                title=tip['title'],
                content=tip['content'],
                category=tip['category'],
                season=tip['season'],
                region=tip['region'],
                farm_type=tip['farm_type'],
                image_url=tip['image_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_tip)
    
    db.session.commit()
    print(f"Added {len(tips)} dairy farming tips")


def add_media_resources():
    """Add media resources related to farming in Malawi"""
    resources = [
        {
            'title': 'Efficient Irrigation Techniques for Malawian Smallholder Farmers',
            'description': 'This video demonstrates various low-cost irrigation methods suitable for small-scale farming in Malawi, including drip irrigation, treadle pumps, and rainwater harvesting.',
            'resource_type': 'video',
            'url': 'https://www.youtube.com/watch?v=SsIQm_XUszU',
            'source': 'FAO',
            'author': 'Food and Agriculture Organization',
            'farm_type': 'crops',
            'thumbnail_url': None
        },
        {
            'title': 'Sustainable Pest Management in Maize Production',
            'description': 'This comprehensive guide covers integrated pest management strategies for maize farmers in Malawi, focusing on fall armyworm control using both traditional and modern techniques.',
            'resource_type': 'article',
            'url': 'https://www.cimmyt.org/news/new-publications-guide-farmers-to-prevent-fall-armyworm-infestation-in-maize-fields/',
            'source': 'CIMMYT',
            'author': 'International Maize and Wheat Improvement Center',
            'farm_type': 'crops',
            'thumbnail_url': None
        },
        {
            'title': 'Improving Dairy Production Through Better Feed Management',
            'description': 'This podcast episode discusses practical approaches to improving dairy cattle nutrition using locally available feed resources in Malawi.',
            'resource_type': 'podcast',
            'url': 'https://www.fao.org/dairy-production-products/resources/podcast/en/',
            'source': 'FAO Dairy Production and Products',
            'author': 'Food and Agriculture Organization',
            'farm_type': 'dairy',
            'thumbnail_url': None
        },
        {
            'title': 'Fish Farming as a Business in Malawi',
            'description': 'This video provides a step-by-step guide to establishing a profitable fish farming enterprise in Malawi, covering pond construction, species selection, and marketing strategies.',
            'resource_type': 'video',
            'url': 'https://www.youtube.com/watch?v=VPSOy5JgH9k',
            'source': 'WorldFish',
            'author': 'WorldFish Center',
            'farm_type': 'fish',
            'thumbnail_url': None
        },
        {
            'title': 'Effective Broiler Management for Smallholders',
            'description': 'This comprehensive guide covers all aspects of small-scale broiler production, from day-old chick management to marketing finished birds.',
            'resource_type': 'article',
            'url': 'https://www.acdivoca.org/resources/poultry-production-manual/',
            'source': 'ACDI/VOCA',
            'author': 'Agricultural Cooperative Development International',
            'farm_type': 'poultry',
            'thumbnail_url': None
        },
        {
            'title': 'Sustainable Vegetable Production Techniques',
            'description': 'This video demonstrates organic pest management and soil fertility improvement techniques for vegetable farmers in Malawi.',
            'resource_type': 'video',
            'url': 'https://www.youtube.com/watch?v=l-M6oZPm3_c',
            'source': 'Total Land Care Malawi',
            'author': 'Total Land Care',
            'farm_type': 'vegetables',
            'thumbnail_url': None
        },
        {
            'title': 'Climate-Smart Agriculture Practices for Malawi',
            'description': 'This comprehensive guide covers practical climate-smart agriculture techniques specifically adapted for Malawian farming systems.',
            'resource_type': 'article',
            'url': 'https://www.cimmyt.org/projects/climate-smart-villages-in-malawi/',
            'source': 'CIMMYT',
            'author': 'International Maize and Wheat Improvement Center',
            'farm_type': 'mixed',
            'thumbnail_url': None
        },
        {
            'title': 'Fruit Tree Propagation and Management',
            'description': 'This podcast series covers grafting, pruning, and management of various fruit trees suitable for cultivation in Malawi.',
            'resource_type': 'podcast',
            'url': 'https://www.icraf.org/resources/',
            'source': 'World Agroforestry Centre',
            'author': 'ICRAF',
            'farm_type': 'fruits',
            'thumbnail_url': None
        }
    ]
    
    for resource in resources:
        existing = MediaResource.query.filter_by(title=resource['title']).first()
        if not existing:
            new_resource = MediaResource(
                title=resource['title'],
                description=resource['description'],
                resource_type=resource['resource_type'],
                url=resource['url'],
                source=resource['source'],
                author=resource['author'],
                farm_type=resource['farm_type'],
                thumbnail_url=resource['thumbnail_url'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_resource)
    
    db.session.commit()
    print(f"Added {len(resources)} media resources")


def add_crop_calendar():
    """Add crop calendar data for Malawi"""
    calendar_entries = [
        {
            'crop_name': 'Maize',
            'region': 'Malawi Central',
            'planting_start': 'November',
            'planting_end': 'December',
            'harvesting_start': 'March',
            'harvesting_end': 'May',
            'growing_period': 120,
            'water_requirements': 'Moderate - requires 500-800mm of water during growing season',
            'soil_requirements': 'Well-drained sandy loams to clay loams with pH 5.5-7.0',
            'notes': 'Main staple crop in Malawi. Early planting with first effective rains is recommended.'
        },
        {
            'crop_name': 'Rice',
            'region': 'Malawi Southern',
            'planting_start': 'December',
            'planting_end': 'January',
            'harvesting_start': 'April',
            'harvesting_end': 'May',
            'growing_period': 120,
            'water_requirements': 'High - requires standing water during most of growth period',
            'soil_requirements': 'Clay soils that can hold water, pH 5.5-7.0',
            'notes': 'Grown in dambo areas and irrigated schemes. Water management is critical.'
        },
        {
            'crop_name': 'Groundnuts',
            'region': 'Malawi',
            'planting_start': 'November',
            'planting_end': 'December',
            'harvesting_start': 'March',
            'harvesting_end': 'April',
            'growing_period': 130,
            'water_requirements': 'Moderate - requires 500-700mm of water during growing season',
            'soil_requirements': 'Well-drained sandy loams with pH 5.3-6.5. Calcium availability important.',
            'notes': 'Important legume for soil improvement and nutrition. Shell just before planting.'
        },
        {
            'crop_name': 'Soybeans',
            'region': 'Malawi',
            'planting_start': 'December',
            'planting_end': 'January',
            'harvesting_start': 'April',
            'harvesting_end': 'May',
            'growing_period': 110,
            'water_requirements': 'Moderate - requires 450-700mm of water during growing season',
            'soil_requirements': 'Well-drained loamy soils with pH 6.0-7.0',
            'notes': 'Important protein source and cash crop. Inoculation with rhizobium improves yields.'
        },
        {
            'crop_name': 'Cassava',
            'region': 'Malawi',
            'planting_start': 'October',
            'planting_end': 'December',
            'harvesting_start': 'September',
            'harvesting_end': 'August',
            'growing_period': 365,
            'water_requirements': 'Low to moderate - drought tolerant once established',
            'soil_requirements': 'Wide range of soils but prefers well-drained sandy loams',
            'notes': 'Can remain in ground for 2+ years. Important food security crop due to drought tolerance.'
        },
        {
            'crop_name': 'Sweet Potato',
            'region': 'Malawi',
            'planting_start': 'December',
            'planting_end': 'January',
            'harvesting_start': 'April',
            'harvesting_end': 'June',
            'growing_period': 120,
            'water_requirements': 'Moderate - drought tolerant once established',
            'soil_requirements': 'Sandy loams with good drainage, pH 5.6-6.6',
            'notes': 'Important food security crop. Orange-fleshed varieties provide vitamin A.'
        },
        {
            'crop_name': 'Beans',
            'region': 'Malawi',
            'planting_start': 'March',
            'planting_end': 'April',
            'harvesting_start': 'June',
            'harvesting_end': 'July',
            'growing_period': 90,
            'water_requirements': 'Moderate - sensitive to both drought and waterlogging',
            'soil_requirements': 'Well-drained loams with pH 5.8-6.5',
            'notes': 'Often grown as a second crop (relay crop) or in dimba (wetland) areas.'
        },
        {
            'crop_name': 'Pigeon Pea',
            'region': 'Malawi Southern',
            'planting_start': 'November',
            'planting_end': 'December',
            'harvesting_start': 'July',
            'harvesting_end': 'August',
            'growing_period': 240,
            'water_requirements': 'Low - highly drought tolerant once established',
            'soil_requirements': 'Adaptable to wide range of soils including poor soils',
            'notes': 'Often intercropped with maize. Long duration varieties provide food during lean seasons.'
        },
        {
            'crop_name': 'Tomato',
            'region': 'Malawi',
            'planting_start': 'April',
            'planting_end': 'June',
            'harvesting_start': 'July',
            'harvesting_end': 'September',
            'growing_period': 90,
            'water_requirements': 'High - requires regular watering',
            'soil_requirements': 'Well-drained loamy soils with pH 6.0-6.8',
            'notes': 'Primarily grown in dimba areas during dry season. Staking and pruning improves yields.'
        },
        {
            'crop_name': 'Banana',
            'region': 'Malawi',
            'planting_start': 'Year-round',
            'planting_end': 'Year-round',
            'harvesting_start': 'Year-round',
            'harvesting_end': 'Year-round',
            'growing_period': 365,
            'water_requirements': 'High - requires consistent moisture',
            'soil_requirements': 'Deep, well-drained loamy soils with high organic matter',
            'notes': 'Perennial crop. Planting at start of rainy season recommended for rainfed systems.'
        }
    ]
    
    for entry in calendar_entries:
        existing = CropCalendar.query.filter_by(crop_name=entry['crop_name'], region=entry['region']).first()
        if not existing:
            new_entry = CropCalendar(
                crop_name=entry['crop_name'],
                region=entry['region'],
                planting_start=entry['planting_start'],
                planting_end=entry['planting_end'],
                harvesting_start=entry['harvesting_start'],
                harvesting_end=entry['harvesting_end'],
                growing_period=entry['growing_period'],
                water_requirements=entry['water_requirements'],
                soil_requirements=entry['soil_requirements'],
                notes=entry['notes']
            )
            db.session.add(new_entry)
    
    db.session.commit()
    print(f"Added {len(calendar_entries)} crop calendar entries")


def link_tips_to_resources():
    """Link farming tips to relevant media resources"""
    
    # Link maize tips to relevant resources
    maize_tips = FarmingTip.query.filter_by(category='maize').all()
    pest_resource = MediaResource.query.filter_by(title='Sustainable Pest Management in Maize Production').first()
    climate_resource = MediaResource.query.filter_by(title='Climate-Smart Agriculture Practices for Malawi').first()
    irrigation_resource = MediaResource.query.filter_by(title='Efficient Irrigation Techniques for Malawian Smallholder Farmers').first()
    
    if maize_tips and pest_resource and climate_resource:
        for tip in maize_tips:
            if pest_resource not in tip.related_resources:
                tip.related_resources.append(pest_resource)
            if climate_resource not in tip.related_resources:
                tip.related_resources.append(climate_resource)
            if irrigation_resource not in tip.related_resources:
                tip.related_resources.append(irrigation_resource)
    
    # Link dairy tips to relevant resources
    dairy_tips = FarmingTip.query.filter_by(farm_type='dairy').all()
    dairy_resource = MediaResource.query.filter_by(title='Improving Dairy Production Through Better Feed Management').first()
    if dairy_tips and dairy_resource:
        for tip in dairy_tips:
            if dairy_resource not in tip.related_resources:
                tip.related_resources.append(dairy_resource)
    
    # Link fish farming tips to relevant resources
    fish_tips = FarmingTip.query.filter_by(farm_type='fish').all()
    fish_resource = MediaResource.query.filter_by(title='Fish Farming as a Business in Malawi').first()
    if fish_tips and fish_resource:
        for tip in fish_tips:
            if fish_resource not in tip.related_resources:
                tip.related_resources.append(fish_resource)
    
    # Link poultry tips to relevant resources
    poultry_tips = FarmingTip.query.filter_by(farm_type='poultry').all()
    poultry_resource = MediaResource.query.filter_by(title='Effective Broiler Management for Smallholders').first()
    if poultry_tips and poultry_resource:
        for tip in poultry_tips:
            if poultry_resource not in tip.related_resources:
                tip.related_resources.append(poultry_resource)
    
    # Link vegetable tips to relevant resources
    vegetable_tips = FarmingTip.query.filter_by(farm_type='vegetables').all()
    vegetable_resource = MediaResource.query.filter_by(title='Sustainable Vegetable Production Techniques').first()
    if vegetable_tips and vegetable_resource:
        for tip in vegetable_tips:
            if vegetable_resource not in tip.related_resources:
                tip.related_resources.append(vegetable_resource)
    
    # Link fruit tips to relevant resources
    fruit_tips = FarmingTip.query.filter_by(farm_type='fruits').all()
    fruit_resource = MediaResource.query.filter_by(title='Fruit Tree Propagation and Management').first()
    if fruit_tips and fruit_resource:
        for tip in fruit_tips:
            if fruit_resource not in tip.related_resources:
                tip.related_resources.append(fruit_resource)
    
    # Link mixed farming tips to relevant resources
    mixed_tips = FarmingTip.query.filter_by(farm_type='mixed').all()
    mixed_resource = MediaResource.query.filter_by(title='Climate-Smart Agriculture Practices for Malawi').first()
    if mixed_tips and mixed_resource:
        for tip in mixed_tips:
            if mixed_resource not in tip.related_resources:
                tip.related_resources.append(mixed_resource)
    
    db.session.commit()
    print("Linked farming tips to relevant media resources")


def main():
    """Run all data addition functions"""
    with app.app_context():
        add_crop_farming_tips()
        add_livestock_farming_tips()
        add_poultry_farming_tips()
        add_fish_farming_tips()
        add_fruit_farming_tips()
        add_vegetable_farming_tips()
        add_mixed_farming_tips()
        add_dairy_farming_tips()
        add_media_resources()
        add_crop_calendar()
        link_tips_to_resources()
        
        print("All farm-specific tips and resources added successfully")


if __name__ == "__main__":
    main()