
# FinanceFlow 💸

FinanceFlow is a personal finance tracker application built using Streamlit. It allows users to log their income and expenses, view their financial data, and visualize their financial status over time. The app features a sleek neumorphic design for an enhanced user experience.

## Features

- User Registration and Login
- Add and View Income
- Add and View Expenses
- Visualize Income and Expenses
- Clear All Data

## Technologies Used

- Streamlit
- SQLite
- bcrypt
- Pandas
- Plotly

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/financeflow.git
    cd financeflow
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    streamlit run financial_tracker.py
    ```

## File Structure

financeflow/
│
├── data/ # Directory for SQLite database files
├── styles.css # CSS file for neumorphic design
├── financial_tracker.py # Main Streamlit application
├── requirements.txt # List of required packages
└── README.md # This README file


## Usage

1. Launch the application using Streamlit:
    ```bash
    streamlit run financial_tracker.py
    ```

2. Open your web browser and go to the provided local URL (usually http://localhost:8501).

3. Use the sidebar to navigate through the app:
    - Home: Welcome page with buttons to navigate to other sections.
    - Login: Login page for existing users.
    - SignUp: Registration page for new users.
    - Add Income: Page to add new income entries.
    - Add Expense: Page to add new expense entries.
    - View Income: Page to view all income entries.
    - View Expenses: Page to view all expense entries.
    - Visualize Data: Page to visualize income and expenses over time.
    - Clear Data: Page to clear all data for the logged-in user.



