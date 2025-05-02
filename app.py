import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Configure the page
st.set_page_config(page_title='Stock Price Predictions', layout='wide')
st.title('📈 Stock Price Predictions')
st.sidebar.info('Welcome to the Stock Price Prediction App. Choose your options below')
st.sidebar.info("Created and designed by [Nare Vignesh](https://www.linkedin.com/in/narevignesh/)")

# Popular stock symbols
STOCK_SYMBOLS = {
    'S&P 500': 'SPY',
    'NASDAQ 100': 'QQQ',
    'Dow Jones': 'DIA',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Google': 'GOOGL',
    'Tesla': 'TSLA',
    'Nvidia': 'NVDA',
    'Meta (Facebook)': 'META',
    'Netflix': 'NFLX',
    'Berkshire Hathaway': 'BRK-B',
    'JPMorgan Chase': 'JPM',
    'Bank of America': 'BAC',
    'Walmart': 'WMT',
    'Visa': 'V',
    'Johnson & Johnson': 'JNJ',
    'Procter & Gamble': 'PG',
    'Coca-Cola': 'KO',
    'Disney': 'DIS'
}

# Initialize data as None at the start
data = None

def main():
    option = st.sidebar.selectbox('Make a choice', ['Visualize', 'Recent Data', 'Predict'])
    if option == 'Visualize':
        visualize_data()
    elif option == 'Recent Data':
        show_recent_data()
    else:
        predict()

@st.cache_data
def download_data(symbol, start_date, end_date):
    try:
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        if df.empty:
            st.error(f'No data found for {symbol}. Please check the stock symbol.')
            return None
        return df
    except Exception as e:
        st.error(f'Error downloading data: {str(e)}')
        return None

def get_user_input():
    # Create a selectbox with stock names but store the symbol
    selected_stock = st.sidebar.selectbox(
        'Select a Stock', 
        options=list(STOCK_SYMBOLS.keys()),
        format_func=lambda x: f"{x} ({STOCK_SYMBOLS[x]})"
    )
    symbol = STOCK_SYMBOLS[selected_stock]
    
    today = date.today()
    duration = st.sidebar.number_input('Enter the duration (days)', value=3000, min_value=1, max_value=10000)
    start_date = st.sidebar.date_input('Start Date', value=today - timedelta(days=duration))
    end_date = st.sidebar.date_input('End Date', today)
    return symbol, start_date, end_date

def visualize_data():
    st.header('Stock Data Visualization')
    if data is None:
        st.error("No data available. Please check your input parameters.")
        return
        
    chart_type = st.radio('Choose what to visualize', ['Closing Price', 'Volume'])
    
    if chart_type == 'Closing Price':
        st.line_chart(data['Close'])
    elif chart_type == 'Volume':
        st.bar_chart(data['Volume'])

def show_recent_data():
    st.header('Recent Data')
    if data is not None:
        st.dataframe(data.tail(10))
    else:
        st.error('No data available. Please check your input parameters.')

def predict():
    if data is None:
        st.error('No data available for prediction. Please check your input parameters.')
        return

    st.header('Stock Price Prediction')
    model_name = st.selectbox('Choose a model', ['LinearRegression', 'RandomForestRegressor', 'KNeighborsRegressor', 'XGBoostRegressor'])
    num = st.slider('How many days to forecast?', value=5, min_value=1, max_value=30)

    if st.button('Predict', type='primary'):
        with st.spinner('Training model and making predictions...'):
            model = {
                'LinearRegression': LinearRegression(),
                'RandomForestRegressor': RandomForestRegressor(n_estimators=100, random_state=42),
                'KNeighborsRegressor': KNeighborsRegressor(n_neighbors=5),
                'XGBoostRegressor': XGBRegressor(n_estimators=100, random_state=42)
            }[model_name]

            model_engine(model, int(num))

def model_engine(model, num):
    df = data[['Close']].copy()
    df['preds'] = df['Close'].shift(-num)

    # Check if we have enough data for prediction
    if len(df) < num:
        st.error(f"Not enough data for {num}-day prediction. Need at least {num} more days of data.")
        return

    x = df[['Close']].values[:-num]
    y = df['preds'].values[:-num]
    x_forecast = df[['Close']].values[-num:]

    # Check if we have data to predict
    if len(x) == 0 or len(y) == 0:
        st.error("Not enough data points for training. Try with a smaller forecast period.")
        return

    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    x_forecast = scaler.transform(x_forecast)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    
    # Display metrics in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric('R² Score', f"{r2_score(y_test, preds):.4f}")
    with col2:
        st.metric('Mean Absolute Error', f"{mean_absolute_error(y_test, preds):.4f}")

    st.subheader('Future Predictions')
    forecast_pred = model.predict(x_forecast)
    future_dates = pd.date_range(start=data.index[-1] + timedelta(days=1), periods=num)

    prediction_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted Price': forecast_pred
    })

    # Display chart and data
    st.line_chart(prediction_df.set_index('Date'))
    
    # Format the dataframe for better display
    styled_df = prediction_df.style.format({
        'Date': lambda x: x.strftime('%Y-%m-%d'),
        'Predicted Price': '{:.2f}'
    })
    st.dataframe(styled_df)

# Entry point
if __name__ == '__main__':
    symbol, start_date, end_date = get_user_input()
    if start_date < end_date:
        data = download_data(symbol, start_date, end_date)
        if data is not None:
            main()
    else:
        st.error('End date must be after start date.')