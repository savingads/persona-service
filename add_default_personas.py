#!/usr/bin/env python3
"""
Add default personas to the persona service database.
"""
import os
import json
from sqlalchemy import text
from app.models import Persona, DemographicData, PersonaAttributes, AttributeCategory, init_db

def add_default_personas(session):
    """Create default personas based on legacy sample data"""
    
    # Sample personas for different regions
    personas = [
        # North America (US) Persona
        {
            "name": "Alex Johnson",
            "demographic": {
                "latitude": 37.7749,
                "longitude": -122.4194,  # San Francisco
                "language": "en-US",
                "country": "US",
                "city": "San Francisco",
                "region": "California",
                "age": 32,
                "gender": "Male",
                "education": "Master's Degree",
                "income": "High",
                "occupation": "Software Engineer"
            },
            "psychographic": {
                "interests": ["technology", "hiking", "craft beer", "photography"],
                "personal_values": ["innovation", "work-life balance", "environmental sustainability"],
                "attitudes": ["optimistic", "progressive", "tech-savvy"],
                "lifestyle": "Urban professional",
                "personality": "Analytical, creative",
                "opinions": ["privacy-focused", "pro-innovation"]
            },
            "behavioral": {
                "browsing_habits": ["tech news", "social media", "productivity tools"],
                "purchase_history": ["electronics", "outdoor gear", "subscription services"],
                "brand_interactions": ["Apple", "Patagonia", "Spotify"],
                "device_usage": {"mobile": "4 hours/day", "desktop": "8 hours/day", "tablet": "1 hour/day"},
                "social_media_activity": {"twitter": "daily", "instagram": "weekly", "linkedin": "daily"},
                "content_consumption": {"videos": "2 hours/day", "articles": "10/day", "podcasts": "5/week"}
            },
            "contextual": {
                "time_of_day": "morning",
                "day_of_week": "weekday",
                "season": "spring",
                "weather": "sunny",
                "device_type": "desktop",
                "browser_type": "chrome",
                "screen_size": "1920x1080",
                "connection_type": "wifi"
            }
        },
        
        # South America (Brazil) Persona
        {
            "name": "Isabela Santos",
            "demographic": {
                "latitude": -23.5505,
                "longitude": -46.6333,  # São Paulo
                "language": "pt-BR",
                "country": "BR",
                "city": "São Paulo",
                "region": "São Paulo",
                "age": 28,
                "gender": "Female",
                "education": "Bachelor's Degree",
                "income": "Medium",
                "occupation": "Marketing Specialist"
            },
            "psychographic": {
                "interests": ["fashion", "travel", "cooking", "social media"],
                "personal_values": ["family", "community", "cultural heritage"],
                "attitudes": ["social", "expressive", "trend-conscious"],
                "lifestyle": "Urban socialite",
                "personality": "Extroverted, creative",
                "opinions": ["community-focused", "culturally proud"]
            },
            "behavioral": {
                "browsing_habits": ["social media", "fashion blogs", "travel sites"],
                "purchase_history": ["clothing", "cosmetics", "travel experiences"],
                "brand_interactions": ["Havaianas", "Natura", "Instagram"],
                "device_usage": {"mobile": "6 hours/day", "desktop": "4 hours/day", "tablet": "2 hours/day"},
                "social_media_activity": {"instagram": "hourly", "facebook": "daily", "tiktok": "daily"},
                "content_consumption": {"videos": "3 hours/day", "articles": "5/day", "social media": "4 hours/day"}
            },
            "contextual": {
                "time_of_day": "evening",
                "day_of_week": "all week",
                "season": "summer",
                "weather": "warm",
                "device_type": "mobile",
                "browser_type": "chrome",
                "screen_size": "375x812",
                "connection_type": "4g"
            }
        },
        
        # Europe (Germany) Persona
        {
            "name": "Lukas Schmidt",
            "demographic": {
                "latitude": 52.5200,
                "longitude": 13.4050,  # Berlin
                "language": "de-DE",
                "country": "DE",
                "city": "Berlin",
                "region": "Berlin",
                "age": 35,
                "gender": "Male",
                "education": "PhD",
                "income": "High",
                "occupation": "Research Scientist"
            },
            "psychographic": {
                "interests": ["classical music", "literature", "environmental issues", "cycling"],
                "personal_values": ["precision", "efficiency", "environmental responsibility"],
                "attitudes": ["analytical", "detail-oriented", "environmentally conscious"],
                "lifestyle": "Eco-conscious urban dweller",
                "personality": "Methodical, thoughtful",
                "opinions": ["pro-environment", "pro-EU", "privacy advocate"]
            },
            "behavioral": {
                "browsing_habits": ["news sites", "academic journals", "environmental blogs"],
                "purchase_history": ["books", "sustainable products", "quality electronics"],
                "brand_interactions": ["Bosch", "Deutsche Bahn", "Birkenstock"],
                "device_usage": {"mobile": "2 hours/day", "desktop": "7 hours/day", "e-reader": "1 hour/day"},
                "social_media_activity": {"twitter": "weekly", "linkedin": "daily", "facebook": "rarely"},
                "content_consumption": {"articles": "15/day", "books": "2/week", "documentaries": "3/week"}
            },
            "contextual": {
                "time_of_day": "morning",
                "day_of_week": "weekday",
                "season": "fall",
                "weather": "cloudy",
                "device_type": "desktop",
                "browser_type": "firefox",
                "screen_size": "2560x1440",
                "connection_type": "ethernet"
            }
        },
        
        # Asia (Japan) Persona
        {
            "name": "Yuki Tanaka",
            "demographic": {
                "latitude": 35.6762,
                "longitude": 139.6503,  # Tokyo
                "language": "ja-JP",
                "country": "JP",
                "city": "Tokyo",
                "region": "Tokyo",
                "age": 24,
                "gender": "Female",
                "education": "Bachelor's Degree",
                "income": "Medium",
                "occupation": "UX Designer"
            },
            "psychographic": {
                "interests": ["anime", "technology", "minimalist design", "photography"],
                "personal_values": ["harmony", "innovation", "aesthetics"],
                "attitudes": ["tech-forward", "detail-oriented", "trend-conscious"],
                "lifestyle": "Urban tech enthusiast",
                "personality": "Creative, meticulous",
                "opinions": ["design-focused", "tech-optimist"]
            },
            "behavioral": {
                "browsing_habits": ["design blogs", "tech news", "social media", "anime streaming"],
                "purchase_history": ["digital content", "tech gadgets", "design books"],
                "brand_interactions": ["Nintendo", "Muji", "Uniqlo"],
                "device_usage": {"mobile": "5 hours/day", "desktop": "6 hours/day", "gaming console": "2 hours/day"},
                "social_media_activity": {"twitter": "hourly", "instagram": "daily", "line": "hourly"},
                "content_consumption": {"anime": "2 hours/day", "tech articles": "8/day", "design tutorials": "3/week"}
            },
            "contextual": {
                "time_of_day": "night",
                "day_of_week": "all week",
                "season": "spring",
                "weather": "mild",
                "device_type": "laptop",
                "browser_type": "chrome",
                "screen_size": "1440x900",
                "connection_type": "wifi"
            }
        },
        
        # Africa (South Africa) Persona
        {
            "name": "Thabo Ndlovu",
            "demographic": {
                "latitude": -26.2041,
                "longitude": 28.0473,  # Johannesburg
                "language": "en-ZA",
                "country": "ZA",
                "city": "Johannesburg",
                "region": "Gauteng",
                "age": 30,
                "gender": "Male",
                "education": "Bachelor's Degree",
                "income": "Medium",
                "occupation": "Entrepreneur"
            },
            "psychographic": {
                "interests": ["business", "football", "music", "community development"],
                "personal_values": ["community", "ambition", "cultural heritage"],
                "attitudes": ["optimistic", "resourceful", "community-minded"],
                "lifestyle": "Ambitious professional",
                "personality": "Outgoing, determined",
                "opinions": ["pro-development", "community-focused"]
            },
            "behavioral": {
                "browsing_habits": ["business news", "sports sites", "educational content"],
                "purchase_history": ["business tools", "mobile data", "local products"],
                "brand_interactions": ["MTN", "Vodacom", "Standard Bank"],
                "device_usage": {"mobile": "7 hours/day", "laptop": "5 hours/day"},
                "social_media_activity": {"whatsapp": "hourly", "facebook": "daily", "twitter": "daily"},
                "content_consumption": {"news": "multiple times/day", "business articles": "5/day", "sports": "daily"}
            },
            "contextual": {
                "time_of_day": "all day",
                "day_of_week": "weekday",
                "season": "summer",
                "weather": "sunny",
                "device_type": "mobile",
                "browser_type": "chrome",
                "screen_size": "412x915",
                "connection_type": "4g"
            }
        }
    ]
    
    # Add each persona to the database
    for persona_data in personas:
        # Create the persona
        persona = Persona(name=persona_data["name"])
        session.add(persona)
        session.flush()  # To get the ID
        
        # Create demographic data
        demo_data = persona_data["demographic"]
        demographic = DemographicData(
            persona_id=persona.id,
            latitude=demo_data.get("latitude"),
            longitude=demo_data.get("longitude"),
            language=demo_data.get("language"),
            country=demo_data.get("country"),
            city=demo_data.get("city"),
            region=demo_data.get("region"),
            age=demo_data.get("age"),
            gender=demo_data.get("gender"),
            education=demo_data.get("education"),
            income=demo_data.get("income"),
            occupation=demo_data.get("occupation")
        )
        session.add(demographic)
        
        # Add psychographic attributes
        if "psychographic" in persona_data:
            psycho_attr = PersonaAttributes(
                persona_id=persona.id,
                category=AttributeCategory.PSYCHOGRAPHIC,
                data=json.dumps(persona_data["psychographic"])
            )
            session.add(psycho_attr)
        
        # Add behavioral attributes
        if "behavioral" in persona_data:
            behav_attr = PersonaAttributes(
                persona_id=persona.id,
                category=AttributeCategory.BEHAVIORAL,
                data=json.dumps(persona_data["behavioral"])
            )
            session.add(behav_attr)
        
        # Add contextual attributes
        if "contextual" in persona_data:
            context_attr = PersonaAttributes(
                persona_id=persona.id,
                category=AttributeCategory.CONTEXTUAL,
                data=json.dumps(persona_data["contextual"])
            )
            session.add(context_attr)
        
        print(f"Created persona: {persona_data['name']} (ID: {persona.id})")
    
    # Commit all changes
    session.commit()
    print("Default personas added successfully!")

def check_existing_personas(session):
    """Check if personas already exist in the database"""
    result = session.execute(text("SELECT COUNT(*) FROM personas"))
    count = result.scalar()
    return count > 0

def main():
    """Main function"""
    print("Initializing persona service database session...")
    session = init_db()
    
    # Check if personas already exist
    if check_existing_personas(session):
        print("Database already contains personas. Skipping default persona creation.")
        return
    
    print("Adding default personas to database...")
    add_default_personas(session)

if __name__ == "__main__":
    main()
