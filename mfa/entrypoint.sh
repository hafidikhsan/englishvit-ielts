#!/bin/bash
set -e

# Download models if not present
if [ ! -f /root/.local/share/montreal-forced-aligner/pretrained_models/english_mfa.zip ]; then
    echo "Downloading acoustic model..."
    mfa model download acoustic english_mfa
fi

if [ ! -f /root/.local/share/montreal-forced-aligner/pretrained_models/english_us_arpa.zip ]; then
    echo "Downloading dictionary..."
    mfa model download dictionary english_us_arpa
fi

# You can run alignment directly here, or wait for a trigger from backend
# For now, just keep container alive for exec commands
tail -f /dev/null
