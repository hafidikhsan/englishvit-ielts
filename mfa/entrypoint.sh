#!/bin/bash
set -e

# Download required models if not already downloaded
mfa model download acoustic english_mfa || true
mfa model download dictionary english_us_arpa || true

# Start Flask server
python3 /app.py
