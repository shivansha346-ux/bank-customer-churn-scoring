# 🏦 Predictive Modeling and Risk Scoring for Bank Customer Churn

## 📊 Project Overview
This project delivers an enterprise-grade **Proactive Churn Intelligence System**. Moving away from traditional reactive analytics, this system evaluates customer behavior, product density, and financial interaction constraints to assign a quantitative risk score (0-100%) to every retail banking customer before they churn. 

This is a complete **End-to-End Machine Learning and Analytics project** featuring a SQL Database Core, Advanced ML Predictive Models, an Interactive Streamlit Web Application, and an Executive Power BI Dashboard.

---

## 📁 Repository Architecture & Deliverables
* **`churn_predictive_modeling.ipynb`** (Formerly *Untitled3.ipynb*): Complete machine learning pipeline including Exploratory Data Analysis (EDA), model training (Logistic Regression, Random Forest, XGBoost), evaluation, and model explainability.
* **`app.py`**: A live **Streamlit Web Application** serving as an interactive Customer Churn Risk Calculator and What-If scenario simulator for relationship managers.
* **`Bank Customer Churn Predictive Scoring Dashboard.pbix`**: An executive-level **Power BI Dashboard** providing high-level macro insights for bank management.

---

## 🛠️ Data Pipeline & Architecture
The analytical methodology follows a structured enterprise pipeline to ensure data cleanliness and algorithmic stability:

### 1. Data Preprocessing & Scrubbing
* Eliminated rows with missing/null values in Balance and EstimatedSalary.
* Dropped non-informative identifiers (`CustomerId`, `Surname`) to remove compliance risks and model bias.

### 2. One-Hot Encoding
* Transformed categorical features (`Geography`, `Gender`) into standardized binary flags (0/1) using conditional `CASE WHEN` logic in SQL and `OneHotEncoder` in Python.

### 3. Robust Feature Scaling (Min-Max)
* Scaled wide-ranged financial features (`CreditScore`, `Age`, `Balance`, `EstimatedSalary`) strictly between 0 and 1.
* Implemented explicit `FLOAT` data-type casting to prevent arithmetic overflow and division-by-zero exceptions (`NULLIF`).

### 4. Feature Engineering (Interaction Terms)
* **Balance_to_Salary_Ratio:** Financial stability relative to income.
* **Product_Density:** Product adoption speed adjusted against tenure.
* **Engagement_Product_Interaction:** Cross-matrix of active status and product count.
* **Age_Tenure_Interaction:** Measures long-term tenure loyalty normalized against age brackets.

---

## 🎯 Statistical Risk Scoring Matrix (SQL Baseline)
To create an explainable and transparent model for banking compliance, risk weights were mathematically calibrated based on core operational drivers:


| Risk Driver | Condition | Risk Points Assigned |
| :--- | :--- | :--- |
| **Age Bracket** | Age > 45 | 35 Points |
| **Age Bracket** | Age 35 - 45 | 15 Points |
| **Engagement Link** | Inactive Member (`IsActiveMember = 0`) | 25 Points |
| **Product Fatigue** | Multi-Product Portfolio ($\ge$ 3 Products) | 20 Points |
| **Financial Exposure** | High Asset Balance (> $100,000) | 20 Points |

---

## 🖥️ How to Run the Streamlit Web Application
To run the interactive customer risk calculator locally:
1. **Install dependencies:**
   ```bash
   pip install streamlit pandas numpy scikit-learn xgboost
   ```
2. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

---

## 📈 Corporate Insights & Findings
* **Critical Age Threshold:** Customers over 45 hold the maximum risk weight. The current product architecture fails to address the wealth-preservation needs of mid-to-late career demographics.
* **The Inactivity Trap:** Inactive status is highly correlated with swift customer departure, highlighting gaps in digital and mobile banking engagement.
* **Product Complexity Friction:** Counter-intuitively, holding 3 or more products accelerates churn rather than locking loyalty. This flags broken multi-product customer support or hidden pricing friction.

---

## 🔴 Executive Strategic Recommendations
* **🛑 High Churn Risk (Score $\ge$ 70) — Immediate Mitigation:** Assign proactive relationship managers, offer custom high-yield deposit rates, and trigger automated fee waivers.
* **⚠️ Medium Churn Risk (Score 40-69) — Targeted Retention:** Deploy cashback and value-driven reward points tailored to inactive users; streamline account bundles.
* **🟢 Low Churn Risk (Score < 40) — Standard Optimization:** Safe target group for organic upselling of long-term investments and premium credit cards.

---

