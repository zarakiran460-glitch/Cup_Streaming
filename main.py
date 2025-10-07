from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   The app will run but database features won't work")
    yield
    # Shutdown
    pass

# Create FastAPI app with enhanced OpenAPI documentation
app = FastAPI(
    title="Cup Streaming API",
    description="""
    ## 🚀 **Cup Streaming Platform API**
    
    A modern, high-performance video streaming platform built with FastAPI.
    
    ### **Features:**
    - 🔐 **Authentication**: JWT-based user authentication
    - 👥 **User Management**: User registration, profiles, and permissions
    - 📹 **Video Management**: Upload, stream, and manage videos
    - ❤️ **Social Features**: Like/unlike videos, view tracking
    - 📊 **Analytics**: Video views and engagement metrics
    - ☁️ **Cloud Storage**: AWS S3 integration
    
    ### **Getting Started:**
    1. **Register** a new user at `/api/v1/auth/register`
    2. **Login** to get your JWT token at `/api/v1/auth/login`
    3. **Use the token** in the Authorization header: `Bearer <your-token>`
    
    ### **API Endpoints:**
    - **Authentication**: `/api/v1/auth/*`
    - **Users**: `/api/v1/users/*`
    - **Videos**: `/api/v1/videos/*`
    
    ---
    *Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL*
    """,
    version="1.0.0",
    contact={
        "name": "Cup Streaming Team",
        "email": "support@cupstreaming.com",
        "url": "https://cupstreaming.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.cupstreaming.com", "description": "Production server"}
    ],
    tags_metadata=[
        {
            "name": "authentication",
            "description": "User authentication operations. Register, login, and manage user sessions.",
            "externalDocs": {
                "description": "JWT Authentication Guide",
                "url": "https://fastapi.tiangolo.com/tutorial/security/",
            },
        },
        {
            "name": "users",
            "description": "User management operations. Create, read, update, and delete user accounts.",
        },
        {
            "name": "videos",
            "description": "Video management operations. Upload, stream, and manage video content.",
        },
    ],
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Customize OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )
    
    # Add custom security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {
        "message": "Welcome to Cup Streaming API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "custom_swagger": "/static/swagger-ui.html",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "authentication": "/api/v1/auth",
            "users": "/api/v1/users",
            "videos": "/api/v1/videos"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/docs/custom")
async def custom_swagger_ui():
    """Custom Swagger UI endpoint"""
    return {"message": "Custom Swagger UI available at /static/swagger-ui.html"}

@app.get("/api-info")
async def api_info():
    """Get detailed API information"""
    return {
        "name": "Cup Streaming API",
        "version": "1.0.0",
        "description": "A modern, high-performance video streaming platform",
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "authentication": "JWT",
        "features": [
            "User Authentication & Management",
            "Video Upload & Streaming",
            "Social Features (Likes, Views)",
            "Analytics & Metrics",
            "AWS S3 Integration"
        ],
        "endpoints": {
            "total": 15,
            "authentication": 3,
            "users": 4,
            "videos": 8
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
