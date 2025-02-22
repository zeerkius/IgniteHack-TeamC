import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sqlalchemy import create_engine
import psycopg2
from sqlalchemy import text


# ✅ Step 1: Load & Clean Dataset
df = pd.read_csv("/Users/htxoe/Downloads/teamc-wellsdata.csv")

# Rename columns properly
df.columns = [
    "State", "Year", "Production_Rate_Bracket", "Class_Number",
    "Oil_Wells", "Oil_Wells_Percentage", "Oil_Wells_Annual_Production",
    "Oil_Wells_Production_Percentage", "Oil_Wells_Rate_Per_Well",
    "Oil_Wells_Annual_Gas_Production", "Oil_Wells_Gas_Rate_Per_Well",
    "Natural_Gas_Wells", "Natural_Gas_Wells_Percentage", 
    "Natural_Gas_Wells_Annual_Production", "Natural_Gas_Wells_Production_Percentage",
    "Natural_Gas_Wells_Gas_Rate_Per_Well", "Natural_Gas_Wells_Annual_Oil_Production", 
    "Natural_Gas_Wells_Oil_Rate_Per_Well", "Total_Wells", 
    "Total_Wells_Annual_Oil_Production", "Total_Wells_Annual_Gas_Production", 
    "Total_Wells_Horizontal_Well_Count"
]

# Convert numerical columns to appropriate data types
numerical_columns = df.columns[3:]
df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values in essential numerical columns
df = df.dropna(subset=numerical_columns)

# ✅ Step 2: Train Random Forest Model
features = [
    "Class_Number", "Oil_Wells", "Oil_Wells_Percentage", "Oil_Wells_Annual_Production",
    "Oil_Wells_Production_Percentage", "Oil_Wells_Rate_Per_Well", "Oil_Wells_Annual_Gas_Production",
    "Oil_Wells_Gas_Rate_Per_Well", "Natural_Gas_Wells", "Natural_Gas_Wells_Percentage",
    "Natural_Gas_Wells_Annual_Production", "Natural_Gas_Wells_Production_Percentage",
    "Natural_Gas_Wells_Gas_Rate_Per_Well", "Natural_Gas_Wells_Annual_Oil_Production",
    "Natural_Gas_Wells_Oil_Rate_Per_Well", "Total_Wells", "Total_Wells_Annual_Gas_Production"
]

target = "Total_Wells_Annual_Oil_Production"

# Split data into training and testing sets
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def predict_oil_production(input_data):
    """Predict total wells' annual oil production based on input features."""
    input_df = pd.DataFrame([input_data], columns=features)
    return model.predict(input_df)[0]

# ✅ Step 3: Connect to PostgreSQL (Google Cloud SQL)
db_user = "teamc-admin"
db_password = "123456"
db_host = "127.0.0.1"  # Use Cloud SQL Proxy if required
db_port = "5432"
db_name = "WellsData"

# Create SQLAlchemy Engine
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# ✅ Step 4: Create Table in PostgreSQL
create_table_query = '''
CREATE TABLE IF NOT EXISTS well_data (
    State TEXT,
    Year INT,
    Production_Rate_Bracket TEXT,
    Class_Number INT,
    Oil_Wells INT,
    Oil_Wells_Percentage FLOAT,
    Oil_Wells_Annual_Production FLOAT,
    Oil_Wells_Production_Percentage FLOAT,
    Oil_Wells_Rate_Per_Well FLOAT,
    Oil_Wells_Annual_Gas_Production FLOAT,
    Oil_Wells_Gas_Rate_Per_Well FLOAT,
    Natural_Gas_Wells INT,
    Natural_Gas_Wells_Percentage FLOAT,
    Natural_Gas_Wells_Annual_Production FLOAT,
    Natural_Gas_Wells_Production_Percentage FLOAT,
    Natural_Gas_Wells_Gas_Rate_Per_Well FLOAT,
    Natural_Gas_Wells_Annual_Oil_Production FLOAT,
    Natural_Gas_Wells_Oil_Rate_Per_Well FLOAT,
    Total_Wells INT,
    Total_Wells_Annual_Oil_Production FLOAT,
    Total_Wells_Annual_Gas_Production FLOAT,
    Total_Wells_Horizontal_Well_Count INT
);
'''

# Execute SQL
with engine.connect() as conn:
    conn.execute(text(create_table_query))
    conn.commit()

# ✅ Step 5: Insert Cleaned Data into PostgreSQL
df.to_sql('well_data', con=engine, if_exists='replace', index=False, method='multi')

print("✅ Data successfully inserted into PostgreSQL, and model is ready for API integration.")

