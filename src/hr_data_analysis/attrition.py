import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_parquet('data/processed/hr_data.parquet')

factor_list = [
    'Department', 'Position', 'Employment Status', 'Gender', 
    'Benefits Enrolled', 'Joining Date', 'Salary Band', 'Performance Score', 
    'Job Satisfaction', 'Age Band'
]

summary_list = []

# Handle the main work of making individual summary tables per factor
def attrition_factor_table(col_name):
    col_counts = pd.crosstab( df[col_name], df['Attrition'])

    col_attrition = (pd.crosstab( df[col_name], df['Attrition'], normalize='index')['Yes'] * 100 ).round(2).sort_values(ascending=False)

    return (pd.concat(
                [df[col_name].value_counts(), col_counts['Yes'], col_attrition], 
                axis=1, 
                keys=['Counts','Left','Attrition']
                ).sort_values(by='Attrition' , ascending=False))



for factor in factor_list:
    table  = attrition_factor_table(factor)

    #  Highest group name
    highest_group = table['Attrition'].idxmax()

    # Highest value
    highest_value = table['Attrition'].max()

    #  Lowest group name
    lowest_group = table['Attrition'].idxmin()

    # Lowest value
    lowest_value = table['Attrition'].min()

    # Difference between the highest group and the lowest group
    gap = highest_value - lowest_value

    smalllest_group_size = table['Counts'].min()

    p_value = chi2_contingency(pd.crosstab(df[factor], df['Attrition']))[1]

    row_dict = {
        "Factor": factor,
        "Highest Group":highest_group,
        "Highest Value":highest_value,
        "Lowest Group":lowest_group,
        "Lowest Value":lowest_value,
        "Gap":round(gap,2),
        "Smallest Group Size": smalllest_group_size,
        "P Value":round(p_value,4)
    }

    summary_list.append(row_dict)

summary_table = pd.DataFrame(summary_list).sort_values(by="Gap", ascending=False)

summary_table
