import os
from datetime import timedelta

# API Configuration
API_TITLE = "IFC Chat API"
API_DESCRIPTION = "API for processing IFC files and answering questions about them"
API_VERSION = "1.0.0"
API_HOST = "0.0.0.0"
API_PORT = 8000

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://ifc-agent-api.onrender.com",
    "https://*.onrender.com"
]
CORS_CREDENTIALS = True
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
CORS_HEADERS = ["*", "Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"]

# AI Configuration
GENAI_API_KEY = "AIzaSyBLuL_Nw20rrNOkKo07gNERvwfXV87Kz0Y"  # Replace with your Gemini API key
MODEL_NAME = "gemini-1.5-pro-latest"  # Use a supported model name
MAX_RETRIES = 3  # Maximum code correction attempts
RETRY_DELAY = 5  # Delay in seconds between retries for quota issues

# File Storage Configuration
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")  # Directory to store uploaded files
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB max file size
FILE_EXPIRY = timedelta(hours=24)  # Files older than this will be deleted

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True) 