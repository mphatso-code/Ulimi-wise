"""
Script to add farming tips for crops commonly grown in Malawi
"""
import sys
from datetime import datetime
from app import app, db
from models import FarmingTip

def add_tips():
    """Add farming tips for various crops grown in Malawi"""
    # List of tips to add
    tips = [
        # Maize (Chimanga) - Malawi's staple crop
        {
            "title": "Growing Maize in Malawi",
            "content": """
Maize (Chimanga) is Malawi's most important staple crop. Follow these guidelines for successful cultivation:

1. Land Preparation:
- Clear your land of weeds and crop residues
- Plough to a depth of 20-30cm
- Add compost or well-decomposed manure (3-5 tons per hectare)

2. Planting Time:
- In most areas of Malawi, plant with the first good rains (November-December)
- In areas with irrigation, you can plant throughout the year

3. Seed Selection and Spacing:
- Choose drought-resistant varieties such as SC403, SC627, or DKC9089
- Plant in rows 75cm apart with 25cm between plants (1 seed per hole)
- Planting depth should be 5cm

4. Fertilizer Application:
- Apply 23:21:0+4S or 23:10:5+6S+1.0Zn at planting (2 bottle caps per planting station)
- Top-dress with Urea 3-4 weeks after germination (1 bottle cap per plant)

5. Weed Management:
- First weeding: 1-2 weeks after emergence
- Second weeding: 4-5 weeks after emergence
- Consider using Atrazine as a pre-emergence herbicide

6. Pest Management:
- Monitor for Fall Armyworm, a serious maize pest in Malawi
- Early detection is crucial - check for leaf damage and frass
- Use biological controls like neem extracts or commercial pesticides as recommended

7. Harvesting:
- Harvest when stalks turn brown and cobs droop downward
- Maize should be dried to 12-13% moisture for proper storage

For subsistence farmers, consider intercropping maize with legumes like beans or groundnuts to improve soil fertility and maximize land use.
            """,
            "category": "maize",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Rice
        {
            "title": "Rice Farming in Malawi",
            "content": """
Rice is becoming an increasingly important crop in Malawi, particularly in areas with good water access. Here are key tips for rice farming:

1. Land Selection and Preparation:
- Choose flat land with good water retention capability
- Create water retention bunds around fields
- Level the field carefully to ensure even water distribution
- Clear land of all weeds and previous crop residues

2. Rice Varieties:
- For irrigated systems: Kilombero, Faya, TCG-10
- For rainfed systems: Pusa 33, NERICA varieties

3. Planting Methods:
- Transplanting method: Prepare seedlings in a nursery for 21-30 days, then transplant at 20cm x 20cm spacing
- Direct seeding: Sow pre-soaked seeds directly at 20cm x 20cm, using 2-3 seeds per hole

4. Water Management:
- Maintain 5-7cm of standing water during vegetative stage
- Drain field 10-15 days before harvesting

5. Fertilizer Application:
- Apply NPK 23:21:0 at planting (200kg/ha)
- Apply Urea at tillering and flowering stages (100kg/ha each time)

6. Weed Management:
- First weeding: 20-25 days after planting
- Second weeding: 40-45 days after planting

7. Pest and Disease Management:
- Watch for Rice Blast, especially in humid conditions
- Monitor for Stem Borers and apply appropriate pesticides if needed
- Check for birds during grain filling stage

8. Harvesting:
- Harvest when 80-85% of grains have turned golden yellow
- Cut stems at ground level
- Dry to 14% moisture content before storage

Rice farming can be profitable in suitable areas of Malawi, especially with good access to markets. For small-scale farmers, consider joining or forming rice farming cooperatives to improve access to inputs and markets.
            """,
            "category": "rice",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Beans
        {
            "title": "Bean Cultivation in Malawi",
            "content": """
Beans (Nyemba) are an important protein source and cash crop in Malawi. Follow these guidelines for successful bean farming:

1. Land Preparation:
- Prepare well-drained soil with good tilth
- Avoid waterlogged areas as beans are susceptible to root rot
- Apply organic matter to improve soil structure

2. Bean Varieties in Malawi:
- Bush beans: Kalima, Napilira, Sugar bean
- Climbing beans: MAC 44, Kholophethe

3. Planting Time:
- First planting: November-December (with first rains)
- Second planting: February-March (residual moisture)
- In areas with irrigation, beans can be grown year-round

4. Seed Rate and Spacing:
- Bush beans: Plant in rows 45cm apart with 10cm between plants
- Climbing beans: Rows 75cm apart with 15cm between plants
- Planting depth: 3-5cm

5. Fertilizer Requirements:
- Apply well-decomposed manure before planting
- Apply 23:21:0+4S fertilizer at planting (100kg/ha)
- Avoid excessive nitrogen which causes vegetative growth at expense of pod development

6. Weed Management:
- First weeding: 2 weeks after emergence
- Second weeding: 4-5 weeks after emergence
- Keep fields weed-free especially during flowering

7. Pest and Disease Management:
- Common pests: Bean fly, aphids, pod borers
- Common diseases: Angular leaf spot, bean rust, anthracnose
- Practice crop rotation to reduce disease pressure
- Use certified disease-free seeds

8. Harvesting:
- For green beans: Harvest when pods are still green but seeds are fully formed
- For dry beans: Harvest when pods turn yellow and begin to dry
- Dry seeds properly to 12-14% moisture content for storage

Beans fix nitrogen in the soil and are excellent in crop rotation or intercropping systems with maize. They can be grown successfully by small-scale farmers with minimal inputs.
            """,
            "category": "beans",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Sorghum
        {
            "title": "Sorghum Cultivation in Malawi",
            "content": """
Sorghum (Mapira) is an important drought-resistant crop in Malawi, especially valuable in dry regions. Here's how to grow it successfully:

1. Land Preparation:
- Clear land of weeds and previous crop residues
- Plough to a depth of 15-20cm
- Create ridges spaced 75-90cm apart in dry areas

2. Varieties Suitable for Malawi:
- Pilira 1 and Pilira 2: Early maturing varieties
- Isidomba: Drought resistant
- Kuyuma and Sima: Good for food
- Thengalamanga: Bird-resistant variety

3. Planting Time:
- Plant at the onset of rains (November-December)
- In areas prone to Quelea birds, delay planting until January

4. Seed Rate and Spacing:
- Plant in rows 75cm apart with 15-20cm between plants
- Seed rate: 8-10kg per hectare
- Planting depth: 3-5cm

5. Fertilizer Application:
- Apply 23:21:0+4S at planting (100kg/ha)
- Top-dress with Urea 3-4 weeks after emergence (50kg/ha)

6. Weed Management:
- Sorghum grows slowly initially, so early weed control is crucial
- First weeding: 2 weeks after emergence
- Second weeding: 4-5 weeks after emergence

7. Pest Management:
- Main pests: Stalk borers, shoot fly, and Quelea birds
- For birds: Use bird-resistant varieties or use bird scaring methods
- For insects: Apply appropriate insecticides if infestation is severe

8. Disease Management:
- Watch for covered smut and downy mildew
- Use resistant varieties and practice crop rotation
- Treat seeds with fungicides before planting

9. Harvesting:
- Harvest when grains are hard and no longer milky
- Cut the heads and dry thoroughly
- Thresh and clean before storage

Sorghum is excellent for regions with erratic rainfall as it can withstand dry spells better than maize. It's also suitable for farmers with limited resources as it requires fewer inputs than many other crops.
            """,
            "category": "sorghum",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Cassava
        {
            "title": "Cassava Farming in Malawi",
            "content": """
Cassava (Chinangwa) is an important food security crop in Malawi due to its drought tolerance. Here are key tips for growing cassava:

1. Land Preparation:
- Clear land completely of weeds and crop residues
- Plough to a depth of 20-30cm to facilitate root development
- Prepare mounds or ridges, especially in areas with heavy rain

2. Cassava Varieties for Malawi:
- Early maturing (12 months): Mbundumali, Sauti
- Disease resistant: Mkondezi, Mulola, Silira
- High yielding: Maunjili, Phoso

3. Planting Material:
- Use mature, pest-free stem cuttings (25-30cm long) from 8-12 month old plants
- Each cutting should have 5-7 nodes
- Allow cuttings to dry in shade for 2-3 days before planting

4. Planting Method:
- Plant at the start of the rainy season (November-December)
- Space plants 1m between rows and 1m within rows
- Plant cuttings either horizontally (5-10cm deep) or at an angle with 2/3 of cutting below ground

5. Fertilizer Requirements:
- Cassava can grow in poor soils but responds well to fertilizers
- Apply NPK (23:21:0) at 100kg/ha if soil fertility is low
- Organic manure can be incorporated during land preparation

6. Weed Management:
- Keep fields weed-free for the first 3-4 months
- First weeding: 3-4 weeks after planting
- Second weeding: 8-10 weeks after planting

7. Pest and Disease Management:
- Watch for cassava mosaic disease and cassava brown streak disease
- Use disease-free planting materials and resistant varieties
- Monitor for mealybugs and green mites
- Practice crop rotation with non-root crops

8. Harvesting:
- Early varieties can be harvested after 9-12 months
- Late varieties after 18-24 months
- Piecemeal harvesting can be done by carefully removing some roots while leaving the plant to continue growing

Cassava is an excellent food security crop for small-scale farmers. It can be processed into flour (kondowole) for longer storage or consumed fresh. Cassava leaves are also nutritious as vegetables.
            """,
            "category": "cassava",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Groundnuts
        {
            "title": "Groundnut Farming in Malawi",
            "content": """
Groundnuts (Mtedza) are an important legume crop in Malawi for both food and income. Here's a guide to successful groundnut farming:

1. Land Selection and Preparation:
- Choose well-drained, sandy or sandy-loam soils
- Avoid clay soils which restrict pod development
- Plough to a depth of 15-20cm
- Prepare a fine seedbed with good tilth

2. Recommended Varieties:
- CG7: High yielding, medium maturity (130-150 days)
- Nsinjiro: Drought tolerant, early maturing (110-120 days)
- Kakoma: High oil content, good for processing
- Chitala: Rosette resistant variety

3. Planting Time:
- Plant with the onset of good rains (mid-November to December)
- Avoid late planting as it reduces yields

4. Seed Rate and Spacing:
- Use 80-100kg of unshelled seed per hectare
- Row spacing: 75cm between ridges
- Plant spacing: 15cm between stations with 1 seed per station
- Planting depth: 5cm

5. Fertilizer Application:
- Groundnuts fix nitrogen but need phosphorus
- Apply 23:21:0+4S at planting (100kg/ha)
- Apply gypsum (calcium sulfate) at flowering for better pod filling

6. Weed Management:
- Weed thoroughly during the first 45 days
- Avoid deep cultivation during flowering and podding
- Hand pull weeds near plants to avoid damaging pods

7. Pest and Disease Management:
- Major pests: Aphids, thrips, and termites
- Major diseases: Rosette virus, early and late leaf spots
- Use certified disease-free seeds
- Practice crop rotation (avoid planting after groundnuts, tobacco or soybeans)

8. Harvesting:
- Harvest when:
  * Plants have yellowish leaves
  * Inside pod shell has dark markings
  * Sample kernels have correct color for the variety
- Dig up plants carefully, shake off soil, and dry with pods attached to plants

9. Post-Harvest Handling:
- Dry to 8-10% moisture content
- Shell only when ready to sell or plant
- Store in clean, well-ventilated conditions

Groundnuts are excellent for intercropping with maize and contribute to soil fertility through nitrogen fixation. They are particularly important for smallholder farmers as they serve both as a food crop and cash crop.
            """,
            "category": "groundnuts",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Sweet Potatoes
        {
            "title": "Sweet Potato Farming in Malawi",
            "content": """
Sweet potatoes (Mbatata) are an important food security crop in Malawi. Here's how to grow them successfully:

1. Land Preparation:
- Sweet potatoes prefer well-drained, sandy loam soils
- Avoid waterlogged areas which cause root rot
- Make ridges or mounds 30-40cm high, spaced 75-100cm apart

2. Recommended Varieties in Malawi:
- Kenya: High yielding orange-fleshed variety (high vitamin A)
- Zondeni: Popular orange-fleshed variety
- Semusa: High yielding white-fleshed variety
- Sakananthaka: Drought tolerant variety
- Tainoni: Good for both leaves and tubers

3. Planting Material:
- Use fresh, healthy vines (30cm long) with 3-4 nodes
- Get vines from disease-free fields
- You can produce your own vines by planting "seed" sweet potatoes

4. Planting Time:
- Best planted at the end of rainy season (February-March) using residual moisture
- Can also be planted in October-November with irrigation
- In areas with continuous rainfall, can be planted year-round

5. Planting Method:
- Plant vines at a 45° angle with 2/3 of the vine buried
- Space plants 30cm apart on ridges
- Ensure at least 2 nodes are below ground

6. Fertilizer Requirements:
- Sweet potatoes do not require much fertilizer
- Apply 23:21:0 at planting (100kg/ha) especially in poor soils
- Avoid excessive nitrogen which promotes vine growth over tuber development

7. Field Management:
- Keep fields weed-free, especially during the first 8 weeks
- Earth up around the base of plants to encourage more tuber formation
- Avoid disturbing the soil once tubers begin forming

8. Pest and Disease Management:
- Major pests: Sweet potato weevil, striped sweet potato beetle
- Major diseases: Sweet potato virus disease, sweet potato feathery mottle virus
- Use clean planting material and practice crop rotation

9. Harvesting:
- Mature in 3-5 months depending on variety
- Harvest when leaves begin to yellow
- Harvest carefully to avoid damaging tubers
- For piecemeal harvesting, carefully remove soil and harvest larger roots, then replace soil

Sweet potatoes are an excellent crop for food security as they are drought tolerant and can be harvested over an extended period. The orange-fleshed varieties are particularly nutritious due to their high vitamin A content. Both leaves and tubers can be consumed.
            """,
            "category": "sweet potatoes",
            "season": "dry",
            "region": "Malawi"
        },
        
        # Millet
        {
            "title": "Finger Millet Cultivation in Malawi",
            "content": """
Finger Millet (Mawere) is a nutritious traditional grain that performs well in dry conditions. Here's a guide to growing finger millet in Malawi:

1. Land Preparation:
- Prepare a fine, firm seedbed
- Clear land completely of weeds
- Level the field well as finger millet seeds are small

2. Varieties Suitable for Malawi:
- Local landraces are well adapted
- Improved varieties: P224, Gulu-E, U-15

3. Planting Time and Method:
- Plant at the onset of rains (November-December)
- Sowing methods:
  * Broadcasting: Mix seed with dry sand (1:10 ratio) for even distribution
  * Row planting: Rows 20-30cm apart, very shallow planting (0.5-1cm deep)
- Seed rate: 5-8kg per hectare

4. Weed Management:
- Critical in early growth stages as finger millet grows slowly initially
- First weeding: 2-3 weeks after emergence
- Second weeding: 5-6 weeks after emergence
- Thinning may be necessary if plants are too dense

5. Fertilizer Application:
- Finger millet responds well to organic manure
- Apply NPK (23:21:0) at 50kg/ha if soil fertility is low
- Avoid excessive nitrogen which can cause lodging

6. Pest and Disease Management:
- Generally resistant to pests and diseases
- Main disease is blast disease in humid conditions
- Rotate crops to reduce disease pressure
- Quelea birds can be a problem during grain filling

7. Harvesting:
- Harvest when heads turn brown (usually 3-4 months after planting)
- Cut heads with a sharp knife, leaving 10-15cm of stalk
- Dry thoroughly in the sun
- Thresh by hand or using simple tools
- Clean winnowing is important for quality

8. Storage:
- Store in dry, clean containers
- Finger millet stores well for 3-5 years if properly dried
- Protect from weevils and moisture

Finger millet is an excellent crop for food security as it has superior storage qualities compared to most other cereals. It is also highly nutritious with high calcium content. For small-scale farmers with limited resources, finger millet is an excellent crop choice.
            """,
            "category": "millet",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Pigeon Peas
        {
            "title": "Pigeon Pea Cultivation in Malawi",
            "content": """
Pigeon peas (Nandolo) are an important legume crop in Malawi that grows well even in dry conditions. Here's how to cultivate them successfully:

1. Land Preparation:
- Clear land of weeds and previous crop residues
- Plough to a depth of 15-20cm
- Pigeon peas can grow in poor soils but respond well to good land preparation

2. Varieties Recommended for Malawi:
- Early maturing (110-120 days): ICPL 87091, ICPL 87105
- Medium duration (150-180 days): ICEAP 00557, ICEAP 00554
- Long duration (180-270 days): ICEAP 00040, ICEAP 00053

3. Planting Time:
- Plant with the first rains (November-December)
- Early varieties can be planted as late as January

4. Seed Rate and Spacing:
- Pure stand: Rows 75-90cm apart, plants 30-50cm within rows
- Intercropping with maize: Plant pigeon peas between maize rows
- Seed rate: 8-10kg per hectare (pure stand)
- Planting depth: 3-5cm

5. Intercropping Systems:
- Pigeon peas work well intercropped with maize, sorghum, or millet
- For intercropping, use long-duration varieties with cereals
- Plant 1 row of pigeon peas for every 2-3 rows of cereal

6. Fertilizer Requirements:
- Pigeon peas fix nitrogen in the soil and generally need minimal fertilizer
- Apply small amounts of phosphorus (e.g., 23:21:0 at 50kg/ha) in poor soils
- Apply manure during land preparation if available

7. Weed Management:
- Keep fields weed-free for the first 6-8 weeks
- First weeding: 2-3 weeks after emergence
- Second weeding: 6-8 weeks after emergence

8. Pest and Disease Management:
- Major pests: Pod borers, pod-sucking bugs, and pod flies
- Major diseases: Fusarium wilt and sterility mosaic disease
- Use resistant varieties and good crop rotation
- Apply insecticides at flowering and podding if pest pressure is high

9. Harvesting:
- Harvest when pods turn brown and dry
- Early varieties: March-April
- Medium/late varieties: May-August
- Cut plants at base or pick mature pods
- Dry thoroughly before threshing

Pigeon peas are excellent for improving soil fertility and can be grown on the same land for 3-4 consecutive years. They provide food security as green peas during the hunger season and dried peas later. The stems also make good firewood after harvest.
            """,
            "category": "pigeon peas",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Cotton
        {
            "title": "Cotton Farming in Malawi",
            "content": """
Cotton is an important cash crop in Malawi, especially in the lower-lying areas. Here's a comprehensive guide to cotton cultivation:

1. Land Selection and Preparation:
- Choose well-drained soils with good water-holding capacity
- Clear land of all weeds and crop residues
- Plough to a depth of 20-30cm
- Prepare ridges 90cm apart

2. Varieties Recommended for Malawi:
- MACON 24: High-yielding and widely adapted
- RASCOM 59: Good fiber quality
- Makoka 2000: Disease resistant variety
- SZ 9314: High-yielding

3. Planting Time:
- Plant with the onset of reliable rains (mid-November to mid-December)
- Avoid late planting which reduces yields and increases pest pressure

4. Seed Rate and Spacing:
- Use 10-15kg of seed per hectare
- Plant on ridges 90cm apart
- Space plants 25-30cm within rows
- Plant 4-5 seeds per station, thin to 2 plants after emergence
- Planting depth: 2-3cm

5. Fertilizer Application:
- Apply 23:21:0+4S at planting (100kg/ha)
- Top-dress with CAN or Urea 4-6 weeks after emergence (50kg/ha)
- Avoid late application of nitrogen as it delays maturity

6. Weed Management:
- Keep fields weed-free, especially during the first 8 weeks
- First weeding: 2-3 weeks after emergence
- Second weeding: 5-6 weeks after emergence
- Third weeding: if necessary, at 8-9 weeks

7. Pest Management:
- Major pests: Bollworms, aphids, jassids, red spider mites
- Scout fields regularly for pests
- Apply appropriate insecticides as recommended by extension officers
- Practice integrated pest management to reduce costs

8. Disease Management:
- Major diseases: Bacterial blight, Fusarium wilt
- Use resistant varieties
- Practice crop rotation (avoid planting after cotton, okra or hibiscus)

9. Harvesting:
- Start picking when 50% of bolls are open
- Pick when dry (not early morning with dew)
- Sort while picking - keep clean cotton separate
- Store in clean, dry bags
- Multiple pickings may be necessary as bolls mature

10. Marketing:
- Sell to licensed buyers
- Ensure cotton is clean and dry
- Grade according to buyer specifications

Cotton requires careful management but can be very profitable with good practices. It's important to follow recommended pest management practices to ensure good yields and quality.
            """,
            "category": "cotton",
            "season": "rainy",
            "region": "Malawi"
        },
        
        # Tomatoes
        {
            "title": "Tomato Growing in Malawi",
            "content": """
Tomatoes are an important horticultural crop in Malawi with good market potential. Here's a guide to successful tomato cultivation:

1. Land Preparation and Soil Requirements:
- Tomatoes prefer well-drained, fertile soils with pH 5.5-7.0
- Prepare land thoroughly, removing all weeds
- Make raised beds in areas with heavy rainfall
- Add well-decomposed manure or compost (10-15 tons/hectare)

2. Varieties Suitable for Malawi:
- Rio Grande: Good for processing, heat tolerant
- Rodade: Disease resistant, good shelf life
- Heinz: Good for processing
- Money Maker: Good for fresh market
- Roma VF: Disease resistant, good for both fresh market and processing

3. Nursery Preparation:
- Prepare nursery beds 1m wide, 10-15cm high
- Treat nursery soil with insecticide to control soil-borne pests
- Sow seeds in lines 15cm apart
- Water carefully using watering can with fine rose
- Cover nursery with grass and remove when seeds germinate
- Seed rate: 300-400g per hectare

4. Transplanting:
- Transplant when seedlings are 15-20cm tall (3-4 weeks old)
- Harden seedlings by reducing watering 5-7 days before transplanting
- Transplant in the evening or on cloudy days
- Spacing: 90cm between rows, 45-60cm within rows

5. Fertilizer Application:
- Basal application: Apply 23:21:0 (200kg/ha) before transplanting
- Top dressing: Apply CAN (100kg/ha) 2-3 weeks after transplanting and again at flowering

6. Irrigation:
- Irrigate immediately after transplanting
- Regular watering is essential, especially during flowering and fruit development
- Water early in the morning or late evening
- Avoid overhead irrigation to reduce disease risks

7. Staking and Pruning:
- Stake plants 2-3 weeks after transplanting using sticks or string trellis
- Prune side shoots (suckers) regularly to promote better fruit development
- Remove lower leaves touching the ground to prevent disease

8. Pest Management:
- Major pests: Tomato fruitworm, whiteflies, aphids, red spider mites
- Use integrated pest management approaches
- Apply appropriate insecticides as per extension officer recommendations

9. Disease Management:
- Major diseases: Early and late blight, bacterial wilt, fusarium wilt
- Use resistant varieties
- Practice crop rotation (avoid planting after tomatoes, potatoes, or peppers)
- Remove and destroy infected plants
- Apply appropriate fungicides preventively during wet periods

10. Harvesting:
- Begin harvesting 70-90 days after transplanting
- Harvest when fruits are mature green or slightly pink for distant markets
- Harvest fully ripe fruit for local markets
- Harvest every 3-4 days
- Handle carefully to avoid bruising

Tomatoes can be highly profitable, especially during the dry season when prices are higher. With good irrigation facilities, tomatoes can be grown year-round in Malawi.
            """,
            "category": "vegetables",
            "season": "year-round",
            "region": "Malawi"
        },
        
        # Soybeans
        {
            "title": "Soybean Cultivation in Malawi",
            "content": """
Soybeans are becoming increasingly important in Malawi as a source of protein and oil. Here's a comprehensive guide to growing soybeans:

1. Land Preparation:
- Clear the land of weeds and crop residues
- Plough to a depth of 15-20cm
- Prepare a fine seedbed as soybean seeds are small
- Soybeans prefer well-drained, fertile soils

2. Varieties Recommended for Malawi:
- Makwacha: High yielding, tolerant to pod shattering
- Tikolore: Early maturing, good for drought-prone areas
- Solitaire: High yielding, good oil content
- Soprano: High protein content

3. Planting Time:
- Plant with the onset of reliable rains (December-early January)
- Early planting gives better yields but requires good soil moisture

4. Seed Rate and Spacing:
- Use 60-80kg of seed per hectare
- Row spacing: 45-60cm between rows
- Plant spacing: 5-10cm within rows
- Planting depth: 2-3cm

5. Inoculation:
- For best results, inoculate seeds with rhizobium inoculant
- Inoculation helps soybeans fix nitrogen from the air
- Mix seeds with inoculant just before planting
- Plant immediately after inoculation and avoid direct sunlight

6. Fertilizer Application:
- Soybeans fix their own nitrogen if properly inoculated
- Apply 23:21:0 at planting (100kg/ha) for phosphorus
- In very poor soils, small amounts of nitrogen may be needed at planting

7. Weed Management:
- Weed control is critical, especially in early growth stages
- First weeding: 2-3 weeks after emergence
- Second weeding: 5-6 weeks after emergence
- Consider pre-emergence herbicides in large fields

8. Pest and Disease Management:
- Major pests: Bean leaf beetles, pod borers, aphids
- Major diseases: Soybean rust, bacterial pustule, mosaic virus
- Use resistant varieties where available
- Scout fields regularly and apply appropriate control measures
- Practice crop rotation to minimize disease buildup

9. Harvesting:
- Harvest when:
  * Most leaves have fallen
  * Pods are dry and brown
  * Seeds rattle in the pods
- Cut plants at base or pull entire plants
- Thresh when completely dry
- Clean and dry seeds to 12% moisture content

10. Storage:
- Store in clean, dry bags
- Keep in well-ventilated storage
- Protect from weevils and moisture

Soybeans are excellent in crop rotation systems and help improve soil fertility. They have great potential as both a food security crop and cash crop in Malawi, with growing markets for processing into various products.
            """,
            "category": "soybean",
            "season": "rainy",
            "region": "Malawi"
        }
    ]
    
    # Add tips to database
    with app.app_context():
        for tip in tips:
            # Check if tip already exists
            existing_tip = FarmingTip.query.filter_by(title=tip["title"]).first()
            if not existing_tip:
                new_tip = FarmingTip(
                    title=tip["title"],
                    content=tip["content"],
                    category=tip["category"],
                    season=tip["season"],
                    region=tip["region"],
                    created_at=datetime.utcnow()
                )
                db.session.add(new_tip)
        
        # Commit changes
        db.session.commit()
        print("Successfully added Malawi farming tips to the database.")

if __name__ == "__main__":
    add_tips()