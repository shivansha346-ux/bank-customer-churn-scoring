import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Model aur Features load karna
import os
model_path = os.path.join(os.path.dirname(__file__), 'xgb_churn_model.pkl')
model = joblib.load(model_path)
model_features = joblib.load(os.path.join(os.path.dirname(__file__), 'model_features.pkl'))

st.title("🏦 Bank Customer Churn - Predictive Scoring System")
st.subheader("European Central Bank (ECB) - Government Stakeholder Dashboard")
st.write("Adjust customer details below to calculate real-time Churn Risk Probability.")

# दो कॉलम का लेआउट बनाना
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Customer Age", 18, 100, 35)
    credit_score = st.slider("Credit Score", 300, 850, 600)
    tenure = st.slider("Tenure (Years with Bank)", 0, 10, 5)
    num_products = st.slider("Number of Products", 1, 4, 1)

with col2:
    balance = st.number_input("Account Balance ($)", min_value=0.0, value=50000.0)
    salary = st.number_input("Estimated Annual Salary ($)", min_value=0.0, value=75000.0)
    is_active = st.selectbox("Is Active Member?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    has_card = st.selectbox("Has Credit Card?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

# फ़ीचर इंजीनियरिंग की लाइव कैलकुलेशन
balance_salary_ratio = balance / (salary + 1)
product_density = num_products / (tenure + 1)
age_tenure_interaction = age * tenure

# वन-हॉट एनकोडिंग के डिफ़ॉल्ट मान
geography_germany = 0
geography_spain = 0
gender_male = 1

# इनपुट्स को एक DataFrame में समेटना
input_data = pd.DataFrame([{
    'Age': age, 'Tenure': tenure, 'Balance': balance, 'NumOfProducts': num_products,
    'HasCrCard': has_card, 'IsActiveMember': is_active, 'EstimatedSalary': salary,
    'CreditScore': credit_score, 'Geography_Germany': geography_germany,
    'Geography_Spain': geography_spain, 'Gender_Male': gender_male,
    'BalanceToSalaryRatio': balance_salary_ratio, 'ProductDensity': product_density,
    'AgeTenureInteraction': age_tenure_interaction
}])

# यह सुनिश्चित करना कि कॉलम्स का क्रम मॉडल के मुताबिक हो
input_data = input_data[model_features]

# लाइव प्रेडिक्शन बटन
if st.button("Calculate Churn Risk Score"):
    prob = model.predict_proba(input_data)[:, 1]
    # Extracting the single probability value safely from the model array
if isinstance(prob, (list, np.ndarray)):
    risk_score = float(prob[0]) * 100
else:
    risk_score = float(prob) * 100
risk_score = int(risk_score)
    st.metric(label="📊 Real-Time ML Risk Score", value=f"{risk_score} / 100")
    if risk_score >= 61:
        st.error("🚨 HIGH RISK ZONE: Customer is highly likely to churn. Immediate retention action needed.")
    elif risk_score >= 31:
        st.warning("⚠️ MEDIUM RISK ZONE: Customer shows signs of disengagement. Send personalized offers.")
    else:
        st.success("✅ LOW RISK ZONE: Customer is stable and loyal.")
