from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from config import (
    API_TITLE, API_DESCRIPTION, API_VERSION, API_HOST, API_PORT,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS
)
from routes import upload_routes, query_routes, health_routes
from utils.error_handling import AppException, handle_app_exception, handle_http_exception, handle_generic_exception

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Configure CORS - This must be the first middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
    expose_headers=["*"],
    max_age=3600,
)

# Add custom middleware to ensure CORS headers are set for all responses
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle preflight requests
    if request.method == "OPTIONS":
        response = JSONResponse(content={"message": "OK"})
    else:
        response = await call_next(request)
    
    # Get the origin from the request
    origin = request.headers.get("origin")
    
    # If the origin is in our allowed origins, set it in the response
    if origin and (origin in CORS_ORIGINS or any(origin.startswith(origin_pattern.replace("*", "")) for origin_pattern in CORS_ORIGINS if "*" in origin_pattern)):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = ", ".join(CORS_METHODS)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(CORS_HEADERS)
        response.headers["Access-Control-Max-Age"] = "3600"
    
    return response

# Include routers
app.include_router(upload_routes.router)
app.include_router(query_routes.router)
app.include_router(health_routes.router)

# Get the path to the frontend build directory
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "build")

# Check if the build directory exists
if os.path.exists(frontend_path):
    # Mount the entire build directory
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
    
    # Serve index.html on root path
    @app.get("/")
    async def serve_root():
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    # If build directory doesn't exist, just serve the API
    @app.get("/")
    async def root():
        """Root endpoint to check if the API is running"""
        return {"status": "ok", "message": "IFC Chat API is running"}

# API health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "ok", "message": "IFC Chat API is running"}

# Exception handlers
app.add_exception_handler(AppException, handle_app_exception)
app.add_exception_handler(Exception, handle_generic_exception)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=API_HOST, port=API_PORT)