from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import Conversation

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["POST", "GET"],
            "allow_headers": ["Content-Type"],
        }
    },
)

conversation = Conversation()


conversation_history = {}
MAX_HISTORY_SIZE = 50


@app.route("/api/chat/clear", methods=["POST"])
def clear_history():
    try:
        session_id = "default_session"
        if session_id in conversation_history:
            conversation_history[session_id] = []
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        session_id = "default_session"

        # Initialize or trim history if too long
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        elif len(conversation_history[session_id]) >= MAX_HISTORY_SIZE:
            conversation_history[session_id] = conversation_history[session_id][
                -MAX_HISTORY_SIZE:
            ]

        # Add the current question to history
        conversation_history[session_id].append(f"User: {data['question']}")

        # Get only the last 10 exchanges
        history = (
            conversation_history[session_id][-10:]
            if conversation_history[session_id]
            else []
        )

        vector = conversation.encoder.encode(data["question"]).tolist()
        results = conversation.index.query(
            vector=vector,
            top_k=3,
            include_values=False,
            include_metadata=True,
        )
        context = " ".join([match["metadata"]["text"] for match in results["matches"]])
        response = conversation.generate_response(context, data["question"])

        # Add the response to history
        conversation_history[session_id].append(f"Scorsese: {response}")

        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
