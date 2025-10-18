import logging
from datetime import datetime, timezone
from typing import Dict, Any
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Profile API",
    description="Profile endpoint with Cat Facts integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class UserInfo(BaseModel):
    email: EmailStr
    name: str
    stack: str

class ProfileResponse(BaseModel):
    status: str
    user: UserInfo
    timestamp: str
    fact: str

# Configuration
CAT_FACTS_API_URL = "https://catfact.ninja/fact"
API_TIMEOUT = 5.0  # seconds
FALLBACK_FACT = "Cats are amazing creatures!"

# User configuration from environment variables
USER_EMAIL = os.getenv("USER_EMAIL", "your.email@example.com")
USER_NAME = os.getenv("USER_NAME", "Your Name")
USER_STACK = os.getenv("USER_STACK", "Python/FastAPI")

async def fetch_cat_fact() -> str:
    """
    Fetch a random cat fact from the Cat Facts API.
    
    Returns:
        str: A cat fact or fallback message if API fails
    """
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            logger.info(f"Fetching cat fact from {CAT_FACTS_API_URL}")
            response = await client.get(CAT_FACTS_API_URL)
            response.raise_for_status()
            data = response.json()
            fact = data.get("fact", FALLBACK_FACT)
            logger.info("Successfully fetched cat fact")
            return fact
    except httpx.TimeoutException:
        logger.error("Timeout while fetching cat fact")
        return FALLBACK_FACT
    except httpx.RequestError as e:
        logger.error(f"Network error while fetching cat fact: {e}")
        return FALLBACK_FACT
    except Exception as e:
        logger.error(f"Unexpected error while fetching cat fact: {e}")
        return FALLBACK_FACT

@app.get("/me", response_model=ProfileResponse, responses={
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "user": {
                        "email": "user@example.com",
                        "name": "John Doe",
                        "stack": "Python/FastAPI"
                    },
                    "timestamp": "2025-10-18T12:34:56.789Z",
                    "fact": "Cats have over 20 vocalizations."
                }
            }
        }
    }
})
async def get_profile() -> JSONResponse:
    """
    Get user profile information with a random cat fact.
    
    Returns:
        JSONResponse: User profile with current timestamp and cat fact
    """
    try:
        # Get current UTC timestamp in ISO 8601 format
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        # Fetch cat fact
        cat_fact = await fetch_cat_fact()
        
        # Construct response
        response_data = {
            "status": "success",
            "user": {
                "email": USER_EMAIL,
                "name": USER_NAME,
                "stack": USER_STACK
            },
            "timestamp": timestamp,
            "fact": cat_fact
        }
        
        logger.info(f"Successfully generated profile response at {timestamp}")
        
        return JSONResponse(
            content=response_data,
            status_code=200,
            media_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error generating profile response: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information
    """
    return {
        "message": "Profile API",
        "endpoints": {
            "/me": "GET - Fetch user profile with cat fact"
        }
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}

