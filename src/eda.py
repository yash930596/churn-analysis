import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set global aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

PRIMARY_COLOR = '#1E3A8A'  # Deep Navy Blue
ACCENT_COLOR = '#EF4444'   # Crimson Red (Churn)
ACTIVE_COLOR = '#10B981'   # Emerald Green (Active)
PALETTE = ['#10B981', '#EF4444']

def generate_eda_charts(clean_path='data/processed/customers_clean.csv', output_dir='outputs/charts'):
    """
    Generates 10 publication-quality charts for Exploratory Data Analysis (EDA)
    and saves them to outputs/charts/.
    """
    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {clean_path}. Run src/data_cleaning.py first.")

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(clean_path)
    print(f"Loaded {len(df)} records from {clean_path} for EDA visual generation.")

    # 1. Overall Churn Distribution (Donut Chart)
    fig, ax = plt.subplots(figsize=(7, 6))
    churn_counts = df['customer_status'].value_counts()
    colors = [ACTIVE_COLOR, ACCENT_COLOR]
    wedges, texts, autotexts = ax.pie(
        churn_counts, labels=churn_counts.index, autopct='%1.1f%%',
        startangle=90, colors=colors, explode=(0, 0.05),
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    plt.setp(autotexts, size=12, weight="bold", color="white")
    plt.setp(texts, size=12, weight="bold")
    ax.set_title('TeleConnect Overall Customer Status (Active vs Churned)', fontsize=14, pad=20, weight='bold', color=PRIMARY_COLOR)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'overall_churn_distribution.png'), dpi=300)
    plt.close()

    # Helper function for churn rate bar charts
    def plot_churn_rate_by_cat(column, title, filename, xlabel, order=None):
        fig, ax1 = plt.subplots(figsize=(8, 5))
        stats = df.groupby(column)['churn'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
        counts = df.groupby(column)['customer_id'].count().reset_index()
        merged = pd.merge(stats, counts, on=column)
        
        if order:
            merged[column] = pd.Categorical(merged[column], categories=order, ordered=True)
            merged = merged.sort_values(column)

        bars = ax1.bar(merged[column].astype(str), merged['churn'], color=PRIMARY_COLOR, width=0.55, alpha=0.9)
        ax1.set_ylabel('Churn Rate (%)', fontsize=11, weight='bold', color=PRIMARY_COLOR)
        ax1.set_xlabel(xlabel, fontsize=11, weight='bold')
        ax1.set_title(title, fontsize=13, weight='bold', pad=15, color=PRIMARY_COLOR)
        ax1.set_ylim(0, max(merged['churn']) * 1.25)

        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}%',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=10, weight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=300)
        plt.close()

    # 2. Churn by Contract Type
    plot_churn_rate_by_cat(
        'contract_type', 'Churn Rate by Contract Type',
        'churn_by_contract_type.png', 'Contract Type',
        order=['Month-to-month', 'One year', 'Two year']
    )

    # 3. Churn by Tenure Group
    plot_churn_rate_by_cat(
        'tenure_group', 'Churn Rate by Customer Tenure Group',
        'churn_by_tenure_group.png', 'Tenure Group',
        order=['0–6 Months', '7–12 Months', '13–24 Months', '25–48 Months', '49+ Months']
    )

    # 4. Churn by Subscription Plan
    plot_churn_rate_by_cat(
        'subscription_plan', 'Churn Rate by Subscription Plan Tier',
        'churn_by_subscription_plan.png', 'Subscription Plan',
        order=['Basic', 'Standard', 'Premium']
    )

    # 5. Churn by Payment Method
    plot_churn_rate_by_cat(
        'payment_method', 'Churn Rate by Payment Method',
        'churn_by_payment_method.png', 'Payment Method'
    )

    # 6. Churn by Satisfaction Group
    plot_churn_rate_by_cat(
        'satisfaction_group', 'Churn Rate by Satisfaction Tier',
        'churn_by_satisfaction_group.png', 'Satisfaction Group',
        order=['Low', 'Medium', 'High']
    )

    # 7. Churn by Support Ticket Group
    plot_churn_rate_by_cat(
        'support_ticket_group', 'Churn Rate by Support Tickets Filed',
        'churn_by_support_tickets.png', 'Support Ticket Count Group',
        order=['0', '1–2', '3–5', '6+']
    )

    # 8. Churn by Monthly Charges (KDE Distribution)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.kdeplot(data=df[df['customer_status']=='Active']['monthly_charges'], ax=ax, color=ACTIVE_COLOR, fill=True, label='Active', alpha=0.4)
    sns.kdeplot(data=df[df['customer_status']=='Churned']['monthly_charges'], ax=ax, color=ACCENT_COLOR, fill=True, label='Churned', alpha=0.4)
    ax.set_title('Monthly Charge Distribution by Customer Status', fontsize=13, weight='bold', pad=15, color=PRIMARY_COLOR)
    ax.set_xlabel('Monthly Charges ($)', fontsize=11, weight='bold')
    ax.set_ylabel('Density', fontsize=11, weight='bold')
    ax.legend(title='Status', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'churn_by_monthly_charges.png'), dpi=300)
    plt.close()

    # 9. Churn by Age Group
    plot_churn_rate_by_cat(
        'age_group', 'Churn Rate by Age Group',
        'churn_by_age_group.png', 'Age Group',
        order=['Under 25', '25–34', '35–44', '45–54', '55–64', '65+']
    )

    # 10. Top Churn Reasons
    fig, ax = plt.subplots(figsize=(9, 5))
    churned_df = df[df['customer_status'] == 'Churned']
    reasons = churned_df['churn_reason'].value_counts()
    
    bars = ax.barh(reasons.index[::-1], reasons.values[::-1], color=ACCENT_COLOR, height=0.6, alpha=0.85)
    ax.set_title('Top Primary Reasons for Customer Cancellation', fontsize=13, weight='bold', pad=15, color=PRIMARY_COLOR)
    ax.set_xlabel('Number of Churned Customers', fontsize=11, weight='bold')
    
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:,}',
                     xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0),
                     textcoords="offset points",
                     ha='left', va='center', fontsize=10, weight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_churn_reasons.png'), dpi=300)
    plt.close()

    print(f"Successfully generated all 10 EDA charts in {output_dir}/")

if __name__ == '__main__':
    generate_eda_charts()
