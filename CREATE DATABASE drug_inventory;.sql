CREATE TABLE drugs (
    id SERIAL PRIMARY KEY,
    drug_name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    manufactured_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    email_notification BOOLEAN DEFAULT FALSE,
    sms_notification BOOLEAN DEFAULT FALSE
);