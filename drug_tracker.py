import streamlit as st
import pandas as pd
import psycopg2
import smtplib
import datetime

# Database connection details (replace with your actual values)
DB_NAME = "drug_inventory"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"

# Email configuration (replace with your email credentials)
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "recipient_email@example.com"

def connect_to_database():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    return conn

def get_drugs():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM drugs")
            data = cursor.fetchall()
            return data
        except Exception as e:
            st.error(f"Error fetching drugs: {e}")
            return None
        finally:
            conn.close()
    else:
        st.error("Error connecting to database.")
        return None

def add_drug(drug_data):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO drugs (drug_name, manufacturer, manufactured_date, expiration_date, quantity, email_notification, sms_notification)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, drug_data)
            conn.commit()
            st.success("Drug added successfully!")
        except Exception as e:
            st.error(f"Error adding drug: {e}")
        finally:
            conn.close()
    else:
        st.error("Error connecting to database.")

def update_drug(drug_id, drug_data):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        try:
            sql = """UPDATE drugs SET drug_name = %s, manufacturer = %s, manufactured_date = %s, expiration_date = %s, quantity = %s, 
                       email_notification = %s, sms_notification = %s WHERE id = %s"""
            cursor.execute(sql, drug_data + (drug_id,))
            conn.commit()
            st.success("Drug updated successfully!")
        except Exception as e:
            st.error(f"Error updating drug: {e}")
        finally:
            conn.close()
    else:
        st.error("Error connecting to database.")

def delete_drug(drug_id):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM drugs WHERE id = %s"
            cursor.execute(sql, (drug_id,))
            conn.commit()
            st.success("Drug deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting drug: {e}")
        finally:
            conn.close()
    else:
        st.error("Error connecting to database.")

def send_email(subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, f"Subject: {subject}\n\n{body}")

def send_sms(message):
    # Replace with your SMS gateway implementation
    pass

# App title and header
st.title("Drugs Expiration Tracker by Appsorwebs Limited")
st.header("Monitor Your Drug Inventory")

# Get drugs from database
drugs = get_drugs()

# Convert data to DataFrame
df = pd.DataFrame(drugs, columns=["id", "drug_name", "manufacturer", "manufactured_date",
                                  "expiration_date", "quantity", "email_notification", "sms_notification"])

# Form to add new drugs
with st.form("Add Drug"):
    drug_name = st.text_input("Drug Name")
    manufacturer = st.text_input("Manufacturer")
    manufactured_date = st.date_input("Manufactured Date")
    expiration_date = st.date_input("Expiration Date")
    quantity = st.number_input("Quantity")
    email_notification = st.checkbox("Email Notification (Near Expiration)")
    sms_notification = st.checkbox("SMS Notification (Near Expiration)")
    submit_button = st.form_submit_button("Add")

    if submit_button:
        new_drug_data = (drug_name, manufacturer, manufactured_date, expiration_date,
                         quantity, email_notification, sms_notification)
        add_drug(new_drug_data)
        df = get_drugs()  # Refresh data after adding a drug

# Display drug list with expiration highlighting
st.subheader("Your Drug Inventory")
df["days_left"] = (pd.to_datetime(df["expiration_date"]) - pd.to_datetime(df["manufactured_date"])).dt.days
df["color"] = df["days_left"].apply(lambda days: "red" if days <= 30 else "orange" if days <= 90 else "green")
st.table(df.style.apply(lambda x: ["background-color: {}".format(x["color"])] * len(x), axis=1))

# Search and filtering
search_term = st.text_input("Search by drug name")
if search_term:
    df = df[df["drug_name"].str.contains(search_term, case=False)]

# Send notifications for drugs nearing expiration
for index, row in df.iterrows():
    if row["days_left"] <= 30:
        if row["email_notification"]:
            subject = "Drug Expiration Alert: " + row["drug_name"]
            body = f"Your drug {row['drug_name']} is nearing expiration. It has {row['days_left']} days left."
            send_email(subject, body)
        if row["sms_notification"]:
            message = f"Drug Expiration Alert: {row['drug_name']} has {row['days_left']} days left."
            send_sms(message)

# Footer
st.write("Designed by Appsorwebs Limited ([https://appsorwebs.com/](https://appsorwebs.com/))")