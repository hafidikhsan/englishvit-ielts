# Import dependencies
import os
from flask import jsonify, request
import requests
from textgrid import TextGrid
import subprocess
import datetime

# Import routes
from app.api.routes import api_bp

# Import services
from app.services.asr_service import asr_service
from app.services.fluency_service import fluency_service
from app.services.grammar_service import grammar_service
from app.services.lexical_service import lexical_service

# Import modules
from app.utils.exception import EvException

@api_bp.route('/mfatest', methods = ['POST'])
def mfatest():
    response = requests.get("http://mfa:5000/")
    return jsonify({
        'status' : 'success',
        'result' : response.json(),
    }), 200, {'ContentType' : 'application/json'}

@api_bp.route('/mfa', methods = ['GET'])
def mfa():
    response = requests.get("http://mfa:5000/mfa")

@api_bp.route('/download-mfa', methods = ['GET'])
def download_mfa():
    response = requests.get("http://mfa:5000/download-mfa")
    return jsonify({
        'status' : 'success',
        'result' : response.json(),
    }), 200, {'ContentType' : 'application/json'}

@api_bp.route('/download-arpa', methods = ['GET'])
def download_arpa():
    response = requests.get("http://mfa:5000/download-arpa")
    return jsonify({
        'status' : 'success',
        'result' : response.json(),
    }), 200, {'ContentType' : 'application/json'}

@api_bp.route('/align', methods = ['GET'])
def align():
    response = requests.get("http://mfa:5000/align")
    return jsonify({
        'status' : 'success',
        'result' : response.json(),
    }), 200, {'ContentType' : 'application/json'}

# MARK: Transcribe
@api_bp.route('/transcribe', methods = ['POST'])
def transcribe():
    if not request.files or 'file' not in request.files:
        raise EvException(
            message = 'Invalid request, audio is required',
            status_code = 400,
            information = {
                'message': 'Invalid request, audio is required',
            }
        )
    
    # Get the audio file
    audio_file = request.files['file']

    # get the date time
    now = datetime.datetime.now().strftime("%Y-%m-%d:%H-%M-%S")

    # Define directory
    directory = f'/app/audio/{now}'

    # Create new directorty using time stamp
    os.makedirs(directory)

    # Save the file
    audio_file_path = os.path.join(directory, now)

    # Save the file
    audio_file.save(audio_file_path + '.wav')

    # Process the audio
    (transcribe, words) = asr_service.process_audio(audio_file_path + '.wav')

    # Wite transcribe text to file
    with open(os.path.join(directory, f'{now}.txt'), 'w') as f:
        f.write(transcribe)

    response = requests.post(
        "http://mfa:5000/align",
        json={
            "input_path": directory,
            "output_path": directory,
            "dictionary": "english_us_arpa",
            "acoustic_model": "english_mfa"
        }
    )

    tg = TextGrid.fromFile(os.path.join(directory, now) + ".TextGrid")
    phones_tier = next(t for t in tg.tiers if 'phone' in t.name.lower())
    words_tier = next(t for t in tg.tiers if 'word' in t.name.lower())

    word_level_feedback = []
    ARPABET_TO_READABLE = {
        'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ',
        'AW': 'aʊ', 'AY': 'aɪ', 'B': 'b', 'CH': 'tʃ',
        'D': 'd', 'DH': 'ð', 'EH': 'ɛ', 'ER': 'ɝ',
        'EY': 'eɪ', 'F': 'f', 'G': 'ɡ', 'HH': 'h',
        'IH': 'ɪ', 'IY': 'i', 'JH': 'dʒ', 'K': 'k',
        'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ',
        'OW': 'oʊ', 'OY': 'ɔɪ', 'P': 'p', 'R': 'ɹ',
        'S': 's', 'SH': 'ʃ', 'T': 't', 'TH': 'θ',
        'UH': 'ʊ', 'UW': 'u', 'V': 'v', 'W': 'w',
        'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'
    }
    

    for word_interval in words_tier.intervals:
        word = word_interval.mark.strip()
        if word == "" or word.lower() in ["<unk>", "sil", "sp"]:
            continue

        word_data = {
            "word": word,
            "start": round(word_interval.minTime, 2),
            "end": round(word_interval.maxTime, 2),
            "phonemes": []
        }

        for ph in phones_tier.intervals:
            if ph.minTime >= word_interval.minTime and ph.maxTime <= word_interval.maxTime:
                ph_mark = ph.mark.strip()
                if ph_mark == "" or ph_mark.lower() in ["sil", "sp"]:
                    continue
                duration = ph.maxTime - ph.minTime
                status = 0 if duration < 0.06 else 1
                base = ''.join(filter(str.isalpha, ph_mark))
                word_data["phonemes"].append({
                    "phoneme": ARPABET_TO_READABLE.get(base.upper(), base.lower()),
                    "start": round(ph.minTime, 2),
                    "end": round(ph.maxTime, 2),
                    "status": status
                })

        word_level_feedback.append(word_data)

    # Remove the directory
    os.rmdir(directory)

    fluency_band, fluency_feedback = fluency_service.score(transcribe, words)
    grammar_band, grammar_feedback = grammar_service.score(transcribe)
    lexical_band, lexical_feedback = lexical_service.score(transcribe)

    result = {
        'transcribe': transcribe,
        'fluency': {
            'band': fluency_band,
            'feedback': fluency_feedback,
        },
        'grammar': {
            'band': grammar_band,
            'feedback': grammar_feedback,
        },
        'lexical': {
            'band': lexical_band,
            'feedback': lexical_feedback,
        },
        'word_level_feedback': word_level_feedback,
    }

    return jsonify({
        'status' : 'success',
        'result' : result,
    }), 200, {'ContentType' : 'application/json'}