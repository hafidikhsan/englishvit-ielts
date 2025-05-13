# MARK: Import
# Dependencies
import os
import json
import shutil
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.pronunciation_service import pronunciation_service
from app.services.grammar_service import grammar_service
from app.services.lexical_service import lexical_service
from app.services.fluency_service import fluency_service

# Modules
from app.utils.exception import EvException
from app.models.response import EvResponseModel

# MARK: Evaluation
@api_bp.route('/evaluation/<type>', methods = ['POST'])
def evaluation(type):
    '''
    Function to handle the evaluation process based on the type of evaluation requested.
    '''
    # MARK: Pronunciation
    # Switch case for different evaluation types
    if type == 'pronunciation':
        # A flag to check if the corpus is already saved
        corpus_folder_path = None
        
        try:
            # Check if the request has files and if the file is present
            if not request.files or 'file' not in request.files:
                # Define the error message
                message = 'Invalid request, audio file is required'

                # Throw an exception
                raise EvException(
                    message = message,
                    status_code = 500,
                    information = {
                        'message': message,
                    }
                )
            
            # Check if the request has a text `transcribe` and `words` field
            if 'transcribe' not in request.form or 'words' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and words are required'

                # Throw an exception
                raise EvException(
                    message = message,
                    status_code = 500,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the audio file from the request
            audio_file = request.files['file']

            # Get the transcribe
            transcribe = request.form.get('transcribe')
            
            # Get the words
            words = request.form.get('words')

            # Declare words timestamps
            words_timestamps = []
            
            # Check if words is not empty
            if words:
                # Load the words timestamps from JSON
                words_timestamps = json.loads(words)

            # Get the file name and extension
            file_name, file_extension = os.path.splitext(audio_file.filename)

            # Define main directory
            main_directory = '/app/audio'

            # Change corpus folder path
            corpus_folder_path = os.path.join(main_directory, file_name)

            # Create new directory if it doesn't exist
            os.makedirs(corpus_folder_path)

            # Get the audio file path
            audio_file_path = os.path.join(corpus_folder_path, file_name + file_extension)

            # Save the audio file to the server
            audio_file.save(audio_file_path)

            # Write transcribe text to file
            with open(os.path.join(corpus_folder_path, f'{file_name}.txt'), 'w') as f:
                f.write(transcribe)

            # Evaluate the pronunciation
            evaluation = pronunciation_service.evaluate_pronunciation(
                corpus_path = corpus_folder_path,
                transcribe = transcribe,
                words_timestamps = words_timestamps,
            )

            # Delete the folder
            shutil.rmtree(corpus_folder_path)

            # Send the result to backend

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Pronunciation evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}
        
        except EvException as error:
            # Check if the corpus folder is saved and delete it
            if corpus_folder_path:
                shutil.rmtree(corpus_folder_path)

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except Exception as error:
            # Check if the corpus folder is saved and delete it
            if corpus_folder_path:
                shutil.rmtree(corpus_folder_path)

            # Return the error message
            return jsonify(EvResponseModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: Grammar
    elif type == 'grammar':
        try:
            # Check if the request has a text `transcribe` field
            if 'transcribe' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe are required'

                # Throw an exception
                raise EvException(
                    message = message,
                    status_code = 500,
                    information = {
                        'message': message,
                    }
                )
            
            # Evaluate the grammar
            evaluation = grammar_service.evaluate_grammar(
                transcribe = request.form.get('transcribe'),
            )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Grammar evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except Exception as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
    # MARK: Lexical
    elif type == 'lexical':
        try:
            # Check if the request has a text `transcribe` field
            if 'transcribe' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe are required'

                # Throw an exception
                raise EvException(
                    message = message,
                    status_code = 500,
                    information = {
                        'message': message,
                    }
                )
            
            # Evaluate the grammar
            evaluation = lexical_service.evaluate_lexical(
                transcribe = request.form.get('transcribe'),
            )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Lexical evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except Exception as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
    # MARK: Fluency
    elif type == 'fluency':
        try:
            # Check if the request has a text `transcribe` and `words` field
            if 'transcribe' not in request.form or 'words' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and words are required'

                # Throw an exception
                raise EvException(
                    message = message,
                    status_code = 500,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the words
            words = request.form.get('words')

            # Declare words timestamps
            words_timestamps = []
            
            # Check if words is not empty
            if words:
                # Load the words timestamps from JSON
                words_timestamps = json.loads(words)
            
            # Evaluate the grammar
            evaluation = fluency_service.evaluate_fluency(
                transcribe = request.form.get('transcribe'),
                words = words_timestamps,
            )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Fluency evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except Exception as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
    else:
        # MARK: InvalidType
        # Return the error message
        return jsonify(EvResponseModel(
            code = 500,
            status = 'Error',
            message = 'Invalid evaluation type',
            data = {
                'error': {
                    'message': 'Invalid evaluation type',
                },
            },
        ).to_dict()), 500, {'ContentType' : 'application/json'}