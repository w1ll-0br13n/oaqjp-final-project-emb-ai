from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotionDetector():
    # Get JSON data from POST request
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Please provide 'text' field in JSON payload"}), 400
    
    text_to_analyse = data['text']
    
    # Call the emotion detection function
    emotions = emotion_detector(text_to_analyse)
    
    # Check if dominant_emotion is None (error case)
    if emotions['dominant_emotion'] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    # Format response string as requested
    response_str = (f"For the given statement, the system response is "
                    f"'anger': {emotions['anger']}, 'disgust': {emotions['disgust']}, "
                    f"'fear': {emotions['fear']}, 'joy': {emotions['joy']} and "
                    f"'sadness': {emotions['sadness']}. The dominant emotion is {emotions['dominant_emotion']}.")
    
    return jsonify({
        "formatted_response": response_str
    })

@app.route('/')
def index():
    # Render the provided index.html page (in templates folder)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
