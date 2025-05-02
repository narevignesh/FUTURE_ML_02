# Stock Price Prediction App

## Overview
This project is a Stock Price Prediction application built using Streamlit, which allows users to visualize stock data, view recent stock prices, and make predictions about future stock prices using various machine learning models.

## Features
- **Data Visualization**: Users can visualize stock closing prices and trading volumes.
- **Recent Data**: Displays the most recent stock data.
- **Price Prediction**: Users can select a machine learning model to predict future stock prices based on historical data.

## Technologies Used
- **Streamlit**: For building the web application.
- **Pandas**: For data manipulation and analysis.
- **yfinance**: For downloading historical stock data.
- **Scikit-learn**: For machine learning models and data preprocessing.
- **XGBoost**: For advanced regression modeling.
- **Matplotlib**: For plotting (integrated within Streamlit).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/narevignesh/FUTURE_ML_02.git
   cd FUTURE_ML_02
   ```

2. Install the required packages:
   ```bash
   pip install streamlit pandas yfinance scikit-learn xgboost
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the application.

3. Use the sidebar to select a stock, specify the date range, and choose the desired functionality (Visualize, Recent Data, or Predict).

## How to Contribute
Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.


## Author
- [Nare Vignesh](https://www.linkedin.com/in/narevignesh/)

## Acknowledgments
- Thanks to the contributors of the libraries used in this project.

---

