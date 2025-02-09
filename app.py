from flask import Flask, request, jsonify  # type: ignore
from credibility import analyze_credibility  # type: ignore # We'll create this next

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    # Analyze the text
    score, flags = analyze_credibility(text)

    return jsonify({"score": score, "flags": flags})


if __name__ == "__main__":
    app.run(debug=True)
