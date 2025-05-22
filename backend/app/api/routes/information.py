# MARK: Import
# Dependencies
import os
import json
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Modules
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel
from app.utils.exception import EvClientException, EvServerException, EvException
from app.utils.logger import ev_logger

# Get the directory
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ))
os.makedirs(JSON_DIR, exist_ok=True)

# MARK: Information
@api_bp.route('/information/<type>', methods=['GET', 'POST'])
def information(type: str):
    '''
    Information route to handle the information requests. to get the information data
    about the IELTS feature.
    '''
    try:
        ev_logger.info(JSON_DIR)
        # If the information type is test
        if type == 'test':
            # Define the filename
            file_path = os.path.join(JSON_DIR, "information_test.json")
            ev_logger.info(file_path)
            ev_logger.info(os.path.exists(file_path))

            # If GET request, return the information
            if request.method == 'GET':
                # Check if the file exists
                if os.path.exists(file_path):
                    # Open the file and return the data
                    with open(file_path, 'r') as f:
                        # Load the data from the file
                        data_list = json.load(f)

                        # Define the response model data
                        response_data = EvResponseModel(
                            metadata = EvResponseMetadataModel(
                                code = 200,
                                status = 'Success',
                                message = 'Information retrieved successfully',
                            ),
                            data = {
                                'information': data_list,
                            }
                        )
                        # Return the information response
                        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                    
                raise EvServerException(
                    message = "File not found",
                )

            # If POST request, update the information
            elif request.method == 'POST':
                try:
                    # Check if have the request json data
                    if not request.is_json:
                        # Define the error message
                        message = 'Invalid request json data are required'

                        # Throw an exception
                        raise EvClientException(
                            message = message,
                            information = {
                                'message': message,
                            }
                        )
                    
                    # Get the json data from the request
                    new_data = request.get_json(force=True)

                    # Write the new data to the file
                    with open(file_path, 'w') as f:
                        # Dump the data to the file
                        json.dump(
                            new_data, 
                            f, 
                            indent = 4,
                        )

                    # Define the response model data
                    response_data = EvResponseModel(
                        metadata = EvResponseMetadataModel(
                            code = 200,
                            status = 'Success',
                            message = 'Information updated successfully',
                        ),
                        data = {
                            'information': new_data,
                        }
                    )

                    # Return the information response
                    return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                
                except Exception as e:
                    # Error writing to file
                    raise EvServerException(
                        message = "Error writing to file",
                    )
                
        # If the information type is speaking introduction
        elif type == 'speaking-intro':
            # Define the filename
            file_path = os.path.join(JSON_DIR, "speaking_simulation_intro.json")
            ev_logger.info(file_path)
            ev_logger.info(os.path.exists(file_path))

            # If GET request, return the information
            if request.method == 'GET':
                # Check if the file exists
                if os.path.exists(file_path):
                    # Open the file and return the data
                    with open(file_path, 'r') as f:
                        # Load the data from the file
                        data_list = json.load(f)

                        # Define the response model data
                        response_data = EvResponseModel(
                            metadata = EvResponseMetadataModel(
                                code = 200,
                                status = 'Success',
                                message = 'Information retrieved successfully',
                            ),
                            data = {
                                'information': data_list,
                            }
                        )
                        # Return the information response
                        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                    
                raise EvServerException(
                    message = "File not found",
                )

            # If POST request, update the information
            elif request.method == 'POST':
                try:
                    # Check if have the request json data
                    if not request.is_json:
                        # Define the error message
                        message = 'Invalid request json data are required'

                        # Throw an exception
                        raise EvClientException(
                            message = message,
                            information = {
                                'message': message,
                            }
                        )
                    
                    # Get the json data from the request
                    new_data = request.get_json(force=True)

                    # Write the new data to the file
                    with open(file_path, 'w') as f:
                        # Dump the data to the file
                        json.dump(
                            new_data, 
                            f, 
                            indent = 4,
                        )

                    # Define the response model data
                    response_data = EvResponseModel(
                        metadata = EvResponseMetadataModel(
                            code = 200,
                            status = 'Success',
                            message = 'Information updated successfully',
                        ),
                        data = {
                            'information': new_data,
                        }
                    )

                    # Return the information response
                    return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                
                except Exception as e:
                    # Error writing to file
                    raise EvServerException(
                        message = "Error writing to file",
                    )
                
        else:
            # If the type is not valid, raise an exception
            raise EvClientException(
                message = "Invalid type",
            )
    
    except EvException as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
            ),
            data = {
                'message': error.message,
                'information': error.information,
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), error.status_code, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error in information',
            ),
            data = {
                'message': 'Internal server error in information',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}