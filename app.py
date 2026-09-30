import joblib


# Load the trained model
model = joblib.load("spam_model.pkl")

# Load the TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load the classification threshold
threshold = joblib.load("spam_threshold.pkl")


# Function to predict whether a message is spam
def predict_message(message):
    # Convert the message into TF-IDF features
    message_tfidf = vectorizer.transform([message])

    # Get the probability that the message is spam
    spam_probability = model.predict_proba(message_tfidf)[0][1]

    # Apply the 0.30 classification threshold
    if spam_probability >= threshold:
        prediction = "spam"
    else:
        prediction = "ham"

    return prediction, spam_probability


# Ask the user for a message
message = input("Enter a message: ")

# Make the prediction
prediction, probability = predict_message(message)

# Display the result
print()
print("Message:", message)
print("Prediction:", prediction)
print("Spam probability:", round(probability, 3))