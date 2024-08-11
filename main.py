from flask import Flask, request, jsonify
import requests
import re
import json

app = Flask(__name__)

@app.route('/ai', methods=['GET'])
def ai_search():
    user_question = request.args.get('search')

    url = "https://www.blackbox.ai/api/chat"

    payload = {
        "messages": [
            {
                "id": "R8D4nWC",
                "content": user_question,
                "role": "user"
            }
        ],
        "id": "R8D4nWC",
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "agentMode": {},
        "trendingAgentMode": {},
        "isMicMode": False,
        "maxTokens": 1024,
        "isChromeExt": False,
        "githubToken": None,
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": None
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    def pretty_print_json(data):
        return json.dumps(data, indent=4, separators=(',', ': '))

    if response.status_code == 200:
        try:
            json_response = response.json()
            return app.response_class(
                response=pretty_print_json({
                    "status_code": response.status_code,
                    "response": json_response
                }),
                mimetype='application/json'
            )
        except requests.exceptions.JSONDecodeError:
            cleaned_response_text = re.sub(r'\$@.*?\$@', '', response.text)
            return app.response_class(
                response=pretty_print_json({
                    
"author": "Kiff Hyacinth Pon",                    
                    "response_text": cleaned_response_text,
                    "status_code": response.status_code
                }),
                mimetype='application/json'
            )
    else:
        return app.response_class(
            response=pretty_print_json({
                "error": "Failed to get a valid response from the API.",
                "response_text": response.text,
                "status_code": response.status_code
            }),
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
