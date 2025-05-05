from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask with MFA!"

@app.route('/mfa')
def run_mfa():
    # Example: version check
    try:
        output = subprocess.check_output(["mfa", "--version"])
        return f"MFA is installed: {output.decode('utf-8')}"
    except Exception as e:
        return f"Error running MFA: {str(e)}"
    
@app.route('/download-mfa')
def download_mfa():
    # Example: downloading a model
    try:
        output = subprocess.check_output(["mfa", "model", "download", "acoustic", "english_mfa"])
        return f"Model downloaded: {output.decode('utf-8')}"
    except Exception as e:
        return f"Error downloading model: {str(e)}"

@app.route('/download-arpa')
def download_arpa():
    # Example: downloading an ARPA file
    try:
        output = subprocess.check_output(["mfa", "model", "download", "dictionary", "english_us_arpa"])
        return f"ARPA file downloaded: {output.decode('utf-8')}"
    except Exception as e:
        return f"Error downloading ARPA file: {str(e)}"
    
@app.route('/align')
def run_align():
    # Example: running a command
    try:
        output = subprocess.check_output(["mfa", "align", "audio", "english_us_arpa", "english_mfa", "audio"])
        return f"Alignment completed: {output.decode('utf-8')}"
    except Exception as e:
        return f"Error running alignment: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
