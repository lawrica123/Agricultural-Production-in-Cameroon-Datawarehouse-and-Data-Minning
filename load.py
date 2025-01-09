import mysql.connector
import pandas as pd

# Paths to your CSV files
climate_csv = './csv files/climate_dim.csv'
crop_csv = './csv files/crop_dim.csv'
region_csv = './csv files/region_dim.csv'
soil_csv = './csv files/soil_dim.csv'
time_csv = './csv files/time_dim.csv'
production_csv = './csv files/production_facts.csv'

# Database connection details
# Connect to MySQL Database
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='uct04bgs101120',
        database='agric_cameroon'
    )
    cursor = conn.cursor()
    print("Connected to the database.")

    # Load and insert climate_Dim data
    climate_df = pd.read_csv(climate_csv)
    for _, row in climate_df.iterrows():
        cursor.execute("""
            INSERT INTO climate_dim (Climate_ID,Climate_Name,Avg_Temperature,Humidity_Level,Annual_Rainfall)
            VALUES (%s, %s, %s, %s , %s)
        """, (row['Climate_ID'], row['Climate_Name'], row['Avg_Temperature'], row['Humidity_Level'], row['Annual_Rainfall'] ))

    # Load and insert crop_Dim data
    crop_df = pd.read_csv(crop_csv)
    for _, row in crop_df.iterrows():
        cursor.execute("""
            INSERT INTO crop_dim (Crop_ID,Crop_Name,Crop_Type,Market_Value,Growth_Duration,Water_Requirement) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['Crop_ID'], row['Crop_Name'], row['Crop_Type'], row['Market_Value'], row['Growth_Duration'], row['Water_Requirement']))

    # Load and insert region_Dim data
    region_df = pd.read_csv(region_csv)
    for _, row in region_df.iterrows():
        cursor.execute("""
            INSERT INTO region_dim (Region_ID,Region_Name,Climate_ID,Soil_ID,Avg_Annual_Rainfall,Altitude,Population)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['Region_ID'], row['Region_Name'], row['Climate_ID'], row['Soil_ID'], row['Avg_Annual_Rainfall'], row['Altitude'], row['Population']))

    # Load and insert soil_dim data
    soil_df = pd.read_csv(soil_csv)
    for _, row in soil_df.iterrows():
        cursor.execute("""
            INSERT INTO soil_dim (Soil_ID,Soil_Type,pH_Level,Organic_Matter)
            VALUES (%s, %s, %s, %s )
        """, (row['Soil_ID'], row['Soil_Type'], row['pH_Level'], row['Organic_Matter']))
        
    # Load and insert time_dim data
    time_df = pd.read_csv(time_csv)
    for _, row in time_df.iterrows():
        cursor.execute("""
            INSERT INTO time_dim (Time_ID,Year,Month,Quarter,Season)
            VALUES (%s, %s, %s , %s, %s)
        """, (row['Time_ID'], row['Year'], row['Month'], row['Quarter'], row['Season'] ))
        

    # Load and insert production_Dim data
    production_df = pd.read_csv(production_csv)
    for _, row in production_df.iterrows():
        cursor.execute("""
            INSERT INTO production_fact(Production_ID,Region_ID,Crop_ID,Time_ID,Area_Harvested,Quantity,Yield)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['Production_ID'], row['Region_ID'], row['Crop_ID'], row['Time_ID'], row['Area_Harvested'], row['Quantity'], row['Yield']))


    # Commit the transactions
    conn.commit()
    print("Data inserted successfully.")

except mysql.connector.Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")
