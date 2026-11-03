import pandas as pd

def clean_hr_data(df):
    pass


if __name__ == "__main__":
    df = pd.read_csv('../data/raw/hr_data.csv')
    cleaned_df = clean_hr_data(df)
    cleaned_df.to_csv('../data/processed/cleaned_hr_data.csv')