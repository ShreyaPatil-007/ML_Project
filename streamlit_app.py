
import requests
import streamlit as st
from datetime import date

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(api_key)

# Page settings
st.set_page_config(
    page_title="SmartStock AI",
    page_icon="📦",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.title("📦 SmartStock AI")
st.subheader("Retail Demand Forecasting Dashboard")
st.write(
    "Predict product demand using your trained AdaBoost machine learning model."
)

st.divider()

# Sidebar
st.sidebar.header("⚙️ Forecast Settings")
store_id = st.sidebar.selectbox("Select Store", ["S001"])
product_id = st.sidebar.selectbox("Select Product", ["P0001"])

st.sidebar.info(
    "Current model is trained for Store S001 and Product P0001."
)

# Input section
st.header("🔮 Predict Future Demand")
st.write("Enter historical demand values for the selected product.")

col1, col2 = st.columns(2)

with col1:
    forecast_date = st.date_input(
        "Forecast Date",
        value=date.today()
    )

    lag_1 = st.number_input(
        "Demand 1 day ago",
        min_value=0.0,
        value=99.0
    )

    lag_7 = st.number_input(
        "Demand 7 days ago",
        min_value=0.0,
        value=113.0
    )

with col2:
    lag_14 = st.number_input(
        "Demand 14 days ago",
        min_value=0.0,
        value=110.0
    )

    rolling_mean = st.number_input(
        "Average demand over previous 7 days",
        min_value=0.0,
        value=105.0
    )

st.caption(
    "Note: Default values are sample inputs. "
    "Replace them with actual historical demand when available."
)

if st.button("🚀 Predict Demand", type="primary"):
    payload = {
        "date": forecast_date.isoformat(),
        "demand_lag_1": lag_1,
        "demand_lag_7": lag_7,
        "demand_lag_14": lag_14,
        "rolling_mean_7": rolling_mean
    }

    try:
        with st.spinner("Predicting demand..."):
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                timeout=30
            )

        if response.ok:
            result = response.json()
            predicted = result["predicted_demand"]

            st.session_state.latest_forecast = {
                "date": result["date"],
                "store_id": result["store_id"],
                "product_id": result["product_id"],
                "predicted_demand": predicted
            }

            st.success("Demand prediction completed!")

            st.subheader("📊 Forecast Results")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Predicted Demand",
                f'{predicted:.2f} units'
            )

            metric2.metric(
                "Store ID",
                result["store_id"]
            )

            metric3.metric(
                "Product ID",
                result["product_id"]
            )

            st.write(f"**Forecast date:** {result['date']}")

            st.subheader("📈 Demand Visualization")

            st.bar_chart({
                "Demand": [predicted]
            }, x_label="Forecast", y_label="Predicted units")

            st.info(
                f"Estimated demand is approximately "
                f"{round(predicted)} units. "
                "This is a model prediction, not actual confirmed demand."
            )

        else:
            st.error(
                f"API error ({response.status_code}): "
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI server is not running. "
            "Start the API in another terminal first."
        )

    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")

st.divider()
st.caption("SmartStock AI | Machine Learning Project")



import os
from google import genai

st.divider()
st.header("🤖 SmartStock AI Assistant")
st.write(
    "Ask questions about demand forecasting, "
    "inventory planning, and your latest prediction."
)

# Keep chat history between Streamlit reruns
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# Store latest forecast for the assistant
if "latest_forecast" not in st.session_state:
    st.session_state.latest_forecast = None

# Display chat history
for message in st.session_state.ai_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask: How can I plan stock for predicted demand?"
)

if question:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "Gemini API key missing. Set GEMINI_API_KEY "
            "in PowerShell and restart Streamlit."
        )
    else:
        st.session_state.ai_messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        forecast_context = st.session_state.latest_forecast

        if forecast_context:
            context_text = str(forecast_context)
        else:
            context_text = (
                "No forecast has been generated in this session yet."
            )

        prompt = f"""
You are SmartStock AI, a retail demand forecasting assistant.

Explain concepts in simple English.
Give practical inventory-planning suggestions.
Do not invent sales data or claim suggestions are guaranteed.
Clearly distinguish model predictions from actual demand.

Latest available forecast:
{context_text}

User question:
{question}
"""

        try:
            with st.chat_message("assistant"):
                with st.spinner("SmartStock AI is thinking..."):
                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=prompt
                    )

                    answer = response.text or (
                        "I could not generate a response. Please try again."
                    )

                st.markdown(answer)

            st.session_state.ai_messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(
                "Gemini request failed. Check your API key, "
                "model availability, internet connection, and API quota."
            )
            st.caption(str(error))



# Questions : 

# “Explain my predicted demand.”
# “How much stock should I keep?”
# “What is demand forecasting?”
# “How can I reduce overstocking?”