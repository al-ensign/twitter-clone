#!/bin/bash

echo "Starting FastAPI microservice"

uvicorn main:app --host 0.0.0.0 --port 8001

echo "FastAPI is working"
