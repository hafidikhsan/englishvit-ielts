from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/align', methods=['POST'])
def align():
    data = request.get_json()
    input_dir = data.get("input_path")
    output_dir = data.get("output_path")
    dictionary = data.get("dictionary", "english_us_arpa")
    acoustic_model = data.get("acoustic_model", "english_mfa")

    if not input_dir or not output_dir:
        return jsonify({"error": "Missing input_path or output_path"}), 400

    if not os.path.exists(input_dir):
        return jsonify({"error": f"Input path does not exist: {input_dir}"}), 400

    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run([
            "mfa", "align",
            input_dir,
            dictionary,
            acoustic_model,
            output_dir
        ], check=True)
        return jsonify({"status": "success", "message": "Alignment complete"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
