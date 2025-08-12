from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import random
import asyncio
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="AI E-commerce Recommendation Service",
    description="AI-powered product recommendation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    sku: str
    is_featured: bool = False

class RecommendationRequest(BaseModel):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    limit: int = 10

class RecommendationResponse(BaseModel):
    user_id: Optional[int]
    recommendations: List[Product]
    strategy: str
    confidence_score: float
    generated_at: datetime

# Sample products data (in production, this would come from database)
SAMPLE_PRODUCTS = [
    Product(id=1, name="Smartphone Pro Max", description="Latest flagship smartphone", price=999.99, category_id=1, sku="PHONE-001", is_featured=True),
    Product(id=2, name="Wireless Headphones", description="Premium noise-cancelling headphones", price=299.99, category_id=1, sku="AUDIO-001", is_featured=True),
    Product(id=3, name="Ultra-Slim Laptop", description="High-performance laptop", price=1299.99, category_id=1, sku="LAPTOP-001", is_featured=True),
    Product(id=4, name="Smart Watch", description="Advanced smartwatch with health monitoring", price=399.99, category_id=1, sku="WATCH-001"),
    Product(id=5, name="Organic Cotton T-Shirt", description="Comfortable organic cotton t-shirt", price=29.99, category_id=2, sku="SHIRT-001"),
    Product(id=6, name="Designer Jeans", description="Premium denim jeans", price=89.99, category_id=2, sku="JEANS-001"),
    Product(id=7, name="Running Shoes Pro", description="Professional running shoes", price=149.99, category_id=2, sku="SHOES-001", is_featured=True),
    Product(id=8, name="Programming Book", description="Learn modern programming", price=49.99, category_id=3, sku="BOOK-001"),
    Product(id=9, name="AI Machine Learning Guide", description="Complete AI guide", price=59.99, category_id=3, sku="BOOK-002"),
    Product(id=10, name="Garden Tools Set", description="Professional gardening tools", price=129.99, category_id=4, sku="GARDEN-001"),
    Product(id=11, name="Smart Security System", description="AI-powered home security", price=299.99, category_id=4, sku="SECURITY-001", is_featured=True),
    Product(id=12, name="Yoga Mat Premium", description="Non-slip premium yoga mat", price=39.99, category_id=5, sku="YOGA-001"),
    Product(id=13, name="Dumbbells Set", description="Adjustable dumbbells set", price=199.99, category_id=5, sku="WEIGHTS-001")
]

# AI Recommendation Engine (Simplified)
class RecommendationEngine:
    def __init__(self):
        self.products = {p.id: p for p in SAMPLE_PRODUCTS}
    
    async def get_collaborative_recommendations(self, user_id: int, limit: int) -> List[Product]:
        """Simulate collaborative filtering recommendations"""
        await asyncio.sleep(0.1)  # Simulate AI processing time
        
        # Simple collaborative filtering simulation
        # In production, this would use actual ML algorithms
        featured_products = [p for p in SAMPLE_PRODUCTS if p.is_featured]
        random.shuffle(featured_products)
        return featured_products[:limit]
    
    async def get_content_based_recommendations(self, product_id: int, limit: int) -> List[Product]:
        """Simulate content-based recommendations"""
        await asyncio.sleep(0.1)
        
        if product_id not in self.products:
            return []
        
        target_product = self.products[product_id]
        # Find products in same category
        similar_products = [
            p for p in SAMPLE_PRODUCTS 
            if p.category_id == target_product.category_id and p.id != product_id
        ]
        
        random.shuffle(similar_products)
        return similar_products[:limit]
    
    async def get_category_recommendations(self, category_id: int, limit: int) -> List[Product]:
        """Get popular products from a category"""
        await asyncio.sleep(0.1)
        
        category_products = [p for p in SAMPLE_PRODUCTS if p.category_id == category_id]
        
        # Sort by featured first, then by price
        category_products.sort(key=lambda x: (not x.is_featured, x.price))
        return category_products[:limit]
    
    async def get_popular_recommendations(self, limit: int) -> List[Product]:
        """Get popular/trending products"""
        await asyncio.sleep(0.1)
        
        # Return featured products and some random ones
        featured = [p for p in SAMPLE_PRODUCTS if p.is_featured]
        others = [p for p in SAMPLE_PRODUCTS if not p.is_featured]
        random.shuffle(others)
        
        result = featured + others
        return result[:limit]

