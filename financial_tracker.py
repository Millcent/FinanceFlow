import os
import sqlite3
import bcrypt
import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="FinanceFlow 💸")
# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")


# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to check hashed passwords
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Function to register users
def register_user(username, password):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?, ?)', (username, hashed_password))
        conn.commit()
        st.success("You have successfully registered!")
    except sqlite3.IntegrityError:
        st.error("Username already exists")
    finally:
        conn.close()

# Function to login users
def login_user(username, password):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    if data and check_password(data[0], password):
        return True
    return False

# Connect to the database and create tables if they don't exist
def create_tables():
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()

    # Create users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create income table
    c.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create expenses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_tables()

def add_income(username, amount, category, date, description):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO income (username, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, amount, category, date, description))
    conn.commit()
    conn.close()
    st.success("Income added successfully!")

def add_expense(username, amount, category, date, description):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (username, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, amount, category, date, description))
    conn.commit()
    conn.close()
    st.success("Expense added successfully!")

def view_data(table, username):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM {table} WHERE username = ?', (username,))
    data = c.fetchall()
    conn.close()
    return data

def clear_data(username):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('DELETE FROM income WHERE username = ?', (username,))
    c.execute('DELETE FROM expenses WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    st.success("All your data has been cleared!")

def visualize_data(username):
    conn = sqlite3.connect('data/users.db')
    income_df = pd.read_sql_query(f'SELECT * FROM income WHERE username = "{username}"', conn)
    expenses_df = pd.read_sql_query(f'SELECT * FROM expenses WHERE username = "{username}"', conn)
    conn.close()

    if not income_df.empty:
        st.subheader("Income Data")
        fig_income_bar = px.bar(income_df, x='date', y='amount', color='category', title='Income Over Time')
        st.plotly_chart(fig_income_bar)

        fig_income_pie = px.pie(income_df, values='amount', names='category', title='Total Income by Category')
        st.plotly_chart(fig_income_pie)

    if not expenses_df.empty:
        st.subheader("Expenses Data")
        fig_expenses_bar = px.bar(expenses_df, x='date', y='amount', color='category', title='Expenses Over Time')
        st.plotly_chart(fig_expenses_bar)

        fig_expenses_pie = px.pie(expenses_df, values='amount', names='category', title='Total Expenses by Category')
        st.plotly_chart(fig_expenses_pie)

    if not income_df.empty and not expenses_df.empty:
        total_income = income_df['amount'].sum()
        total_expenses = expenses_df['amount'].sum()
        surplus_deficit = total_income - total_expenses

        st.subheader("Surplus/Deficit")
        st.write(f"Total Income: ${total_income}")
        st.write(f"Total Expenses: ${total_expenses}")
        st.write(f"Surplus/Deficit: ${surplus_deficit}")

        fig_surplus_deficit = px.bar(
            x=['Total Income', 'Total Expenses', 'Surplus/Deficit'],
            y=[total_income, total_expenses, surplus_deficit],
            title='Surplus/Deficit',
            labels={'x': 'Category', 'y': 'Amount'},
            color=['Total Income', 'Total Expenses', 'Surplus/Deficit'],
            color_discrete_map={'Total Income': 'green', 'Total Expenses': 'red', 'Surplus/Deficit': 'blue'}
        )
        st.plotly_chart(fig_surplus_deficit)

def main():
    st.title("Personal Finance Tracker")

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    def set_page(page):
        st.session_state.page = page

    menu = ["Home", "Login", "SignUp", "Add Income", "Add Expense", "View Income", "View Expenses", "Visualize Data", "Clear Data"]
    
    # Sidebar menu
    choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state.page))

    if choice:
        set_page(choice)

    if st.session_state.page == "Home":
        st.subheader("Welcome to the FinanceFlow - Your Personal Finance Tracker!")
        st.write("""
            This app helps you keep track of your income and expenses. You can log your financial transactions, 
            view your financial data, and visualize your income and expenses over time.
        """)
        
        if st.session_state.logged_in:
            st.success(f"Logged in as {st.session_state.username}")
            st.write("What would you like to do next?")
            col1, col2, col3 = st.columns(3)
            if col1.button("Add Income"):
                set_page("Add Income")
                st.experimental_rerun()
            if col2.button("Add Expense"):
                set_page("Add Expense")
                st.experimental_rerun()
            if col3.button("Visualize Data"):
                set_page("Visualize Data")
                st.experimental_rerun()
        else:
            st.warning("You are not logged in. Please log in to use the app's features.")

    elif st.session_state.page == "Login":
        st.subheader("Login Section")

        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged In as {}".format(username))
                set_page("Home")
                st.experimental_rerun()
            else:
                st.warning("Incorrect Username/Password")
    
    elif st.session_state.page == "SignUp":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("SignUp"):
            register_user(new_user, new_password)
            set_page("Login")
            st.experimental_rerun()
    
    elif st.session_state.page == "Add Income":
        if st.session_state.logged_in:
            st.subheader("Add Income")

            username = st.session_state.username
            amount = st.number_input("Amount")
            category = st.text_input("Category")
            date = st.date_input("Date")
            description = st.text_area("Description")
            if st.button("Add Income"):
                add_income(username, amount, category, date, description)
        else:
            st.warning("You need to log in to add income.")

    elif st.session_state.page == "Add Expense":
        if st.session_state.logged_in:
            st.subheader("Add Expense")

            username = st.session_state.username
            amount = st.number_input("Amount")
            category = st.text_input("Category")
            date = st.date_input("Date")
            description = st.text_area("Description")
            if st.button("Add Expense"):
                add_expense(username, amount, category, date, description)
        else:
            st.warning("You need to log in to add expenses.")

    elif st.session_state.page == "View Income":
        if st.session_state.logged_in:
            st.subheader("View Income")
            username = st.session_state.username
            income_data = view_data('income', username)
            st.write(income_data)
        else:
            st.warning("You need to log in to view income data.")

    elif st.session_state.page == "View Expenses":
        if st.session_state.logged_in:
            st.subheader("View Expenses")
            username = st.session_state.username
            expenses_data = view_data('expenses', username)
            st.write(expenses_data)
        else:
            st.warning("You need to log in to view expense data.")

    elif st.session_state.page == "Visualize Data":
        if st.session_state.logged_in:
            st.subheader("Visualize Data")
            username = st.session_state.username
            visualize_data(username)
        else:
            st.warning("You need to log in to visualize data.")

    elif st.session_state.page == "Clear Data":
        if st.session_state.logged_in:
            st.subheader("Clear Data")
            st.write("This will delete all your income and expense data.")
            if st.button("Clear Data"):
                clear_data(st.session_state.username)
        else:
            st.warning("You need to log in to clear your data.")

if __name__ == '__main__':
    main()