## 💻 Core SQL Pipeline Implementation Script
```sql
-- ========================================================================= 
-- 0. पुरानी प्रोसेसिंग टेबल्स को हटाना (ताकि कोई पुराना एरर न आए) 
-- ========================================================================= 
IF OBJECT_ID('dbo.Prepared_Bank_Data', 'U') IS NOT NULL DROP TABLE Prepared_Bank_Data; 
IF OBJECT_ID('dbo.Scaled_Bank_Data', 'U') IS NOT NULL DROP TABLE Scaled_Bank_Data; 
IF OBJECT_ID('dbo.Final_Prepared_Data', 'U') IS NOT NULL DROP TABLE Final_Prepared_Data; 
IF OBJECT_ID('dbo.Churn_Risk_Scoring_Report', 'U') IS NOT NULL DROP TABLE Churn_Risk_Scoring_Report;

-- ========================================================================= 
-- 1. मिसिंग वैल्यूज़ हटाना (Handle Missing Values) 
-- ========================================================================= 
DELETE FROM [European_Bank] WHERE Balance IS NULL OR EstimatedSalary IS NULL;

-- ========================================================================= 
-- 2. नॉन-इंफॉर्मेटिव फीचर्स हटाना (Remove Non-Informative Features) 
-- ========================================================================= 
IF COL_LENGTH('[European_Bank]', 'CustomerId') IS NOT NULL ALTER TABLE [European_Bank] DROP COLUMN CustomerId;
IF COL_LENGTH('[European_Bank]', 'Surname') IS NOT NULL ALTER TABLE [European_Bank] DROP COLUMN Surname;

-- ========================================================================= 
-- 3. कैटेगोरिकल वेरिएबल्स को एनकोड करना (One-Hot Encoding) 
-- ========================================================================= 
SELECT Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, CreditScore, Exited, 
CASE WHEN Geography = 'Germany' THEN 1 ELSE 0 END AS Geography_Germany, 
CASE WHEN Geography = 'Spain' THEN 1 ELSE 0 END AS Geography_Spain, 
CASE WHEN Gender = 'Male' THEN 1 ELSE 0 END AS Gender_Male 
INTO Prepared_Bank_Data FROM [European_Bank];

-- ========================================================================= 
-- 4. न्यूमेरिकल फीचर्स को स्केल करना (Min-Max Scaling) 
-- ========================================================================= 
WITH MinMax AS ( 
    SELECT CAST(MIN(CreditScore) AS FLOAT) as min_cr, CAST(MAX(CreditScore) AS FLOAT) as max_cr, 
           CAST(MIN(Age) AS FLOAT) as min_age, CAST(MAX(Age) AS FLOAT) as max_age, 
           CAST(MIN(Balance) AS FLOAT) as min_bal, CAST(MAX(Balance) AS FLOAT) as max_bal, 
           CAST(MIN(EstimatedSalary) AS FLOAT) as min_sal, CAST(MAX(EstimatedSalary) AS FLOAT) as max_sal 
    FROM Prepared_Bank_Data 
) 
SELECT p.*, 
CAST((CAST(p.CreditScore AS FLOAT) - m.min_cr) / NULLIF(m.max_cr - m.min_cr, 0) AS DECIMAL(5,4)) AS Scaled_CreditScore, 
CAST((CAST(p.Age AS FLOAT) - m.min_age) / NULLIF(m.max_age - m.min_age, 0) AS DECIMAL(5,4)) AS Scaled_Age, 
CAST((CAST(p.Balance AS FLOAT) - m.min_bal) / NULLIF(m.max_bal - m.min_bal, 0) AS DECIMAL(5,4)) AS Scaled_Balance, 
CAST((CAST(p.EstimatedSalary AS FLOAT) - m.min_sal) / NULLIF(m.max_sal - m.min_sal, 0) AS DECIMAL(5,4)) AS Scaled_Salary 
INTO Scaled_Bank_Data FROM Prepared_Bank_Data p, MinMax m;

-- ========================================================================= 
-- 5. नए फीचर्स बनाना (Feature Engineering - Safe from TinyInt Overflow) 
-- ========================================================================= 
SELECT *, 
CAST(Balance / (EstimatedSalary + 1) AS DECIMAL(10,4)) AS Balance_to_Salary_Ratio, 
CAST(CAST(NumOfProducts AS FLOAT) / (CAST(Tenure AS FLOAT) + 1.0) AS DECIMAL(10,4)) AS Product_Density, 
(CAST(IsActiveMember AS INT) * CAST(NumOfProducts AS INT)) AS Engagement_Product_Interaction, 
(CAST(Age AS INT) * CAST(Tenure AS INT)) AS Age_Tenure_Interaction 
INTO Final_Prepared_Data FROM Scaled_Bank_Data;

-- ========================================================================= 
-- 6. Quantitative Churn Risk Scoring (रिस्क स्कोर और प्रोबेबिलिटी) 
-- ========================================================================= 
SELECT *, 
( 
    CASE WHEN Age > 45 THEN 35 WHEN Age BETWEEN 35 AND 45 THEN 15 ELSE 5 END + 
    CASE WHEN IsActiveMember = 0 THEN 25 ELSE 0 END + 
    CASE WHEN NumOfProducts >= 3 THEN 20 ELSE 5 END + 
    CASE WHEN Balance > 100000 THEN 20 ELSE 5 END 
) AS Churn_Probability_Score 
INTO Churn_Risk_Scoring_Report FROM Final_Prepared_Data;

-- ========================================================================= 
-- फाइनल आउटपुट: रिस्क सेगमेंट्स (High, Medium, Low Risk) की रिपोर्ट देखना 
-- ========================================================================= 
SELECT TOP 20 Age, Balance, Balance_to_Salary_Ratio, Scaled_CreditScore, Churn_Probability_Score,
CASE 
    WHEN Churn_Probability_Score >= 70 THEN 'High Risk'
    WHEN Churn_Probability_Score BETWEEN 40 AND 69 THEN 'Medium Risk'
    ELSE 'Low Risk'
END AS Risk_Segment
FROM Churn_Risk_Scoring_Report;
```

