# TeleConnect Churn Project — Interview Preparation Guide (20 Q&As)

This document prepares junior and mid-level Data Analysts to confidently discuss this project during job interviews.

---

### Q1: Why did you choose customer churn for this portfolio project?
**Sample Answer:**  
Customer churn is one of the most critical metrics for subscription-based businesses like telecommunications. Retaining existing customers is far more cost-effective than acquiring new ones. I chose churn analysis because it directly impacts recurring revenue, allows me to solve a realistic business problem, and showcases full-stack data capabilities—from Python data cleaning and SQL analytics to Power BI visualization and strategic business recommendations.

---

### Q2: How did you calculate the overall churn rate?
**Sample Answer:**  
In both Python and SQL, churn rate is calculated as total churned customers divided by total customer count, expressed as a percentage:
$$\text{Churn Rate \%} = \frac{\text{Count of Churned Customers}}{\text{Total Customer Base}} \times 100$$
In Power BI, I implemented this dynamically using the DAX formula `DIVIDE([Churned Customers], [Total Customers], 0) * 100`.

---

### Q3: How did you handle missing values during data cleaning?
**Sample Answer:**  
I audited missing values using Python Pandas. For `total_charges`, I imputed missing values logically using `monthly_charges * tenure_months`. For missing `satisfaction_score`, I imputed missing records using the median score per contract tier to maintain distribution integrity. For missing categorical features like `internet_service`, I filled missing values with the modal category (`DSL`).

---

### Q4: How did you identify and handle duplicate records?
**Sample Answer:**  
I checked for duplicate records based on the primary key `customer_id` using `df.duplicated(subset=['customer_id'])`. I found 20 duplicate customer entries in the raw dataset and dropped them using `df.drop_duplicates(subset=['customer_id'], keep='first')` in `src/data_cleaning.py`.

---

### Q5: Why did you use SQL for this project alongside Python?
**Sample Answer:**  
Python is ideal for automated data generation, cleaning, and exploratory plotting. SQL is the industry standard for querying relational databases, building structured datasets, and serving BI tools. Using SQL demonstrated my ability to write schema DDLs, indexes, CTEs, window functions (`RANK()`, `ROW_NUMBER()`), and conditional aggregations (`CASE WHEN`).

---

### Q6: Can you give an example of an advanced SQL query you wrote?
**Sample Answer:**  
I wrote a query utilizing Common Table Expressions (CTEs) and Window Functions (`ROW_NUMBER()`) to rank churned customers by annualized revenue loss:
```sql
WITH RankedLoss AS (
    SELECT customer_id, subscription_plan, monthly_charges * 12 AS annual_revenue_lost,
           ROW_NUMBER() OVER (ORDER BY monthly_charges DESC) AS rank_by_loss
    FROM customers WHERE churn = 'Yes'
)
SELECT * FROM RankedLoss WHERE rank_by_loss <= 10;
```
This allowed management to immediately identify the top 10 highest-value lost accounts.

---

### Q7: Why did you design a Power BI dashboard?
**Sample Answer:**  
Business stakeholders need interactive visual intelligence rather than raw code or static files. I designed a 3-page dashboard (Executive Overview, Churn Drivers, Retention & Revenue) with slicers, KPI metric cards, and visual hierarchies so leaders can self-serve insights across segments.

---

### Q8: What were your main Key Performance Indicators (KPIs)?
**Sample Answer:**  
1. Total Customers
2. Active vs Churned Customers
3. Overall Churn Rate (%)
4. Average Monthly Charge ($)
5. Average Customer Tenure (Months)
6. Annualized Revenue at Risk ($)

---

### Q9: What was the single most important finding of your analysis?
**Sample Answer:**  
Contract type and early tenure are the strongest observable drivers of churn. Customers on month-to-month contracts with under 12 months of tenure exhibit disproportionately higher churn rates compared to long-term contract holders, generating over 70% of total revenue at risk.

---

### Q10: What actionable recommendations did you present to management?
**Sample Answer:**  
1. **Contract Migration Campaigns**: Offer a 10% annual discount to incentivize month-to-month customers to move to 1-year contracts.
2. **First-Year Onboarding**: Implement proactive onboarding touchpoints during months 1–6.
3. **High-Ticket Proactive Outreach**: Automatically flag accounts filing 3+ support tickets for immediate customer success intervention.

---

### Q11: How did you define and calculate "Revenue at Risk"?
**Sample Answer:**  
Revenue at risk was calculated as an estimated annualized revenue metric for churned accounts: `monthly_charges * 12`. I specifically labeled this as an estimated annualized loss metric rather than historical cash flow loss to avoid misleading stakeholders.

---

### Q12: What are the main limitations of your analysis?
**Sample Answer:**  
The dataset is synthetic, built for portfolio demonstration. Additionally, observational data shows strong associations but cannot prove strict causality. Lastly, revenue at risk is an annualized projection.

---

### Q13: Can you prove that month-to-month contracts *cause* churn?
**Sample Answer:**  
No, correlation does not imply causation. Month-to-month contracts lower the switching barrier for dissatisfied customers, making them more likely to churn when friction arises, but the contract structure itself is an enabling factor rather than the sole root cause.

---

### Q14: How would you validate the accuracy of your dashboard before sharing it?
**Sample Answer:**  
I cross-validate key metrics across Python script outputs, SQL query returns, and Power BI DAX card values. If all three produce identical numbers for Total Customers, Churned Customers, and Churn Rate, I know the pipeline is logically consistent.

---

### Q15: How would you adapt this project if working with real company data?
**Sample Answer:**  
I would integrate direct SQL database connections (e.g. Snowflake or BigQuery), set up automated ETL pipelines (Airflow/dbt), incorporate real-time support ticket logs, and track monthly cohort retention curves over time.

---

### Q16: How would you explain "Churn Rate" to a non-technical marketing manager?
**Sample Answer:**  
"Churn rate is simply the percentage of our total customers who stopped paying for our service during a given period. If we started the month with 100 customers and 5 cancelled, our churn rate is 5%. Our goal is to keep that number as close to zero as possible."

---

### Q17: What would you do if executive stakeholders disagreed with your findings?
**Sample Answer:**  
I would listen to their business perspective, walk them transparently through the data sources, SQL queries, and logic, offer to run sensitivity checks or drill down into specific customer cohorts, and refine the analysis collaboratively.

---

### Q18: How would you prioritize retention campaigns with a limited budget?
**Sample Answer:**  
I would focus budget on the **High-Value, High-Risk** quadrant of our customer matrix—targeting customers paying above-average monthly fees who are on month-to-month contracts and showing early dissatisfaction signals (high tickets or low CSAT).

---

### Q19: What additional data features would you request to improve the analysis?
**Sample Answer:**  
I would request competitor pricing benchmark data, network service outage logs, customer interaction sentiment scores from support chat transcripts, and detailed payment failure logs.

---

### Q20: How would you convert this descriptive project into a Machine Learning churn prediction model?
**Sample Answer:**  
I would frame it as a binary classification problem (Churn = 1/0), train a Random Forest or XGBoost model on historical customer features, tune hyperparameters, and evaluate using **Recall** and **ROC-AUC**. Maximizing Recall ensures we catch as many at-risk customers as possible before they cancel.
