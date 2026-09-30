import joblib


# Load the trained model
model = joblib.load("spam_model.pkl")

# Load the TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load the classification threshold
threshold = joblib.load("spam_threshold.pkl")


def predict_message(message):
    """
    Predict whether a message is spam or ham.

    Returns:
        prediction: "spam" or "ham"
        spam_probability: probability between 0 and 1
    """

    # Convert the message into TF-IDF features
    message_tfidf = vectorizer.transform([message])

    # Get spam probability
    spam_probability = model.predict_proba(message_tfidf)[0][1]

    # Apply the classification threshold
    if spam_probability >= threshold:
        prediction = "spam"
    else:
        prediction = "ham"

    return prediction, spam_probability

def get_probability_level(spam_probability):
    """
    Convert spam probability into a simple risk level.
    """

    if spam_probability < 0.30:
        return "Low"

    elif spam_probability < 0.70:
        return "Medium"

    else:
        return "High"