from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import random
import re
from datetime import datetime
import os
from dataclasses import dataclass

app = FastAPI(title="Premium Jewelry Recommender API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enhanced jewelry database with premium focus
PREMIUM_JEWELRY_DATA = {
    "diamonds": {
        "round": {"brilliance": "exceptional", "price_premium": 1.0, "story_themes": ["timeless", "classic", "eternal"]},
        "princess": {"brilliance": "excellent", "price_premium": 0.85, "story_themes": ["modern", "bold", "confident"]},
        "cushion": {"brilliance": "romantic", "price_premium": 0.80, "story_themes": ["vintage", "romantic", "soft"]},
        "emerald": {"brilliance": "elegant", "price_premium": 0.75, "story_themes": ["sophisticated", "art deco", "architectural"]},
        "oval": {"brilliance": "graceful", "price_premium": 0.90, "story_themes": ["elongating", "graceful", "unique"]},
        "pear": {"brilliance": "unique", "price_premium": 0.75, "story_themes": ["teardrops of joy", "unique", "artistic"]},
        "marquise": {"brilliance": "dramatic", "price_premium": 0.70, "story_themes": ["regal", "dramatic", "vintage"]},
        "heart": {"brilliance": "romantic", "price_premium": 0.75, "story_themes": ["ultimate love", "romantic", "symbolic"]}
    },
    "premium_metals": {
        "platinum": {
            "price_per_gram": 45,
            "durability": "lifetime",
            "story": "Rarer than gold, platinum represents eternal commitment",
            "personality_match": ["sophisticated", "classic", "refined"]
        },
        "white_gold": {
            "price_per_gram": 65,
            "durability": "excellent",
            "story": "Modern elegance with timeless appeal",
            "personality_match": ["contemporary", "clean", "minimalist"]
        },
        "yellow_gold": {
            "price_per_gram": 70,
            "durability": "excellent", 
            "story": "Traditional warmth and golden memories",
            "personality_match": ["traditional", "warm", "classic"]
        },
        "rose_gold": {
            "price_per_gram": 68,
            "durability": "excellent",
            "story": "Romantic blush of copper creates unique beauty",
            "personality_match": ["romantic", "unique", "artistic", "bohemian"]
        }
    },
    "story_themes": {
        "beach": {"metals": ["white_gold", "platinum"], "shapes": ["oval", "pear"], "style": "organic flowing"},
        "vintage": {"metals": ["rose_gold", "yellow_gold"], "shapes": ["cushion", "emerald"], "style": "art deco details"},
        "nature": {"metals": ["rose_gold", "yellow_gold"], "shapes": ["oval", "pear"], "style": "organic textures"},
        "artistic": {"metals": ["rose_gold", "white_gold"], "shapes": ["princess", "emerald"], "style": "sculptural unique"},
        "minimalist": {"metals": ["platinum", "white_gold"], "shapes": ["round", "princess"], "style": "clean modern"},
        "bohemian": {"metals": ["rose_gold", "yellow_gold"], "shapes": ["oval", "pear"], "style": "organic flowing"}
    }
}

# Story analysis keywords
STORY_KEYWORDS = {
    "romantic": ["love", "romantic", "sunset", "candles", "roses", "proposal", "heart", "valentine"],
    "vintage": ["vintage", "antique", "classic", "old", "grandmother", "heirloom", "traditional"],
    "nature": ["nature", "hiking", "outdoors", "garden", "flowers", "trees", "beach", "mountains"],
    "artistic": ["art", "creative", "artist", "paint", "design", "unique", "sculpture", "gallery"],
    "minimalist": ["simple", "clean", "minimal", "modern", "sleek", "understated"],
    "bohemian": ["boho", "free", "creative", "artistic", "unconventional", "indie", "eclectic"],
    "sophisticated": ["elegant", "refined", "classy", "sophisticated", "professional", "executive"],
    "adventurous": ["travel", "adventure", "explore", "journey", "discover", "wanderlust"]
}

# Pydantic models
class StoryData(BaseModel):
    love_story: Optional[str] = None
    personality: Optional[str] = None
    style_preferences: Optional[str] = None
    special_moments: Optional[str] = None
    occasion: Optional[str] = None
    timeline: Optional[str] = None

class PremiumPreferences(BaseModel):
    ring_type: Optional[str] = None
    center_stone: Optional[str] = None
    metal_type: Optional[str] = None
    budget_range: Optional[str] = None
    design_inspiration: Optional[str] = None

class StoryRecommendationRequest(BaseModel):
    story: StoryData
    preferences: PremiumPreferences
    type: str = "story_based"

class PremiumDesign(BaseModel):
    id: str
    stone_type: str = "diamond"
    stone_shape: str
    stone_color: str
    stone_clarity: str
    carat_weight: float
    metal_type: str
    setting_type: str
    estimated_price: float
    rationale: str
    story_connection: Optional[str] = None
    style_tags: List[str]
    premium_features: List[str]

# In-memory storage
user_sessions = {}
story_sessions = {}

@dataclass
class StoryAnalysis:
    themes: List[str]
    style_indicators: List[str]
    personality_traits: List[str]
    emotional_keywords: List[str]
    recommended_elements: Dict[str, Any]

def analyze_story_text(story_data: StoryData) -> StoryAnalysis:
    """Analyze story text for themes, personality, and style indicators"""
    
    # Combine all story text
    full_text = " ".join([
        story_data.love_story or "",
        story_data.personality or "",
        story_data.style_preferences or "",
        story_data.special_moments or ""
    ]).lower()
    
    themes = []
    style_indicators = []
    personality_traits = []
    emotional_keywords = []
    
    # Analyze for story themes
    for theme, keywords in STORY_KEYWORDS.items():
        keyword_count = sum(1 for keyword in keywords if keyword in full_text)
        if keyword_count > 0:
            themes.append(theme)
            if keyword_count >= 2:  # Strong indicator
                style_indicators.append(theme)
    
    # Extract emotional keywords
    emotion_words = ["love", "joy", "happiness", "passion", "devotion", "cherish", "adore"]
    emotional_keywords = [word for word in emotion_words if word in full_text]
    
    # Determine personality traits from text patterns
    if any(word in full_text for word in ["quiet", "introverted", "shy", "private"]):
        personality_traits.append("introverted")
    if any(word in full_text for word in ["outgoing", "social", "party", "friends"]):
        personality_traits.append("extroverted")
    if any(word in full_text for word in ["creative", "artistic", "paint", "design"]):
        personality_traits.append("creative")
    if any(word in full_text for word in ["active", "sports", "hiking", "gym"]):
        personality_traits.append("active")
    
    # Generate recommendations based on analysis
    recommended_elements = {}
    
    # Recommend metal based on themes
    if "vintage" in themes or "romantic" in themes:
        recommended_elements["metals"] = ["rose_gold", "yellow_gold"]
    elif "minimalist" in themes or "modern" in style_indicators:
        recommended_elements["metals"] = ["platinum", "white_gold"]
    else:
        recommended_elements["metals"] = ["white_gold", "platinum"]
    
    # Recommend shapes based on personality
    if "romantic" in themes:
        recommended_elements["shapes"] = ["round", "cushion", "heart"]
    elif "minimalist" in themes:
        recommended_elements["shapes"] = ["round", "princess", "emerald"]
    elif "artistic" in themes:
        recommended_elements["shapes"] = ["pear", "marquise", "oval"]
    else:
        recommended_elements["shapes"] = ["round", "oval", "cushion"]
    
    return StoryAnalysis(
        themes=themes[:3],  # Top 3 themes
        style_indicators=style_indicators,
        personality_traits=personality_traits,
        emotional_keywords=emotional_keywords,
        recommended_elements=recommended_elements
    )

def generate_story_connection(design: Dict, story_analysis: StoryAnalysis, story_data: StoryData) -> str:
    """Generate a personalized story connection for each design"""
    
    connections = []
    
    # Connect to themes
    if "romantic" in story_analysis.themes:
        if design["stone_shape"] == "heart":
            connections.append("The heart shape literally embodies the love you share")
        elif design["stone_shape"] == "round":
            connections.append("Like your love, a round diamond has no beginning or end - it's eternal")
        elif design["metal_type"] == "rose_gold":
            connections.append("Rose gold's warm blush mirrors the romantic glow you bring to each other's lives")
    
    if "vintage" in story_analysis.themes:
        if design["stone_shape"] in ["cushion", "emerald"]:
            connections.append("This vintage-inspired cut echoes the timeless romance you both cherish")
        if design["metal_type"] == "yellow_gold":
            connections.append("Yellow gold connects you to generations of love stories before yours")
    
    if "nature" in story_analysis.themes:
        if design["stone_shape"] in ["oval", "pear"]:
            connections.append("The organic curves mirror the natural beauty where your love story began")
        if "hiking" in (story_data.love_story or ""):
            connections.append("Durable enough for all your adventures together, from mountain peaks to everyday moments")
    
    if "artistic" in story_analysis.themes:
        if design["stone_shape"] in ["pear", "marquise"]:
            connections.append("This unique cut reflects your creative spirits and artistic appreciation")
    
    # Connect to special moments
    if story_data.special_moments:
        special_text = story_data.special_moments.lower()
        if "laugh" in special_text:
            connections.append("The way light dances through this diamond reminds us of how she lights up when she laughs")
        if "hands" in special_text:
            connections.append("Designed to complement the graceful hands that create such beautiful art")
        if "eyes" in special_text:
            connections.append("The brilliance matches the sparkle we see in her eyes when she's truly happy")
    
    # Default connection if no specific matches
    if not connections:
        connections.append(f"This {design['stone_shape']} diamond in {design['metal_type'].replace('_', ' ')} celebrates your unique love story")
    
    return random.choice(connections)

def calculate_premium_price(stone_shape: str, carat_weight: float, metal_type: str, 
                          setting_complexity: float = 1.0, story_premium: bool = False) -> float:
    """Calculate price with premium considerations"""
    
    # Base diamond price (premium quality assumed)
    base_diamond_price = 8000  # Premium grade diamonds
    shape_premium = PREMIUM_JEWELRY_DATA["diamonds"].get(stone_shape, {}).get("price_premium", 1.0)
    
    # Carat weight with exponential pricing
    carat_price = base_diamond_price * (carat_weight ** 1.5) * shape_premium
    
    # Premium metal pricing
    metal_data = PREMIUM_JEWELRY_DATA["premium_metals"].get(metal_type, {})
    metal_price = metal_data.get("price_per_gram", 50) * 6  # 6g average for premium setting
    
    # Setting complexity
    setting_base = 1200 * setting_complexity  # Premium craftsmanship
    
    # Story customization premium
    story_premium_cost = 800 if story_premium else 0
    
    total = carat_price + metal_price + setting_base + story_premium_cost
    return round(total, 2)

def generate_premium_suggestions(story_analysis: StoryAnalysis, story_data: StoryData, 
                               preferences: PremiumPreferences) -> List[PremiumDesign]:
    """Generate premium jewelry suggestions with story integration"""
    
    suggestions = []
    
    # Extract budget range
    budget_ranges = {
        "5000-10000": (5000, 10000),
        "10000-20000": (10000, 20000),
        "20000-50000": (20000, 50000),
        "50000-100000": (50000, 100000),
        "100000+": (100000, 500000),
        "consultation": (20000, 100000)
    }
    
    budget_min, budget_max = budget_ranges.get(preferences.budget_range, (10000, 30000))
    
    # Generate 3 suggestions with different approaches
    approaches = [
        {"focus": "story_optimized", "carat_range": (0.8, 1.5), "premium_factor": 1.2},
        {"focus": "balanced", "carat_range": (1.0, 2.0), "premium_factor": 1.0},
        {"focus": "statement", "carat_range": (1.5, 3.0), "premium_factor": 1.1}
    ]
    
    for i, approach in enumerate(approaches):
        # Select components based on story analysis
        recommended_metals = story_analysis.recommended_elements.get("metals", ["white_gold"])
        recommended_shapes = story_analysis.recommended_elements.get("shapes", ["round"])
        
        metal_type = preferences.metal_type or random.choice(recommended_metals)
        stone_shape = random.choice(recommended_shapes)
        
        # Adjust carat weight to fit budget
        target_carat = random.uniform(*approach["carat_range"])
        max_affordable_carat = (budget_max * 0.8) / (8000 * approach["premium_factor"])
        carat_weight = min(target_carat, max_affordable_carat)
        carat_weight = max(0.5, round(carat_weight, 2))
        
        # Premium clarity and color
        clarity_options = ["FL", "IF", "VVS1", "VVS2", "VS1"]
        stone_clarity = random.choice(clarity_options)
        stone_color = "D" if random.random() > 0.7 else random.choice(["E", "F", "G"])
        
        # Setting based on style
        setting_options = {
            "vintage": ["vintage", "halo", "milgrain"],
            "modern": ["prong", "bezel", "tension"],
            "romantic": ["halo", "vintage", "pave"]
        }
        
        primary_theme = story_analysis.themes[0] if story_analysis.themes else "classic"
        available_settings = setting_options.get(primary_theme, ["prong", "halo"])
        setting_type = random.choice(available_settings)
        
        # Calculate price
        estimated_price = calculate_premium_price(
            stone_shape, carat_weight, metal_type, 
            setting_complexity=1.3, story_premium=True
        )
        
        # Ensure within budget
        if estimated_price > budget_max:
            # Reduce carat weight to fit budget
            target_carat = (budget_max * 0.9) / (8000 * approach["premium_factor"])
            carat_weight = max(0.5, round(target_carat, 2))
            estimated_price = calculate_premium_price(
                stone_shape, carat_weight, metal_type, 
                setting_complexity=1.3, story_premium=True
            )
        
        # Generate design
        design_dict = {
            "stone_shape": stone_shape,
            "stone_type": "diamond",
            "metal_type": metal_type,
            "stone_clarity": stone_clarity,
            "carat_weight": carat_weight,
            "stone_color": stone_color,
            "setting_type": setting_type
        }
        
        design = PremiumDesign(
            id=f"lumiere_{random.randint(1000, 9999)}_{datetime.now().strftime('%H%M%S')}",
            stone_type="diamond",
            stone_shape=stone_shape,
            stone_color=f"{stone_color} (Colorless)" if stone_color in ["D", "E", "F"] else f"{stone_color} (Near Colorless)",
            stone_clarity=stone_clarity,
            carat_weight=carat_weight,
            metal_type=metal_type,
            setting_type=setting_type,
            estimated_price=estimated_price,
            rationale=generate_premium_rationale(design_dict, approach["focus"], story_analysis),
            story_connection=generate_story_connection(design_dict, story_analysis, story_data),
            style_tags=story_analysis.themes[:2] + [approach["focus"]],
            premium_features=generate_premium_features(design_dict, story_analysis)
        )
        
        suggestions.append(design)
    
    return suggestions

def generate_premium_rationale(design: Dict, focus: str, story_analysis: StoryAnalysis) -> str:
    """Generate sophisticated rationale for premium recommendations"""
    
    rationales = {
        "story_optimized": f"This design harmoniously weaves your personal story into every detail. The {design['stone_shape']} cut and {design['metal_type'].replace('_', ' ')} setting were specifically chosen to reflect the {', '.join(story_analysis.themes[:2])} elements of your journey together.",
        
        "balanced": f"Representing the perfect balance of exceptional quality and meaningful design, this {design['carat_weight']}-carat {design['stone_shape']} diamond achieves optimal brilliance while honoring your style preferences. The {design['stone_clarity']} clarity ensures maximum light return.",
        
        "statement": f"For those moments when only the extraordinary will do, this magnificent {design['carat_weight']}-carat centerpiece commands attention while maintaining sophisticated elegance. The {design['metal_type'].replace('_', ' ')} setting provides the perfect stage for this remarkable diamond."
    }
    
    base_rationale = rationales.get(focus, rationales["balanced"])
    
    # Add technical excellence note
    technical_note = f" Certified for exceptional cut quality and {design['stone_clarity']} clarity grade, this piece represents the pinnacle of diamond craftsmanship."
    
    return base_rationale + technical_note

def generate_premium_features(design: Dict, story_analysis: StoryAnalysis) -> List[str]:
    """Generate list of premium features for the design"""
    
    features = [
        "GIA Certified Diamond",
        "Premium Cut Grade: Excellent",
        "Conflict-Free Sourcing Guarantee",
        "Lifetime Warranty & Service",
        "Custom Story Engraving Available"
    ]
    
    # Add metal-specific features
    metal_features = {
        "platinum": "Platinum Purity Hallmark",
        "white_gold": "Rhodium Plated Finish",
        "rose_gold": "Proprietary Rose Gold Alloy",
        "yellow_gold": "18K Gold Purity"
    }
    
    if design["metal_type"] in metal_features:
        features.append(metal_features[design["metal_type"]])
    
    # Add story-specific features
    if "vintage" in story_analysis.themes:
        features.append("Hand-Engraved Milgrain Details")
    if "artistic" in story_analysis.themes:
        features.append("Sculptural Setting Design")
    
    return features[:5]  # Return top 5 features

# API Routes
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/api/story-recommendations")
async def create_story_recommendations(request: StoryRecommendationRequest):
    """Generate recommendations based on customer story and preferences"""
    
    session_id = f"lumiere_{random.randint(10000, 99999)}"
    
    try:
        # Analyze the story
        story_analysis = analyze_story_text(request.story)
        
        # Generate premium suggestions
        suggestions = generate_premium_suggestions(story_analysis, request.story, request.preferences)
        
        # Create story insights
        story_insights = {
            "themes": story_analysis.themes,
            "style_match": f"{story_analysis.themes[0].title()} Romance" if story_analysis.themes else "Classic Elegance",
            "emotional_connection": len(story_analysis.emotional_keywords),
            "personalization_level": "High"
        }
        
        # Store in session
        story_sessions[session_id] = {
            "story": request.story.dict(),
            "preferences": request.preferences.dict(),
            "story_analysis": {
                "themes": story_analysis.themes,
                "style_indicators": story_analysis.style_indicators,
                "personality_traits": story_analysis.personality_traits
            },
            "suggestions": [s.dict() for s in suggestions],
            "timestamp": datetime.now().isoformat()
        }
        
        message = f"Based on your beautiful love story, we've crafted three exceptional pieces that capture the essence of your journey. Each design reflects the {', '.join(story_analysis.themes[:2])} elements that make your relationship unique."
        
        return {
            "session_id": session_id,
            "suggestions": [s.dict() for s in suggestions],
            "message": message,
            "story_insights": story_insights,
            "personalization_score": min(100, len(story_analysis.themes) * 25 + len(story_analysis.emotional_keywords) * 10)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating story recommendations: {str(e)}")

@app.post("/api/preferences")
async def collect_preferences(preferences: PremiumPreferences):
    """Generate recommendations based on preferences only"""
    
    session_id = f"lumiere_{random.randint(10000, 99999)}"
    
    try:
        # Create default story analysis for preference-based recommendations
        default_analysis = StoryAnalysis(
            themes=["classic"],
            style_indicators=["elegant"],
            personality_traits=[],
            emotional_keywords=[],
            recommended_elements={
                "metals": ["white_gold", "platinum"],
                "shapes": ["round", "oval", "princess"]
            }
        )
        
        # Create minimal story data
        default_story = StoryData()
        
        suggestions = generate_premium_suggestions(default_analysis, default_story, preferences)
        
        user_sessions[session_id] = {
            "preferences": preferences.dict(),
            "suggestions": [s.dict() for s in suggestions],
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "session_id": session_id,
            "suggestions": [s.dict() for s in suggestions],
            "message": "Here are three exceptional pieces selected based on your preferences, each representing the pinnacle of diamond craftsmanship."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/api/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    """Handle multiple image uploads for style analysis"""
    
    session_id = f"lumiere_{random.randint(10000, 99999)}"
    
    try:
        # Mock image analysis for multiple images
        detected_styles = []
        confidence_scores = []
        
        for file in files:
            if not file.content_type.startswith("image/"):
                continue
                
            # Simulate advanced image analysis
            styles = random.sample(["vintage", "modern", "romantic", "minimalist", "bohemian"], k=2)
            detected_styles.extend(styles)
            confidence_scores.append(random.uniform(0.75, 0.95))
        
        # Aggregate analysis results
        style_counts = {}
        for style in detected_styles:
            style_counts[style] = style_counts.get(style, 0) + 1
        
        # Get most common styles
        top_styles = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        primary_themes = [style for style, count in top_styles]
        
        # Create analysis based on detected styles
        image_analysis = StoryAnalysis(
            themes=primary_themes,
            style_indicators=primary_themes,
            personality_traits=[],
            emotional_keywords=[],
            recommended_elements={
                "metals": ["rose_gold", "white_gold"] if "romantic" in primary_themes else ["platinum", "white_gold"],
                "shapes": ["round", "cushion"] if "vintage" in primary_themes else ["round", "princess"]
            }
        )
        
        # Create preferences from image analysis
        preferences = PremiumPreferences(
            ring_type="engagement",
            metal_type=random.choice(image_analysis.recommended_elements["metals"]),
            design_inspiration=f"Inspired by {', '.join(primary_themes)} visual elements"
        )
        
        suggestions = generate_premium_suggestions(image_analysis, StoryData(), preferences)
        
        user_sessions[session_id] = {
            "image_analysis": {
                "detected_styles": primary_themes,
                "confidence": sum(confidence_scores) / len(confidence_scores),
                "style_distribution": style_counts
            },
            "suggestions": [s.dict() for s in suggestions],
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "session_id": session_id,
            "suggestions": [s.dict() for s in suggestions],
            "message": f"Your visual inspiration reveals {', '.join(primary_themes)} design preferences. Here are three pieces that capture those aesthetic elements.",
            "image_analysis": {
                "detected_styles": primary_themes,
                "confidence": sum(confidence_scores) / len(confidence_scores)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing images: {str(e)}")

@app.post("/api/shortlist")
async def add_to_shortlist(request: dict):
    """Add design to premium collection"""
    
    design_id = request.get("design_id")
    session_id = request.get("user_session")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    # Implementation for shortlisting would go here
    return {
        "message": "Added to your premium collection! Our diamond specialist will prepare detailed specifications for your viewing.",
        "collection_status": "premium",
        "next_steps": "Schedule private consultation to view piece"
    }

@app.get("/api/data/options")
async def get_premium_options():
    """Get premium jewelry options"""
    return {
        "diamond_shapes": list(PREMIUM_JEWELRY_DATA["diamonds"].keys()),
        "premium_metals": list(PREMIUM_JEWELRY_DATA["premium_metals"].keys()),
        "story_themes": list(PREMIUM_JEWELRY_DATA["story_themes"].keys()),
        "budget_ranges": [
            "5000-10000", "10000-20000", "20000-50000", 
            "50000-100000", "100000+", "consultation"
        ],
        "occasions": ["engagement", "anniversary", "birthday", "valentine", "just_because", "milestone"]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Create static directory if it doesn't exist
    if not os.path.exists("static"):
        os.makedirs("static")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {"message": "Frontend not found. Please ensure static/index.html exists."}