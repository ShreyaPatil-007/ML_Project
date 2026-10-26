
# SmartStock AI 📦

### AI-Powered Retail Demand Forecasting and Inventory Decision Support System

**Developer:** Shreya Gurbas Patil  
**PRN:** RBT24CS021

## About the Project

SmartStock AI is a machine-learning-based retail demand forecasting project. It combines a trained AdaBoost regression model, a FastAPI backend, and a Streamlit dashboard. A Google Gemini LLM assistant is being integrated to explain predictions and provide general inventory-planning guidance.

## Features

- Retail demand prediction using machine learning
- Historical demand lag and calendar-based features
- Model comparison using MAE and RMSE
- FastAPI prediction endpoint
- Streamlit dashboard
- Gemini LLM assistant integration
- Secure API-key configuration using environment variables


<img width="1357" height="640" alt="Screenshot 2026-10-26 195635" src="https://github.com/user-attachments/assets/579c5061-27c8-4553-b5b3-0952a0d75cfb" />



<img width="1365" height="677" alt="Screenshot 2026-10-26 195548" src="https://github.com/user-attachments/assets/bdea2bb4-b2f0-470e-acab-742d10879f8b" />


<img width="1364" height="640" alt="Screenshot 2026-10-26 195612" src="https://github.com/user-attachments/assets/dadea5bc-7607-47b0-854b-4877bfe1de3e" />



## Tech Stack

- Python
- Pandas and NumPy
- Scikit-learn
- AdaBoost Regressor
- FastAPI and Uvicorn
- Streamlit
- Google Gemini API

## Project Structure

```text
ML_Project/
├── app.py
├── streamlit_app.py
├── data/
├── models/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a local `.env` file:

```text
GEMINI_API_KEY=your_gemini_api_key
```

5. Start the FastAPI backend:

```bash
python -m uvicorn app:app --reload
```

6. In a separate terminal, start Streamlit:

```bash
python -m streamlit run streamlit_app.py
```

7. Open `http://localhost:8501` in your browser.

## Current Scope

The current forecasting model is trained for Store S001 and Product P0001. Predictions depend on the historical demand inputs supplied to the API.

## Limitations

- The model currently supports one store/product series.
- Historical demand inputs are supplied manually.
- Predictions are estimates, not guaranteed future sales.
- Inventory alerts require reliable current-stock and lead-time data.

## Future Improvements

- Support multiple stores and products
- Retrieve historical data automatically
- Add forecast-versus-actual visualizations
- Add inventory shortage alerts
- Improve the LLM assistant with verified inventory data

## Author

Shreya Gurbas Patil