# Initialize recommendation engine
rec_engine = RecommendationEngine()

# API Routes
@app.get("/")
async def root():
    return {
        "service": "AI E-commerce Recommendation Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "recommendations": "/recommendations",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-recommendation-service",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Generate AI-powered product recommendations
    """
    try:
        recommendations = []
        strategy = "hybrid"
        confidence = 0.85
        
        if request.user_id:
            # Collaborative filtering for registered users
            collab_recs = await rec_engine.get_collaborative_recommendations(
                request.user_id, request.limit
            )
            recommendations.extend(collab_recs)
            strategy = "collaborative"
            confidence = 0.90
        
        if request.product_id and len(recommendations) < request.limit:
            # Content-based recommendations
            content_recs = await rec_engine.get_content_based_recommendations(
                request.product_id, request.limit - len(recommendations)
            )
            recommendations.extend(content_recs)
            strategy = "content_based" if not recommendations else "hybrid"
            confidence = 0.80
        
        if request.category_id and len(recommendations) < request.limit:
            # Category-based recommendations
            category_recs = await rec_engine.get_category_recommendations(
                request.category_id, request.limit - len(recommendations)
            )
            recommendations.extend(category_recs)
            strategy = "category_based" if not recommendations else "hybrid"
            confidence = 0.75
        
        # Fill with popular products if needed
        if len(recommendations) < request.limit:
            popular_recs = await rec_engine.get_popular_recommendations(
                request.limit - len(recommendations)
            )
            recommendations.extend(popular_recs)
            strategy = "popular" if not recommendations else "hybrid"
        
        # Remove duplicates and limit results
        seen = set()
        unique_recommendations = []
        for product in recommendations:
            if product.id not in seen:
                seen.add(product.id)
                unique_recommendations.append(product)
        
        unique_recommendations = unique_recommendations[:request.limit]
        
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=unique_recommendations,
            strategy=strategy,
            confidence_score=confidence,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")

@app.get("/products")
async def get_products():
    """Get all available products"""
    return {"products": SAMPLE_PRODUCTS}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get specific product details"""
    if product_id in rec_engine.products:
        return {"product": rec_engine.products[product_id]}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/track-interaction")
async def track_user_interaction(
    user_id: int,
    product_id: int,
    interaction_type: str,
    session_id: Optional[str] = None
):
    """Track user interactions for improving recommendations"""
    # In production, this would store data in database
    return {
        "message": "Interaction tracked successfully",
        "user_id": user_id,
        "product_id": product_id,
        "interaction_type": interaction_type,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/analytics/popular-products")
async def get_popular_products():
    """Get analytics on popular products"""
    featured_products = [p for p in SAMPLE_PRODUCTS if p.is_featured]
    return {
        "popular_products": featured_products,
        "total_products": len(SAMPLE_PRODUCTS),
        "featured_count": len(featured_products)
    }

# GenAI Personalization Endpoints

@app.post("/genai/customer-interaction")
async def process_customer_interaction(
    user_id: int,
    message: str,
    interaction_type: str = "chat",
    channel: str = "web",
    demographics: Optional[dict] = None
):
    """
    Process customer interaction using advanced GenAI services
    """
    try:
        from genai_services import AdvancedPersonalizationOrchestrator
        
        # Initialize GenAI orchestrator
        orchestrator = AdvancedPersonalizationOrchestrator()
        
        # Prepare interaction data
        interaction_data = {
            'message': message,
            'type': interaction_type,
            'channel': channel,
            'demographics': demographics or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Process interaction with all AI services
        result = await orchestrator.process_customer_interaction(user_id, interaction_data)
        
        return {
            "status": "success",
            "ai_analysis": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GenAI processing failed: {str(e)}")

@app.post("/genai/personalized-recommendations")
async def get_personalized_recommendations(
    user_id: int,
    context: str = "general",
    limit: int = 10,
    include_reasoning: bool = True
):
    """
    Get AI-powered personalized product recommendations
    """
    try:
        from genai_services import AdvancedPersonalizationOrchestrator
        
        orchestrator = AdvancedPersonalizationOrchestrator()
        
        # Check if customer profile exists
        if user_id in orchestrator.personalization_engine.customer_profiles:
            profile = orchestrator.personalization_engine.customer_profiles[user_id]
            
            # Get top preferences
            top_categories = sorted(
                profile.preferences.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Generate recommendations based on preferences
            recommendations = []
            for category, score in top_categories:
                category_products = [p for p in SAMPLE_PRODUCTS if p.id <= 5]  # Sample logic
                for product in category_products[:limit//3]:
                    recommendations.append({
                        "product_id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "confidence_score": round(score * 0.9, 2),
                        "reasoning": f"Based on your {category} preference score of {score:.2f}" if include_reasoning else None,
                        "personalization_type": "preference_based"
                    })
            
            return {
                "user_id": user_id,
                "recommendations": recommendations[:limit],
                "customer_insights": {
                    "lifecycle_stage": profile.lifecycle_stage,
                    "predicted_ltv": profile.predicted_ltv,
                    "churn_risk": profile.churn_risk
                },
                "generated_at": datetime.now().isoformat()
            }
        else:
            # Return popular products for new users
            popular_products = [p for p in SAMPLE_PRODUCTS if p.is_featured][:limit]
            return {
                "user_id": user_id,
                "recommendations": [{
                    "product_id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "confidence_score": 0.7,
                    "reasoning": "Popular product for new customers" if include_reasoning else None,
                    "personalization_type": "popularity_based"
                } for p in popular_products],
                "customer_insights": {
                    "lifecycle_stage": "new",
                    "predicted_ltv": 100.0,
                    "churn_risk": 0.1
                },
                "generated_at": datetime.now().isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personalized recommendations failed: {str(e)}")

@app.post("/genai/sentiment-analysis")
async def analyze_customer_sentiment(
    text: str,
    user_id: Optional[int] = None
):
    """
    Analyze customer sentiment using NLP
    """
    try:
        from genai_services import NaturalLanguageProcessor
        
        nlp = NaturalLanguageProcessor()
        
        # Analyze sentiment and intent
        sentiment = await nlp.analyze_sentiment(text)
        intent = await nlp.extract_intent(text)
        attributes = await nlp.extract_product_attributes(text)
        
        return {
            "text": text,
            "sentiment_analysis": sentiment,
            "intent_analysis": intent,
            "extracted_attributes": attributes,
            "dominant_sentiment": max(sentiment.items(), key=lambda x: x[1])[0],
            "primary_intent": max(intent.items(), key=lambda x: x[1])[0],
            "analyzed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@app.post("/genai/conversational-ai")
async def conversational_ai_response(
    user_message: str,
    user_id: int,
    context: str = "general"
):
    """
    Generate AI-powered conversational response
    """
    try:
        from genai_services import ConversationalAI, AdvancedPersonalizationOrchestrator
        
        orchestrator = AdvancedPersonalizationOrchestrator()
        conv_ai = ConversationalAI()
        
        # Get or create customer profile
        if user_id not in orchestrator.personalization_engine.customer_profiles:
            profile = await orchestrator.personalization_engine.create_customer_profile(user_id, {})
        else:
            profile = orchestrator.personalization_engine.customer_profiles[user_id]
        
        # Generate AI response
        ai_response = await conv_ai.generate_response(user_message, profile, context)
        
        # Analyze emotions for empathetic response
        emotions = await orchestrator.emotional_ai.analyze_emotional_state(user_message, profile.interaction_history)
        empathetic_response = await orchestrator.emotional_ai.generate_empathetic_response(emotions, context)
        
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "empathetic_response": empathetic_response,
            "emotional_analysis": emotions,
            "customer_context": {
                "lifecycle_stage": profile.lifecycle_stage,
                "interaction_count": len(profile.interaction_history)
            },
            "response_generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversational AI failed: {str(e)}")

@app.get("/genai/customer-profile/{user_id}")
async def get_customer_profile(user_id: int):
    """
    Get comprehensive customer profile with AI insights
    """
    try:
        from genai_services import AdvancedPersonalizationOrchestrator
        
        orchestrator = AdvancedPersonalizationOrchestrator()
        
        if user_id in orchestrator.personalization_engine.customer_profiles:
            profile = orchestrator.personalization_engine.customer_profiles[user_id]
            
            return {
                "customer_id": user_id,
                "profile": {
                    "demographics": profile.demographics,
                    "preferences": profile.preferences,
                    "behavior_patterns": profile.behavior_patterns,
                    "personality_traits": profile.personality_traits,
                    "lifecycle_stage": profile.lifecycle_stage,
                    "predicted_ltv": profile.predicted_ltv,
                    "churn_risk": profile.churn_risk,
                    "interaction_count": len(profile.interaction_history),
                    "last_updated": profile.last_updated.isoformat()
                },
                "ai_insights": {
                    "top_preferences": dict(sorted(profile.preferences.items(), key=lambda x: x[1], reverse=True)[:5]),
                    "risk_level": "high" if profile.churn_risk > 0.7 else "medium" if profile.churn_risk > 0.4 else "low",
                    "value_segment": "high" if profile.predicted_ltv > 500 else "medium" if profile.predicted_ltv > 200 else "standard"
                }
            }
        else:
            raise HTTPException(status_code=404, detail="Customer profile not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile retrieval failed: {str(e)}")

@app.post("/genai/dynamic-pricing")
async def get_dynamic_pricing(
    product_id: int,
    user_id: int,
    context: str = "standard"
):
    """
    Get AI-driven dynamic pricing based on customer profile
    """
    try:
        from genai_services import AdvancedPersonalizationOrchestrator
        
        orchestrator = AdvancedPersonalizationOrchestrator()
        
        # Find product
        product = next((p for p in SAMPLE_PRODUCTS if p.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        base_price = product.price
        
        # Get customer profile for personalization
        if user_id in orchestrator.personalization_engine.customer_profiles:
            profile = orchestrator.personalization_engine.customer_profiles[user_id]
            
            # Dynamic pricing logic based on customer profile
            price_multiplier = 1.0
            
            # Churn risk pricing
            if profile.churn_risk > 0.6:
                price_multiplier *= 0.85  # 15% discount for at-risk customers
            
            # High-value customer pricing
            if profile.predicted_ltv > 1000:
                price_multiplier *= 1.05  # Slight premium for high-value customers
            
            # Lifecycle stage pricing
            if profile.lifecycle_stage == "new":
                price_multiplier *= 0.9  # 10% new customer discount
            elif profile.lifecycle_stage == "champion":
                price_multiplier *= 0.95  # 5% loyalty discount
            
            final_price = round(base_price * price_multiplier, 2)
            discount_amount = round(base_price - final_price, 2)
            
            return {
                "product_id": product_id,
                "base_price": base_price,
                "personalized_price": final_price,
                "discount_amount": discount_amount,
                "discount_percentage": round((discount_amount / base_price) * 100, 1) if discount_amount > 0 else 0,
                "pricing_factors": {
                    "churn_risk_adjustment": profile.churn_risk > 0.6,
                    "high_value_customer": profile.predicted_ltv > 1000,
                    "lifecycle_discount": profile.lifecycle_stage in ["new", "champion"]
                },
                "generated_at": datetime.now().isoformat()
            }
        else:
            # Standard pricing for unknown customers
            return {
                "product_id": product_id,
                "base_price": base_price,
                "personalized_price": base_price,
                "discount_amount": 0,
                "discount_percentage": 0,
                "pricing_factors": {
                    "new_customer": True
                },
                "generated_at": datetime.now().isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dynamic pricing failed: {str(e)}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8001))
    host = os.environ.get('HOST', '0.0.0.0')
    uvicorn.run(app, host=host, port=port)
