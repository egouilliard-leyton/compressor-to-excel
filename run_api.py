#!/usr/bin/env python3
"""
Simple script to run the FastAPI application.

Usage:
    python run_api.py

Or with custom host/port:
    python run_api.py --host 0.0.0.0 --port 8001
"""
import uvicorn
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Compressor to Excel API")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port to bind to (default: 8001)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

