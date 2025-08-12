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

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8001))
    host = os.environ.get('HOST', '0.0.0.0')
    uvicorn.run(app, host=host, port=port)
