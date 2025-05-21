# MARK: Import
# Dependencies
import os
import requests
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
from app.services.overall_feedback_service import overall_feedback_service

# Modules
from app.utils.exception import EvServerException, EvClientException, EvAPIException
from app.models.response_model import EvResponseModel

# MARK: Evaluation
@api_bp.route('/evaluation/<type>', methods = ['POST'])
def evaluation(type):
    '''
    Function to handle the evaluation process based on the type of evaluation requested.
    '''
    # Switch case for different evaluation types
    # MARK: Pronunciation
    if type == 'pronunciation_simple':
        try:
            # Check if the request has a text `words`, `transcribe`, and `test_id` field
            if 'words' not in request.form or 'test_id' not in request.form or 'transcribe' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and words are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            # Get the words
            words = request.form.get('words')
            transcribe = request.form.get('transcribe')

            # Declare words timestamps
            words_timestamps = []
            
            # Check if words is not empty
            if words:
                # Load the words timestamps from JSON
                words_timestamps = json.loads(words)

            # Evaluate the pronunciation
            evaluation = pronunciation_service.evaluate_pronunciation_new(
                words_timestamps = words_timestamps,
                transcribe = transcribe,
            )

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'pronunciation_feedback': json.dumps(evaluation.to_dict()),
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Pronunciation evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}
        
        except EvClientException as error:

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in pronunciation evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in pronunciation evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in pronunciation evaluation',
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
                message = 'Internal server error in pronunciation evaluation',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
    
    elif type == 'pronunciation':
        # A flag to check if the corpus is already saved
        corpus_folder_path = None
        
        try:
            # Check if the request has files and if the file is present
            if not request.files or 'file' not in request.files:
                # Define the error message
                message = 'Invalid request, audio file is required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Check if the request has a text `transcribe`, `words`, and `test_id` field
            if 'transcribe' not in request.form or 'words' not in request.form or 'test_id' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and words are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
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

            # Prepare local temp folder for processing
            tmp_corpus_folder_path = os.path.join('/app/tmp_audio', file_name)

            # Clean tmp folder if exists
            if os.path.exists(tmp_corpus_folder_path):
                shutil.rmtree(tmp_corpus_folder_path)

            # Copy corpus folder (audio + transcript) to tmp folder
            shutil.copytree(corpus_folder_path, tmp_corpus_folder_path)

            # Evaluate the pronunciation
            evaluation = pronunciation_service.evaluate_pronunciation(
                corpus_path = tmp_corpus_folder_path,
                transcribe = transcribe,
                words_timestamps = words_timestamps,
            )

            # Copy generated TextGrid(s) or output files back to original folder
            # Assuming your evaluation produces TextGrid file(s) inside tmp_corpus_folder_path
            for file in os.listdir(tmp_corpus_folder_path):
                if file.endswith('.TextGrid'):
                    shutil.copy(
                        os.path.join(tmp_corpus_folder_path, file),
                        corpus_folder_path
                    )

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'pronunciation_feedback': json.dumps(evaluation.to_dict()),
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Delete the folder
            shutil.rmtree(corpus_folder_path)
            shutil.rmtree(tmp_corpus_folder_path)

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Pronunciation evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}
        
        except EvClientException as error:
            # Check if the corpus folder is saved and delete it
            if corpus_folder_path:
                shutil.rmtree(corpus_folder_path)

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in pronunciation evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:
            # Check if the corpus folder is saved and delete it
            if corpus_folder_path:
                shutil.rmtree(corpus_folder_path)

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in pronunciation evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:
            # Check if the corpus folder is saved and delete it
            if corpus_folder_path:
                shutil.rmtree(corpus_folder_path)

            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in pronunciation evaluation',
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
                message = 'Internal server error in pronunciation evaluation',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: Grammar
    elif type == 'grammar':
        try:
            # Check if the request has a text `transcribe` and `test_id` field
            if 'transcribe' not in request.form or 'test_id' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and test_id are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Evaluate the grammar
            evaluation = grammar_service.evaluate_grammar(
                transcribe = request.form.get('transcribe'),
            )

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'grammar_feedback': json.dumps(evaluation.to_dict()),
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Grammar evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in grammar evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in grammar evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in grammar evaluation',
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
                message = 'Internal server error in grammar evaluation',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: Lexical
    elif type == 'lexical':
        try:
            # Check if the request has a text `transcribe` and `test_id` field
            if 'transcribe' not in request.form or 'test_id' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe and test_id are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Evaluate the grammar
            evaluation = lexical_service.evaluate_lexical(
                transcribe = request.form.get('transcribe'),
            )

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'lexical_feedback': json.dumps(evaluation.to_dict()),
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Lexical evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in lexical evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in lexical evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in lexical evaluation',
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
                message = 'Internal server error in lexical evaluation',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: Fluency
    elif type == 'fluency':
        try:
            # Check if the request has a text `transcribe`, `test_id`, and `words` field
            if 'transcribe' not in request.form or 'test_id' not in request.form or 'words' not in request.form:
                # Define the error message
                message = 'Invalid request, transcribe, test_id, and words are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
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

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'fluency_feedback': json.dumps(evaluation.to_dict()),
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Fluency evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in fluency evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in fluency evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in fluency evaluation',
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
                message = 'Internal server error in fluency evaluation',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: Overall
    elif type == 'overall':
        try:
            # Check if the request has a text `session_id`, `finished`, `fluency`, `lexical`, `grammar`, and `pronunciation` field
            if 'session_id' not in request.form or 'finished' not in request.form or 'fluency' not in request.form or 'lexical' not in request.form or 'grammar' not in request.form or 'pronunciation' not in request.form:
                # Define the error message
                message = 'Invalid request session_id, finished, fluency, lexical, grammar, and pronunciation are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the list of fluency, lexical, grammar, and pronunciation evaluations
            fluency = json.loads(request.form.get('fluency'))
            lexical = json.loads(request.form.get('lexical'))
            grammar = json.loads(request.form.get('grammar'))
            pronunciation = json.loads(request.form.get('pronunciation'))
            
            # Evaluate the overall feedback
            evaluation = overall_feedback_service.evaluate_overall_feedback(
                fluency = fluency,
                lexical = lexical,
                grammar = grammar,
                pronunciation = pronunciation,
            )

            # Send the result to backend
            if (request.headers.get('Authorization', '') != ''):
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'finished': request.form.get('finished'),
                    'overall_band': evaluation.overall_band,
                    'overall_feedback': evaluation.overall_feedback,
                    'fluency_band': evaluation.fluency_band,
                    'fluency_feedback': evaluation.fluency_feedback,
                    'lexical_band': evaluation.lexical_band,
                    'lexical_feedback': evaluation.lexical_feedback,
                    'grammar_band': evaluation.grammar_band,
                    'grammar_feedback': evaluation.grammar_feedback,
                    'pronunciation_band': evaluation.pronunciation_band,
                    'pronunciation_feedback': evaluation.pronunciation_feedback,
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/session/update/{request.form['session_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the data to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

            # Return the evaluation result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Overall evaluation completed successfully',
                data = evaluation.to_dict(),
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in overall evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvServerException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Server error in overall evaluation',
                data = {
                    'error': {
                        'message': error.message,
                        'information': error.information,
                    },
                },
            ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
        
        except EvAPIException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'API error in overall evaluation',
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
                message = 'Internal server error in overall evaluation',
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
            code = 400,
            status = 'Error',
            message = 'Invalid evaluation type',
            data = {
                'error': {
                    'message': 'Invalid evaluation type',
                },
            },
        ).to_dict()), 400, {'ContentType' : 'application/json'}