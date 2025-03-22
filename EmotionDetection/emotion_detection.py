"""
Emotion Detection Module

This module sends a text to the Watson Emotion API and returns the detected emotions.
"""

import json
import requests

def emotion_detector(text_to_analyze):
    """
    Analyze the emotion of the given text using Watson Emotion API.

    Args:
        text_to_analyze (str): The input text.

    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion.
    """
    url = ('https://sn-watson-emotion.labs.skills.network/v1/'
           'watson.runtime.nlp.v1/NlpService/EmotionPredict')
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}

    # Initialize emotions with default values
    anger = None
    disgust = None
    fear = None
    joy = None
    sadness = None
    dominant_emotion = None

    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        formatted_response = json.loads(response.text)

        if response.status_code == 200:
            emotions = formatted_response.get('emotionPredictions', [{}])[0].get('emotion', {})
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)
            dominant_emotion = max(emotions, key=emotions.get, default=None)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return {'anger': anger, 'disgust': disgust, 'fear': fear, 'joy': joy,
            'sadness': sadness, 'dominant_emotion': dominant_emotion}
