import os
import json
import pandas as pd
import numpy as np

def run_churn_analysis(clean_path='data/processed/customers_clean.csv', output_report_dir='outputs/reports'):
    """
    Performs comprehensive statistical, segmentation, and revenue-at-risk analysis.
    Outputs metrics to outputs/reports/churn_summary_metrics.json.
    """
    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {clean_path}. Run src/data_cleaning.py first.")

    os.makedirs(output_report_dir, exist_ok=True)
    df = pd.read_csv(clean_path)

    total_customers = int(len(df))
    churned_customers = int((df['customer_status'] == 'Churned').sum())
    active_customers = int((df['customer_status'] == 'Active').sum())
    churn_rate = float(np.round((churned_customers / total_customers) * 100, 2))

    avg_monthly_charges = float(np.round(df['monthly_charges'].mean(), 2))
    avg_tenure = float(np.round(df['tenure_months'].mean(), 2))
    
    total_monthly_revenue = float(np.round(df['monthly_charges'].sum(), 2))
    total_annualized_revenue = float(np.round(total_monthly_revenue * 12, 2))
    
    revenue_at_risk = float(np.round(df[df['customer_status'] == 'Churned']['estimated_annual_revenue'].sum(), 2))
    pct_revenue_at_risk = float(np.round((revenue_at_risk / total_annualized_revenue) * 100, 2))

    # Segment metrics breakdown helper
    def get_segment_stats(col):
        grouped = df.groupby(col, observed=False).agg(
            total_cust=('customer_id', 'count'),
            churned_cust=('churn', lambda x: int((x == 'Yes').sum())),
            churn_rate=('churn', lambda x: float(round((x == 'Yes').mean() * 100, 2))),
            avg_monthly_charge=('monthly_charges', lambda x: float(round(x.mean(), 2))),
            annual_rev_at_risk=('estimated_revenue_at_risk', lambda x: float(round(x.sum(), 2)))
        ).reset_index()
        grouped[col] = grouped[col].astype(str)
        records = grouped.to_dict(orient='records')
        for r in records:
            r['total_cust'] = int(r['total_cust'])
            r['churned_cust'] = int(r['churned_cust'])
        return records

    by_contract = get_segment_stats('contract_type')
    by_tenure = get_segment_stats('tenure_group')
    by_plan = get_segment_stats('subscription_plan')
    by_payment = get_segment_stats('payment_method')
    by_internet = get_segment_stats('internet_service')
    by_tickets = get_segment_stats('support_ticket_group')
    by_satisfaction = get_segment_stats('satisfaction_group')

    # Customer Segmentation (4 Matrix Quadrants)
    median_charge = df['monthly_charges'].median()
    df['value_tier'] = np.where(df['monthly_charges'] >= median_charge, 'High-Value', 'Low-Value')
    
    # Risk definition: Churned OR (Month-to-month AND support_tickets >= 3)
    high_risk_cond = (df['customer_status'] == 'Churned') | ((df['contract_type'] == 'Month-to-month') & (df['support_tickets'] >= 3))
    df['risk_tier'] = np.where(high_risk_cond, 'High-Risk', 'Low-Risk')

    seg_df = df.groupby(['value_tier', 'risk_tier'], observed=False).agg(
        customers=('customer_id', 'count'),
        churned=('churn', lambda x: int((x == 'Yes').sum())),
        churn_rate=('churn', lambda x: float(round((x == 'Yes').mean() * 100, 2))),
        annual_revenue=('estimated_annual_revenue', lambda x: float(round(x.sum(), 2))),
        revenue_at_risk=('estimated_revenue_at_risk', lambda x: float(round(x.sum(), 2)))
    ).reset_index()
    seg_df['value_tier'] = seg_df['value_tier'].astype(str)
    seg_df['risk_tier'] = seg_df['risk_tier'].astype(str)
    segment_matrix = seg_df.to_dict(orient='records')
    for r in segment_matrix:
        r['customers'] = int(r['customers'])
        r['churned'] = int(r['churned'])

    # High-Risk Customer Combo Profile Analysis
    combo_condition = (
        (df['contract_type'] == 'Month-to-month') &
        (df['tenure_months'] <= 12) &
        (df['satisfaction_score'] <= 4)
    )
    combo_total = int(combo_condition.sum())
    combo_churned = int((combo_condition & (df['customer_status'] == 'Churned')).sum())
    combo_churn_rate = float(np.round((combo_churned / combo_total * 100) if combo_total > 0 else 0, 2))
    combo_rev_risk = float(np.round(df[combo_condition & (df['customer_status'] == 'Churned')]['estimated_annual_revenue'].sum(), 2))

    summary_metrics = {
        'kpis': {
            'total_customers': total_customers,
            'churned_customers': churned_customers,
            'active_customers': active_customers,
            'churn_rate_pct': churn_rate,
            'avg_monthly_charges': avg_monthly_charges,
            'avg_tenure_months': avg_tenure,
            'total_monthly_revenue': total_monthly_revenue,
            'total_annualized_revenue': total_annualized_revenue,
            'annualized_revenue_at_risk': revenue_at_risk,
            'pct_revenue_at_risk': pct_revenue_at_risk
        },
        'by_contract': by_contract,
        'by_tenure': by_tenure,
        'by_plan': by_plan,
        'by_payment': by_payment,
        'by_internet': by_internet,
        'by_tickets': by_tickets,
        'by_satisfaction': by_satisfaction,
        'segment_matrix': segment_matrix,
        'high_risk_profile_vulnerability': {
            'criteria': 'Month-to-month contract + Tenure <= 12 mos + Satisfaction <= 4',
            'matching_customers': combo_total,
            'churned_customers': combo_churned,
            'churn_rate_pct': combo_churn_rate,
            'annualized_revenue_at_risk': combo_rev_risk
        }
    }

    report_path = os.path.join(output_report_dir, 'churn_summary_metrics.json')
    with open(report_path, 'w') as f:
        json.dump(summary_metrics, f, indent=4)

    print("\n========================================================")
    print("         TELECONNECT CHURN ANALYSIS SUMMARY             ")
    print("========================================================")
    print(f"Total Customers:               {total_customers:,}")
    print(f"Active Customers:              {active_customers:,}")
    print(f"Churned Customers:             {churned_customers:,}")
    print(f"Overall Churn Rate:            {churn_rate}%")
    print(f"Average Monthly Charge:        ${avg_monthly_charges:,.2f}")
    print(f"Average Customer Tenure:       {avg_tenure} months")
    print(f"Total Monthly Revenue:         ${total_monthly_revenue:,.2f}")
    print(f"Total Annualized Revenue:      ${total_annualized_revenue:,.2f}")
    print(f"Estimated Annual Rev at Risk:  ${revenue_at_risk:,.2f} ({pct_revenue_at_risk}%)")
    print("========================================================")
    print(f"High-Risk Profile Segment Churn Rate: {combo_churn_rate}% ({combo_churned}/{combo_total} customers)")
    print(f"Saved summary metrics JSON to: {report_path}")

    return summary_metrics

if __name__ == '__main__':
    run_churn_analysis()
