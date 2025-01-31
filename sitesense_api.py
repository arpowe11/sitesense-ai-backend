#
# Description: API gateway for SiteSense AI Agent, enabling communication between the AI logic and the frontend.
# Author: Alexander Powell
# Version: v1.0
# Dependencies: flask, jsonify, sitesense_ai
#


from flask import Flask, jsonify, request
from typing import Any
from src.sitesense_ai import SiteSenseAI


ss_api: Flask = Flask(__name__)
agent_emily: SiteSenseAI = SiteSenseAI(model="gpt-4-turbo", temp=0.8)


@ss_api.route('/get-ai-response', methods=['POST'])
def get_response():
    try:
        if request.method == 'POST':
            data: Any = request.json
            ai_response: dict = agent_emily.engage(data["question"])
            return jsonify("ai_response:", ai_response["output"]), 200
        else:
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as ex:
        return jsonify({'error': f'Something went wrong: {ex}'}), 400


if __name__ == '__main__':
    ss_api.run(debug=True, port=5000)
