import pandas as pd
from sqlalchemy import create_engine

# Load data
df = pd.read_csv('C:/Users/mahaw/OneDrive/Documents/CODING/Data Analytics/majorProject/customer_shopping_behavior.csv')
print(df)

# Handle missing Review Rating
df['Review Rating'] = df.groupby('Category')['Review Rating'] \
                         .transform(lambda x: x.fillna(x.median()))

# Clean column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# Create age groups
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

# Map frequency to days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchases_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# Drop duplicate column
df = df.drop('promo_code_used', axis=1)

# MySQL connection
engine = create_engine(
    "mysql+pymysql://root:pokemonpo123%40%26@localhost/myDB"
)

# Upload cleaned data
df.to_sql(
    name="customer_shopping",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Cleaned data successfully loaded into MySQL!")