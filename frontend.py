import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import requests
import json
from PIL import Image
import pandas as pd

# Initialize Streamlit app
st.set_page_config(page_title="ECC Secure Payment System", page_icon="🔒", layout="wide", initial_sidebar_state="expanded")

# Set up the dropdown menu in the sidebar
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "Login", "Transaction", "Transaction History"],
        icons=["house", "key", "cash-coin", "clock-history"],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"background-color": "#333"},
            "icon": {"color": "white"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#444"},
            "nav-link-selected": {"background-color": "#444"},
        }
    )

# Define a function to display the logos
def display_logo():
    try:
        # Load the images
        logo1 = Image.open("/Users/rishigupta/Documents/IITG_Project/Prototype_1/images/IITG_White.png")
        logo2 = Image.open("/Users/rishigupta/Documents/IITG_Project/Prototype_1/images/logo-e78ff0ab.webp")

        # Display the images side by side
        col1, col2, col3 = st.columns([0.15, 0.1, 1])
        col1.image(logo1, width=200, caption="")
        col3.image(logo2, width=200, caption="")
    except Exception as e:
        st.error(f"Error loading images: {e}")

# Display the logo at the top of each page
display_logo()

# Define content for each page
if selected == "Home":
    st.title("ECC Secure Payment System")
    st.subheader("Welcome to the ECC Secure Payment System")
    st.write("""
        This project utilizes Elliptic Curve Cryptography (ECC) to enable secure payments.
        ECC is a public-key encryption technique based on elliptic curve theory that can create faster, smaller,
        and more efficient cryptographic keys. Here’s how it works:
        
        1. **Key Generation:** Each user generates a public and private key pair.
        2. **Transaction Signing:** Transactions are signed using the sender's private key.
        3. **Signature Verification:** The transaction is verified using the sender's public key.
        
        This ensures that only the owner of the private key can initiate a transaction, providing a high level of security.
    """)
    st.write("""
        ## How to Use
        1. Navigate to the Login page to register or log in.
        2. Use your keys to initiate and track transactions.
        3. View your transaction history.
    """)

elif selected == "Login":
    st.title("Login")
    st.subheader("First-time users will receive their public and private keys upon login.")
    user_id = st.text_input("User ID")
    if st.button("Register / Login"):
        response = requests.post("http://127.0.0.1:5000/login", json={"user_id": user_id})
        if response.status_code == 200:
            keys = response.json()
            st.write("### Your Keys")
            cols = st.columns(2)
            with cols[0]:
                ui.metric_card(title="Public Key", content=keys['public_key'], description="Your ECC Public Key", key="pub_key_card")
            with cols[1]:
                ui.metric_card(title="Private Key", content=keys['private_key'], description="Your ECC Private Key", key="priv_key_card")
        else:
            st.error("Login failed. Please try again.")

elif selected == "Transaction":
    st.title("Transaction")
    st.subheader("Send Transaction")
    from_user_id = st.text_input("From User ID")
    private_key = st.text_input("Private Key", type="password")
    to_user_id = st.text_input("To User ID")
    amount = st.text_input("Amount")

    if st.button("Send"):
        data = {
            'from_user_id': from_user_id,
            'private_key': private_key,
            'to_user_id': to_user_id,
            'amount': amount
        }
        response = requests.post("http://127.0.0.1:5000/send_transaction", json=data)
        if response.status_code == 200:
            result = response.json()
            st.success("Transaction successful")
            st.write(f"**Signature:** {result['signature']}")
        else:
            st.error("Transaction failed")

elif selected == "Transaction History":
    st.title("Transaction History")
    if st.button("Show Transactions"):
        response = requests.get("http://127.0.0.1:5000/transactions")
        if response.status_code == 200:
            transactions = response.json()
            if transactions:  # Check if transactions list is not empty
                # Convert transactions list to DataFrame
                transactions_df = pd.DataFrame(transactions)
                # Display transactions in a simple table
                st.dataframe(transactions_df)
            else:
                st.info("No transactions available.")
        else:
            st.error("Failed to retrieve transactions")

# Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #ffffff;
            color: black;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        Developed by Rishi Gupta and Akarshan Nagpal | 
        <a href="https://github.com/rishigupta2004" style="color: black;">Your GitHub</a> | 
        <a href="https://github.com/akarshann" style="color: black;">Teammate's GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
