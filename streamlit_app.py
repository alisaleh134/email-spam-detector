import streamlit as st

from database import (
    save_prediction,
    get_predictions,
    get_statistics,
    clear_predictions
)

from predictor import (
    predict_message,
    get_probability_level
)


st.set_page_config(
    page_title="AI Spam Detector",
    page_icon="📩",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("📩 AI SMS Spam Detector")

st.write(
    "Enter a message and the machine learning model "
    "will determine whether it is spam or not."
)

st.divider()


# -----------------------------
# Message Input
# -----------------------------

message = st.text_area(
    "Message",
    height=150,
    placeholder="Example: Congratulations! You won a free prize!"
)


# -----------------------------
# Prediction
# -----------------------------

if st.button("🔍 Check Message", use_container_width=True):

    if not message.strip():

        st.warning("Please enter a message.")

    else:

        prediction, spam_probability = predict_message(message)

        probability_level = get_probability_level(
            spam_probability
        )

        # Save prediction to SQLite
        save_prediction(
            message,
            prediction,
            spam_probability,
            probability_level
        )

        st.divider()

        if prediction == "spam":

            st.error("🚨 SPAM MESSAGE")

        else:

            st.success("✅ NOT SPAM")

        st.write(
            f"**Spam probability:** {spam_probability:.1%}"
        )

        st.progress(spam_probability)

        st.write(
            f"**Spam probability level:** {probability_level}"
        )

        if prediction == "spam":

            st.write(
                "⚠️ The model detected patterns commonly "
                "associated with spam messages."
            )

        else:

            st.write(
                "✅ The model did not detect strong "
                "spam patterns in this message."
            )


# -----------------------------
# Prediction History
# -----------------------------

st.divider()

st.subheader("📋 Prediction History")

predictions = get_predictions()

if predictions:

    history = []

    for prediction in predictions:

        history.append({
            "Message": prediction[0],
            "Prediction": prediction[1].upper(),
            "Spam Probability": f"{prediction[2]:.1%}",
            "Level": prediction[3],
            "Date": prediction[4]
        })

    st.dataframe(
        history,
        use_container_width=True
    )

    if st.button("🗑️ Clear Prediction History"):

        clear_predictions()

        st.success("Prediction history cleared.")

        st.rerun()

else:

    st.info("No predictions saved yet.")


# -----------------------------
# Analytics
# -----------------------------

st.divider()

st.subheader("📊 Analytics")

total, spam, ham = get_statistics()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Messages",
        total
    )

with col2:

    st.metric(
        "Spam",
        spam
    )

with col3:

    st.metric(
        "Not Spam",
        ham
    )


# Spam percentage

spam_percentage = (
    spam / total * 100
    if total > 0
    else 0
)

st.write(
    f"**Spam Percentage:** {spam_percentage:.1f}%"
)


# Chart

chart_data = {
    "Message Type": [
        "Spam",
        "Not Spam"
    ],
    "Count": [
        spam,
        ham
    ]
}

st.bar_chart(
    chart_data,
    x="Message Type",
    y="Count"
)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "Machine Learning Model: Logistic Regression + TF-IDF"
)