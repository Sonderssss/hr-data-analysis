import pandas as pd

def clean_hr_data(raw_path):
    df = pd.read_csv(raw_path)


    print(f"Department blanks: {df['Department'].isna().sum()} (Expected: 0)")
    # Department
    department_map = {
    'Finance':'Finance',
        'Sales':'Sales',
        'HR':'HR',
        'IT':'IT',
        'Marketing':'Marketing',
        'marketing':'Marketing',
        'finance':'Finance',  
        'it':'IT',
        'hr':'HR',     
        'sales':'Sales'
    }

    df['Department'] = df['Department'].str.strip().map(department_map)

    ## Employment Status 
    print(f"Employment Status blanks: {df['Employment Status'].isna().sum()} (Expected: 0)")

    employment_status_map = {
        'Full-Time':'Full-Time',
        'Part-Time':'Part-Time',
        'full-time':'Full-Time',
        'part-time':'Part-Time',
        'FULL-TIME':'Full-Time',
        'PART-TIME':'Part-Time',
        'contract':'Contract',
        'Contract':'Contract',
    }

    df['Employment Status'] = df['Employment Status'].str.strip().map(employment_status_map)

    #Age
    #replacing all the string values in the Age column with the numeric values
    # Process original column cleanly into a temporary space
    df['Age_Temp_Original'] = df['Age'].replace('thirty', 30)
    df['Age_Temp_Original'] = pd.to_numeric(df['Age_Temp_Original'], errors='coerce').astype('Int64')

    # Calculate using vectorized operations across the entire column simultaneously
    df['Age'] = (2024 - df['Birth Year']).astype('Int64')

    # Check for discrepancies before dropping the temporary check column
    age_discrepancies = df[df['Age_Temp_Original'].notna() & (df['Age_Temp_Original'] != df['Age'])]
    print("--- Age Discrepancy Integrity Check ---")
    print(f"Number of pre-existing ages that conflict with calculated birth-year age: {len(age_discrepancies)}")
    df = df.drop(columns=['Age_Temp_Original'])

    # Fixing the salary column

    # Removing any non-numeric characters from the salary column and converting it to a numeric data type
    df['Salary'] = df['Salary'].replace('SIXTY THOUSAND', 60000)

    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce').astype('Int64')

    print("--- Salary Data Validation Check ---")
    print(f"Salary missing values post-conversion: {df['Salary'].isna().sum()} (Expected: 0)\n")

    # Renamed Name column header to First Name to match Last Name column header.
    df = df.rename(columns={'Name': 'First Name'})

    # flag if any duplicate identical name pairs exist
    duplicate_names_count = df.duplicated(subset=['First Name', 'Last Name'], keep=False).sum()
    print("--- Email & Collision Integrity Check ---")
    print(f"Rows sharing exactly identical First and Last names: {duplicate_names_count}")

    generated_emails = df['First Name'].str.lower() + '.' + df['Last Name'].str.lower() + '@saltcorp.com'
    df['Email'] = df['Email'].fillna(generated_emails)

    #fixing the benefits enrolled column
    print(f"Benefits Enrolled blanks: {df['Benefits Enrolled'].isna().sum()} (Expected: 210)\n")

    benefits_enrolled_map = {
        'No':'No',
        'Yes':'Yes',
        'no':'No',
        'YES':'Yes',
        'yes':'Yes',
        'Y':'Yes',
        'N':'No'
    }

    df['Benefits Enrolled'] = df['Benefits Enrolled'].str.strip().map(benefits_enrolled_map)

    df['Benefits Enrolled'] = df['Benefits Enrolled'].fillna('')


    # Fixing the Joining Date column
    df['Joining Date'] = pd.to_datetime(df['Joining Date'], format='mixed', errors='coerce')

    # It replaced the N/A with blanks 
    df['Last Promotion Date'] = pd.to_datetime(df['Last Promotion Date'], format='mixed', errors='coerce')

    # Fixing column headers
    df = df.rename(columns={'attrition': 'Attrition', 'job_satisfaction':'Job Satisfaction'})

    print(f"Joining Date blank count: {df['Joining Date'].isna().sum()} (Expected: 0)")
    print(f"Last Promotion Date blank count: {df['Last Promotion Date'].isna().sum()} (Expected: 641)\n")


    return df

if __name__ == "__main__":
    df_clean = clean_hr_data('data/raw/hr_data.csv')
    print("Cleaned HR Data:")
    df_clean.to_parquet('data/processed/hr_data.parquet', index=False)
    print("Cleaned HR data saved to 'data/processed/hr_data.parquet'")
    print(df_clean.info())
    