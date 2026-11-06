import pandas as pd

def clean_hr_data(raw_path):
    df = pd.read_csv(raw_path)

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
    df['Age'] = df['Age'].replace('thirty', 30)

    # Int64 is a nullable integer data type in pandas that allows for missing values (NaN) in the column.
    # It will not raise errors when encountering NaN values.
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').astype('Int64')

    # Calculating the age based on the birth year and 2024 as the current year.
    df['Age'] = df['Birth Year'].apply(lambda x: 2024 - x if pd.notnull(x) else x)

    # Fixing the salary column

    # Removing any non-numeric characters from the salary column and converting it to a numeric data type
    df['Salary'] = df['Salary'].replace('SIXTY THOUSAND', 60000)

    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce').astype('Int64')

    # Renamed Name column header to First Name to match Last Name column header.
    df = df.rename(columns={'Name': 'First Name'})

    df['Email'] = df['First Name'].str.lower() + '.' + df['Last Name'].str.lower() + '@saltcorp.com'

    #fixing the benefits enrolled column
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

    df['Joining Date'] = df['Joining Date'].dt.strftime('%d/%m/%Y')

    # It replaced the N/A with blanks 
    df['Last Promotion Date'] = pd.to_datetime(df['Last Promotion Date'], format='mixed', errors='coerce')
    df['Last Promotion Date'] = df['Last Promotion Date'].dt.strftime('%d/%m/%Y')

    # Fixing column headers
    df.rename(columns={'attrition': 'Attrition', 'job_satisfaction':'Job Satisfaction'})


    return df

if __name__ == "__main__":
    df = clean_hr_data('/data/raw/hr_data.csv')
    print("Cleaned HR Data:")
    print(df.info())
    print(df.dtypes)
    print(df.head())
    