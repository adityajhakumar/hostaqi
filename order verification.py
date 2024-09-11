import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize session state orders DataFrame if not exists
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=['order_id', 'timestamp', 'email'])

# Function to add order to session state
def add_order(order_id, user_email):
    timestamp = datetime.datetime.now()
    new_order = pd.DataFrame({'order_id': [order_id], 'timestamp': [timestamp], 'email': [user_email]})
    
    # Filter out empty or all-NA columns before concatenation to avoid warnings
    if not new_order.dropna(how='all').empty:
        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)

# Function to send email using Gmail (with app password)
def send_email(recipient_email, order_id):
    sender_email = 'vidushi.agnihotri26@gmail.com'
    sender_password = 'dhan wweb tqmz tfya'  # Your app password
    subject = 'Tervive Order Confirmation'

    message = f"""
    Dear Customer,

    Thank you for purchasing through Tervive! We truly appreciate your efforts to save the planet and uplift society.

    Your order process is still under verification. The order ID is: {order_id}.
    You will receive credits once verification is complete.

    For any concerns, please contact us at 9003605331, or visit our website at https://tervive.vercel.app/.
    You can also track your plant's growth at: https://hostaqi-jcvnydnopmmpkmexbwwr5b.streamlit.app/

    Best regards,
    Tervive Team
    """

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Set up the server connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Function to check credit eligibility
def check_credit(order_id):
    current_time = datetime.datetime.now()

    # Ensure the timestamp column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(st.session_state.orders['timestamp']):
        st.session_state.orders['timestamp'] = pd.to_datetime(st.session_state.orders['timestamp'])
    
    order = st.session_state.orders[st.session_state.orders['order_id'] == order_id]
    if not order.empty:
        order_time = order['timestamp'].values[0]
        if isinstance(order_time, pd.Timestamp):
            difference = (current_time - order_time).days
            if difference >= 15:
                return True
    return False

# Streamlit UI
st.title('Amazon Order Verification for Credit')

order_id = st.text_input('Enter your Amazon Order ID:')
user_email = st.text_input('Enter your Email ID:')

if st.button('Submit'):
    if order_id and user_email:
        add_order(order_id, user_email)
        if send_email(user_email, order_id):
            st.success('Order ID submitted successfully! We will check your credit eligibility after 15 days.')
        else:
            st.error('Order submitted, but email could not be sent.')
    else:
        st.error('Please enter both a valid Order ID and Email ID.')

# Simulate credit check
if st.button('Check Credit'):
    if order_id:
        if check_credit(order_id):
            st.success('You are eligible for credit!')
        else:
            st.error('You are not yet eligible for credits. Please wait until we verify your order status.')
    else:
        st.error('Please enter a valid Order ID to check credit.')
