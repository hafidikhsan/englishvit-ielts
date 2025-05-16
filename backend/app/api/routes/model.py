# MARK: Import
# Dependencies
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.asr_service import asr_service
from app.services.spacy_service import spacy_service
from app.services.grammar_service import grammar_service
from app.services.lexical_service import lexical_service
from app.services.fluency_service import fluency_service

# Modules
from app.utils.exception import EvServerException, EvClientException, EvAPIException
from app.models.response_model import EvResponseModel

# MARK: Information
@api_bp.route('/model/<type>', methods = ['GET'])
def model(type):
    '''
    Information route for setting the model.
    '''
    # Switch case for different evaluation types
    # MARK: Pronunciation
    if type == 'check':
        # Check the ASR model
        asr_model = asr_service.check_model()
        # Check the Spacy model
        spacy_model = spacy_service.check_model()
        # Check the Grammar model
        grammar_model = grammar_service.check_model()
        # Check the Lexical model
        lexical_model = lexical_service.check_model()
        # Check the Fluency model
        fluency_model = fluency_service.check_model()

        # Return the result
        return jsonify(EvResponseModel(
            code = 200,
            status = 'Success',
            message = 'Model check successful',
            data = {
                'asr': asr_model,
                'spacy': spacy_model,
                'grammar': grammar_model,
                'lexical': lexical_model,
                'fluency': fluency_model,
            }
        ).to_dict()), 200, {'ContentType' : 'application/json'}
    
    # MARK: UpdateASR
    elif type == 'update-asr':
        try:
            # Check if the request has a text `model_name` field
            if 'model_name' not in request.form:
                # Define the error message
                message = 'Invalid request, model_name is required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            model_name = request.form['model_name']

            # Change the ASR model
            asr_service.update_model(model_name = model_name)

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'ASR model updated successfully',
                data = {
                    'model_name': model_name,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in ASR model update',
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
                message = 'Server error in ASR model update',
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
                message = 'API error in ASR model update',
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
                message = 'Internal server error in ASR model update',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: UpdateSpacy
    elif type == 'update-spacy':
        try:
            # Check if the request has a text `model_name` field
            if 'model_name' not in request.form:
                # Define the error message
                message = 'Invalid request, model_name is required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            model_name = request.form['model_name']

            # Change the Spacy model
            spacy_service.update_model(model_name = model_name)

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Spacy model updated successfully',
                data = {
                    'model_name': model_name,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in spacy model update',
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
                message = 'Server error in spacy model update',
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
                message = 'API error in spacy model update',
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
                message = 'Internal server error in spacy model update',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: UpdateFluency
    elif type == 'update-fluency':
        try:
            # Get the model name from the request
            filled_pauses_model = request.form.get('filled_pauses_model', None)
            explicit_editing_terms_model = request.form.get('explicit_editing_terms_model', None)
            discourse_markers_model = request.form.get('discourse_markers_model', None)
            coordinating_conjunctions_model = request.form.get('coordinating_conjunctions_model', None)
            restart_words_model = request.form.get('restart_words_model', None)

            # Change the fluency model
            fluency_service.update_model(
                filled_pauses_model = filled_pauses_model,
                explicit_editing_terms_model = explicit_editing_terms_model,
                discourse_markers_model = discourse_markers_model,
                coordinating_conjunctions_model = coordinating_conjunctions_model,
                restart_words_model = restart_words_model,
            )

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Fluency model updated successfully',
                data = {
                    'filled_pauses_model': filled_pauses_model,
                    'explicit_editing_terms_model': explicit_editing_terms_model,
                    'discourse_markers_model': discourse_markers_model,
                    'coordinating_conjunctions_model': coordinating_conjunctions_model,
                    'restart_words_model': restart_words_model,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in fluency model update',
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
                message = 'Server error in fluency model update',
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
                message = 'API error in fluency model update',
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
                message = 'Internal server error in fluency model update',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: UpdateGrammar
    elif type == 'update-grammar':
        try:
            # Change the grammar model
            grammar_service.update_model()

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Grammar model updated successfully',
                data = {
                    'grammarly_model_name': grammar_service.grammarly_model_name,
                    'happy_base_model_name': grammar_service.happy_base_model_name,
                    'open_source_model_name': grammar_service.open_source_model_name,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in grammar model update',
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
                message = 'Server error in grammar model update',
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
                message = 'API error in grammar model update',
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
                message = 'Internal server error in grammar model update',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: ChangeGrammar
    elif type == 'change-grammar':
        try:
            # Check if the request has a text `model_name` field
            if 'model_name' not in request.form:
                # Define the error message
                message = 'Invalid request, model_name is required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            model_name = request.form['model_name']

            # Change the grammar model
            grammar_service.change_gec_model(model = model_name)

            # Define model name
            current_model_name = ''

            # Define the model name
            if model_name == 'grammarly':
                current_model_name = grammar_service.grammarly_model_name
            elif model_name == 'happy':
                current_model_name = grammar_service.happy_base_model_name
            elif model_name == 'base':
                current_model_name = grammar_service.open_source_model_name

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Grammar model change successfully',
                data = {
                    'model_key': model_name,
                    'model_name': current_model_name,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in grammar model change',
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
                message = 'Server error in grammar model change',
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
                message = 'API error in grammar model change',
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
                message = 'Internal server error in grammar model change',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
        
    # MARK: UpdateLexical
    elif type == 'update-lexical':
        try:
            # Change the lexical model
            lexical_service.update_model()

            # Return the result
            return jsonify(EvResponseModel(
                code = 200,
                status = 'Success',
                message = 'Lexical model updated successfully',
                data = {
                    'cefr_classification_model_name': lexical_service.cefr_classification_model_name,
                    'bert_fill_masked_model_name': lexical_service.bert_fill_masked_model_name,
                },
            ).to_dict()), 200, {'ContentType' : 'application/json'}

        except EvClientException as error:
            # Return the error message
            return jsonify(EvResponseModel(
                code = error.status_code,
                status = 'Error',
                message = 'Invalid request in lexical model update',
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
                message = 'Server error in lexical model update',
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
                message = 'API error in lexical model update',
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
                message = 'Internal server error in lexical model update',
                data = {
                    'error': {
                        'message': str(error),
                    },
                },
            ).to_dict()), 500, {'ContentType' : 'application/json'}
    