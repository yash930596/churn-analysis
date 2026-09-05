import os
import pandas as pd
import numpy as np

def clean_teleconnect_data(raw_path='data/raw/customers.csv', output_path='data/processed/customers_clean.csv'):
    """
    Data Cleaning & Feature Engineering Pipeline for TeleConnect Customer Dataset.
    Identifies, audits, cleans data quality issues, and derives analytical variables.
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run src/data_generation.py first.")

    print(f"Loading raw dataset from {raw_path}...")
    df_raw = pd.read_csv(raw_path)
    initial_rows = len(df_raw)
    print(f"Initial raw record count: {initial_rows}")

    df = df_raw.copy()

    # 1. Deduplication
    dupes_count = df.duplicated(subset=['customer_id']).sum()
    print(f"Found {dupes_count} duplicate customer IDs. Removing duplicates...")
    df = df.drop_duplicates(subset=['customer_id'], keep='first')

    # 2. String Standardization & Whitespace Trimming
    string_cols = [
        'gender', 'marital_status', 'dependents', 'city', 'state',
        'contract_type', 'subscription_plan', 'internet_service',
        'payment_method', 'paperless_billing', 'phone_service',
        'multiple_lines', 'streaming_service', 'online_security',
        'online_backup', 'tech_support', 'device_protection',
        'churn', 'churn_reason', 'competitor_offer', 'cancellation_channel'
    ]

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Map standardized categorical values
    gender_map = {'Male': 'Male', 'male': 'Male', 'MALE': 'Male', 'Female': 'Female', 'Female ': 'Female', 'nan': 'Female'}
    df['gender'] = df['gender'].map(gender_map).fillna('Female')

    marital_map = {'Single': 'Single', 'single': 'Single', 'Married': 'Married', 'MARRIED': 'Married'}
    df['marital_status'] = df['marital_status'].map(marital_map).fillna('Single')

    contract_map = {
        'Month-to-month': 'Month-to-month', 'month-to-month': 'Month-to-month',
        'One year': 'One year', 'one year': 'One year',
        'Two year': 'Two year', 'two year': 'Two year'
    }
    df['contract_type'] = df['contract_type'].map(contract_map).fillna('Month-to-month')

    net_map = {'DSL': 'DSL', 'dsl': 'DSL', 'Fiber Optic': 'Fiber optic', 'Fiber optic': 'Fiber optic', 'None': 'None'}
    df['internet_service'] = df['internet_service'].replace({'nan': np.nan}).map(net_map)

    pay_map = {
        'Electronic check': 'Electronic check', 'electronic check': 'Electronic check',
        'Mailed check': 'Mailed check', 'Bank transfer': 'Bank transfer',
        'Credit card': 'Credit card'
    }
    df['payment_method'] = df['payment_method'].map(pay_map).fillna('Electronic check')

    # 3. Handle Missing Values
    # Missing internet_service -> default to 'DSL'
    df['internet_service'] = df['internet_service'].fillna('DSL')

    # 4. Handle Outliers & Invalid Values in Numeric Fields
    # Age outlier handling (keep 18-85, replace invalid with median age 45)
    invalid_age_mask = (df['age'] < 18) | (df['age'] > 85)
    df.loc[invalid_age_mask, 'age'] = 45
    df['senior_citizen'] = (df['age'] >= 65).astype(int)

    # Monthly charges outliers (< $18 or > $150 -> replace with realistic median $65.0)
    invalid_charge_mask = (df['monthly_charges'] < 18.0) | (df['monthly_charges'] > 150.0)
    df.loc[invalid_charge_mask, 'monthly_charges'] = 65.00

    # Impute missing total_charges with monthly_charges * tenure_months
    missing_tot_mask = df['total_charges'].isna()
    df.loc[missing_tot_mask, 'total_charges'] = np.round(df.loc[missing_tot_mask, 'monthly_charges'] * df.loc[missing_tot_mask, 'tenure_months'], 2)

    # Impute missing satisfaction_score with median per contract_type
    df['satisfaction_score'] = df.groupby('contract_type')['satisfaction_score'].transform(lambda x: x.fillna(x.median())).round().astype(int)

    # Re-calculate lifetime value logically
    df['lifetime_value'] = np.round(df['total_charges'] * (1 - df['discount_percentage'] / 100.0), 2)

    # Clean active vs churned consistency
    active_mask = (df['churn'] == 'No')
    df.loc[active_mask, 'churn_date'] = np.nan
    df.loc[active_mask, 'churn_reason'] = 'None'
    df.loc[active_mask, 'cancellation_channel'] = 'None'

    churned_mask = (df['churn'] == 'Yes')
    df.loc[churned_mask & (df['churn_reason'] == 'nan'), 'churn_reason'] = 'Service dissatisfaction'
    df.loc[churned_mask & (df['cancellation_channel'] == 'nan'), 'cancellation_channel'] = 'Customer Service Call'

    # 5. DERIVED VARIABLES
    # Age Group
    age_bins = [0, 24, 34, 44, 54, 64, 120]
    age_labels = ['Under 25', '25–34', '35–44', '45–54', '55–64', '65+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

    # Tenure Group
    tenure_bins = [-1, 6, 12, 24, 48, 100]
    tenure_labels = ['0–6 Months', '7–12 Months', '13–24 Months', '25–48 Months', '49+ Months']
    df['tenure_group'] = pd.cut(df['tenure_months'], bins=tenure_bins, labels=tenure_labels)

    # Monthly Charge Group
    charge_bins = [0, 40, 80, 500]
    charge_labels = ['Low', 'Medium', 'High']
    df['monthly_charge_group'] = pd.cut(df['monthly_charges'], bins=charge_bins, labels=charge_labels)

    # Support Ticket Group
    ticket_bins = [-1, 0, 2, 5, 100]
    ticket_labels = ['0', '1–2', '3–5', '6+']
    df['support_ticket_group'] = pd.cut(df['support_tickets'], bins=ticket_bins, labels=ticket_labels)

    # Satisfaction Group
    sat_bins = [0, 4, 7, 10]
    sat_labels = ['Low', 'Medium', 'High']
    df['satisfaction_group'] = pd.cut(df['satisfaction_score'], bins=sat_bins, labels=sat_labels)

    # Customer Status
    df['customer_status'] = df['churn'].map({'Yes': 'Churned', 'No': 'Active'})

    # Estimated Annual Revenue
    df['estimated_annual_revenue'] = np.round(df['monthly_charges'] * 12, 2)

    # Estimated Revenue at Risk
    df['estimated_revenue_at_risk'] = np.where(df['customer_status'] == 'Churned', df['estimated_annual_revenue'], 0.0)

    # Export Clean Dataset
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv(output_path, index=False)

    print("\n--- DATA CLEANING AUDIT REPORT ---")
    print(f"Original Records: {initial_rows}")
    print(f"Cleaned Records: {len(df)}")
    print(f"Duplicates Removed: {dupes_count}")
    print(f"Null Values Remaining: {df.isna().sum().sum()}")
    print(f"Active Customers: {(df['customer_status'] == 'Active').sum()}")
    print(f"Churned Customers: {(df['customer_status'] == 'Churned').sum()}")
    print(f"Overall Churn Rate: {((df['customer_status'] == 'Churned').mean() * 100):.2f}%")
    print(f"Cleaned dataset saved to: {output_path}")

    return df

if __name__ == '__main__':
    clean_teleconnect_data()
