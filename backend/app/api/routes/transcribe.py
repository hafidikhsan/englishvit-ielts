# Import dependencies
import os
from flask import jsonify, request

# Import routes
from app.api.routes import api_bp

# Import services
from app.services.asr_service import asr_service
from app.services.fluency_service import fluency_service
from app.services.grammar_service import grammar_service
from app.services.lexical_service import lexical_service

# Import modules
from app.utils.exception import EvException

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

    # Get the file name
    file_name = audio_file.filename

    # Save the file
    audio_file_path = os.path.join('/app/audio', file_name)

    # Save the file
    audio_file.save(audio_file_path)

    # Process the audio
    (transcribe, words) = asr_service.process_audio(audio_file_path)

    # Remove the file
    os.remove(audio_file_path)

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
    }

    return jsonify({
        'status' : 'success',
        'result' : result,
    }), 200, {'ContentType' : 'application/json'}