import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_teleconnect_data(num_records=10000, seed=42):
    """
    Generates a realistic synthetic customer dataset for TeleConnect with 10,000 records.
    Introduces controlled noise and data quality issues to simulate raw production data.
    """
    np.random.seed(seed)
    random.seed(seed)

    print(f"Generating {num_records} raw customer records for TeleConnect...")

    customer_ids = [f"TC-{10000 + i}" for i in range(num_records)]
    genders = np.random.choice(['Male', 'Female', 'male', 'Female ', 'MALE'], size=num_records, p=[0.45, 0.45, 0.04, 0.03, 0.03])
    ages = np.random.randint(18, 85, size=num_records)
    # Add a couple of age outliers
    outlier_idx = np.random.choice(num_records, size=5, replace=False)
    for idx in outlier_idx:
        ages[idx] = random.choice([120, 150, -5])

    senior_citizens = [1 if a >= 65 else 0 for a in ages]
    marital_statuses = np.random.choice(['Single', 'Married', ' single ', 'MARRIED'], size=num_records, p=[0.48, 0.46, 0.03, 0.03])
    dependents = np.random.choice(['Yes', 'No'], size=num_records, p=[0.30, 0.70])
    
    cities_states = [
        ('Austin', 'TX'), ('Seattle', 'WA'), ('Dallas', 'TX'), ('Chicago', 'IL'),
        ('Denver', 'CO'), ('Miami', 'FL'), ('New York', 'NY'), ('Los Angeles', 'CA'),
        ('Atlanta', 'GA'), ('Phoenix', 'AZ')
    ]
    city_choices = np.random.choice(len(cities_states), size=num_records)
    cities = [cities_states[i][0] for i in city_choices]
    states = [cities_states[i][1] for i in city_choices]

    # Subscriptions
    contract_types = np.random.choice(
        ['Month-to-month', 'One year', 'Two year', ' Month-to-month ', 'month-to-month', 'one year'],
        size=num_records,
        p=[0.50, 0.25, 0.18, 0.03, 0.02, 0.02]
    )
    subscription_plans = np.random.choice(['Basic', 'Standard', 'Premium'], size=num_records, p=[0.35, 0.45, 0.20])
    internet_services = np.random.choice(['DSL', 'Fiber optic', 'None', 'dsl', ' Fiber Optic'], size=num_records, p=[0.33, 0.43, 0.18, 0.03, 0.03])
    payment_methods = np.random.choice(
        ['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card', 'electronic check'],
        size=num_records,
        p=[0.32, 0.22, 0.22, 0.20, 0.04]
    )
    paperless_billings = np.random.choice(['Yes', 'No'], size=num_records, p=[0.60, 0.40])

    tenure_months = np.random.exponential(scale=24, size=num_records).astype(int)
    tenure_months = np.clip(tenure_months, 1, 72)

    # Base pricing based on plan & service
    base_prices = {'Basic': 25.0, 'Standard': 55.0, 'Premium': 85.0}
    service_add = {'DSL': 15.0, 'Fiber optic': 35.0, 'None': 0.0}

    monthly_charges = []
    for i in range(num_records):
        plan = subscription_plans[i]
        net_raw = str(internet_services[i]).strip().title()
        net = net_raw if net_raw in service_add else 'DSL'
        price = base_prices[plan] + service_add.get(net, 15.0) + np.random.normal(0, 5)
        monthly_charges.append(round(max(19.99, price), 2))
    
    monthly_charges = np.array(monthly_charges)
    # Inject a few charge outliers
    for idx in outlier_idx[:3]:
        monthly_charges[idx] = random.choice([-25.00, 1250.00])

    total_charges = np.round(monthly_charges * tenure_months + np.random.normal(0, 15, size=num_records), 2)
    total_charges = np.clip(total_charges, 0, None)

    discount_percentages = np.random.choice([0, 5, 10, 15, 20], size=num_records, p=[0.50, 0.20, 0.15, 0.10, 0.05])
    lifetime_values = np.round(total_charges * (1 - discount_percentages / 100.0) + np.random.normal(50, 20, size=num_records), 2)
    lifetime_values = np.clip(lifetime_values, 20, None)

    # Services
    phone_services = np.random.choice(['Yes', 'No'], size=num_records, p=[0.90, 0.10])
    multiple_lines = [
        'No phone service' if phone_services[i] == 'No' else np.random.choice(['Yes', 'No'], p=[0.45, 0.55])
        for i in range(num_records)
    ]
    streaming_services = np.random.choice(['Yes', 'No'], size=num_records, p=[0.48, 0.52])
    online_securities = np.random.choice(['Yes', 'No'], size=num_records, p=[0.30, 0.70])
    online_backups = np.random.choice(['Yes', 'No'], size=num_records, p=[0.35, 0.65])
    tech_supports = np.random.choice(['Yes', 'No'], size=num_records, p=[0.29, 0.71])
    device_protections = np.random.choice(['Yes', 'No'], size=num_records, p=[0.34, 0.66])

    # Engagement
    support_tickets = np.random.poisson(lam=1.8, size=num_records)
    complaints = np.random.poisson(lam=0.8, size=num_records)
    avg_usage_gb = np.random.gamma(shape=3.0, scale=80.0, size=num_records).round(1)
    satisfaction_scores = np.random.choice(range(1, 11), size=num_records, p=[0.08, 0.09, 0.10, 0.12, 0.15, 0.16, 0.14, 0.08, 0.05, 0.03])
    last_login_days = np.random.randint(1, 60, size=num_records)

    # Signup dates
    end_date = datetime(2024, 6, 30)
    signup_dates = [
        (end_date - timedelta(days=int(tenure_months[i] * 30.43) + random.randint(0, 20))).strftime('%Y-%m-%d')
        for i in range(num_records)
    ]

    # Calculate Realistic Churn Probability score
    churn_list = []
    churn_dates = []
    churn_reasons = []
    competitor_offers = []
    cancellation_channels = []

    possible_reasons = [
        'Competitor offered higher speeds',
        'Price too high',
        'Service dissatisfaction',
        'Customer moved',
        'Poor tech support',
        'Lack of features'
    ]
    possible_channels = ['Online Portal', 'Customer Service Call', 'In-Person Store', 'Email']

    for i in range(num_records):
        score = 0.02 # Baseline probability ~2%
        
        # Contract risk
        ct_clean = str(contract_types[i]).strip().lower()
        if 'month-to-month' in ct_clean:
            score += 0.16
        elif 'one year' in ct_clean:
            score += 0.02
        elif 'two year' in ct_clean:
            score -= 0.05
        
        # Tenure risk
        if tenure_months[i] <= 6:
            score += 0.15
        elif tenure_months[i] <= 12:
            score += 0.06
        elif tenure_months[i] > 36:
            score -= 0.10

        # Satisfaction risk
        if satisfaction_scores[i] <= 3:
            score += 0.25
        elif satisfaction_scores[i] <= 5:
            score += 0.10
        elif satisfaction_scores[i] >= 8:
            score -= 0.10

        # Support & Complaints
        if support_tickets[i] >= 4:
            score += 0.12
        if complaints[i] >= 2:
            score += 0.12
        
        # Fiber Optic & High Charges
        net_str = str(internet_services[i]).strip().lower()
        if 'fiber' in net_str:
            score += 0.05
        if monthly_charges[i] > 80.0:
            score += 0.05

        # Multi-services reduce churn
        services_count = sum([
            1 if phone_services[i] == 'Yes' else 0,
            1 if streaming_services[i] == 'Yes' else 0,
            1 if online_securities[i] == 'Yes' else 0,
            1 if tech_supports[i] == 'Yes' else 0
        ])
        if services_count >= 3:
            score -= 0.08

        # Competitor offer trigger
        has_comp_offer = 'Yes' if random.random() < (0.30 if score > 0.3 else 0.12) else 'No'
        if has_comp_offer == 'Yes':
            score += 0.12

        churn_prob = max(0.01, min(0.85, score))
        is_churned = random.random() < churn_prob

        if is_churned:
            churn_list.append('Yes')
            signup_dt = datetime.strptime(signup_dates[i], '%Y-%m-%d')
            c_date = signup_dt + timedelta(days=int(tenure_months[i] * 30))
            if c_date > end_date:
                c_date = end_date - timedelta(days=random.randint(1, 60))
            churn_dates.append(c_date.strftime('%Y-%m-%d'))
            
            if has_comp_offer == 'Yes' and random.random() < 0.6:
                churn_reasons.append('Competitor offered higher speeds')
            elif satisfaction_scores[i] <= 3:
                churn_reasons.append(random.choice(['Service dissatisfaction', 'Poor tech support']))
            elif monthly_charges[i] > 75:
                churn_reasons.append('Price too high')
            else:
                churn_reasons.append(random.choice(possible_reasons))

            competitor_offers.append(has_comp_offer)
            cancellation_channels.append(random.choice(possible_channels))
        else:
            churn_list.append('No')
            churn_dates.append(None)
            churn_reasons.append(None)
            competitor_offers.append(has_comp_offer)
            cancellation_channels.append(None)

    df = pd.DataFrame({
        'customer_id': customer_ids,
        'gender': genders,
        'age': ages,
        'senior_citizen': senior_citizens,
        'marital_status': marital_statuses,
        'dependents': dependents,
        'city': cities,
        'state': states,
        'signup_date': signup_dates,
        'tenure_months': tenure_months,
        'contract_type': contract_types,
        'subscription_plan': subscription_plans,
        'internet_service': internet_services,
        'payment_method': payment_methods,
        'paperless_billing': paperless_billings,
        'monthly_charges': monthly_charges,
        'total_charges': total_charges,
        'discount_percentage': discount_percentages,
        'lifetime_value': lifetime_values,
        'phone_service': phone_services,
        'multiple_lines': multiple_lines,
        'streaming_service': streaming_services,
        'online_security': online_securities,
        'online_backup': online_backups,
        'tech_support': tech_supports,
        'device_protection': device_protections,
        'support_tickets': support_tickets,
        'complaints': complaints,
        'avg_monthly_usage_gb': avg_usage_gb,
        'satisfaction_score': satisfaction_scores,
        'last_login_days_ago': last_login_days,
        'churn': churn_list,
        'churn_date': churn_dates,
        'churn_reason': churn_reasons,
        'competitor_offer': competitor_offers,
        'cancellation_channel': cancellation_channels
    })

    # Introduce intentional missing values (~1.5% - 2%)
    mask_tot = np.random.choice([True, False], size=num_records, p=[0.015, 0.985])
    df.loc[mask_tot, 'total_charges'] = np.nan

    mask_sat = np.random.choice([True, False], size=num_records, p=[0.02, 0.98])
    df.loc[mask_sat, 'satisfaction_score'] = np.nan

    mask_net = np.random.choice([True, False], size=num_records, p=[0.01, 0.99])
    df.loc[mask_net, 'internet_service'] = np.nan

    # Introduce 20 duplicate rows
    dupes = df.sample(n=20, random_state=seed)
    df = pd.concat([df, dupes], ignore_index=True)

    # Ensure target output directory exists
    os.makedirs('data/raw', exist_ok=True)
    raw_path = 'data/raw/customers.csv'
    df.to_csv(raw_path, index=False)
    print(f"Successfully generated {len(df)} raw rows (including 20 duplicates) -> {raw_path}")
    return df

if __name__ == '__main__':
    generate_teleconnect_data()
