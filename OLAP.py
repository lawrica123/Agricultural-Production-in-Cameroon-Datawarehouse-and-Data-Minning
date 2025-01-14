import mysql.connector
import pandas as pd

# Database connection details
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='uct04bgs101120',
            database='agric_cameroon'
        )
        cursor = conn.cursor()
        print("Connected to the database.")
        return conn, cursor
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None, None

# Check connection and execute query
def execute_query(query):
    conn, cursor = connect_to_database()
    if conn and cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Extract column names
            df = pd.DataFrame(result, columns=columns)
            return df
        except mysql.connector.Error as e:
            print(f"Error while executing query: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("MySQL connection is closed.")

# OLAP Queries

# 1. Total Crop Production by Region and Year
query_1 = """
SELECT r.Region_Name, t.Year, SUM(p.Quantity) AS Total_Production
FROM production_fact p
JOIN region_dim r ON p.Region_ID = r.Region_ID
JOIN time_dim t ON p.Time_ID = t.Time_ID
GROUP BY r.Region_Name, t.Year
ORDER BY r.Region_Name, t.Year;
"""

# 2. Average Yield per Crop Type by Region
query_2 = """
SELECT r.Region_Name, c.Crop_Type, AVG(p.Yield) AS Avg_Yield
FROM production_fact p
JOIN crop_dim c ON p.Crop_ID = c.Crop_ID
JOIN region_dim r ON p.Region_ID = r.Region_ID
GROUP BY r.Region_Name, c.Crop_Type
ORDER BY r.Region_Name, c.Crop_Type;
"""

# 3. Total Production by Crop and Climate Type
query_3 = """
SELECT c.Climate_Name, c.Crop_Name, SUM(p.Quantity) AS Total_Production
FROM production_fact p
JOIN crop_dim c ON p.Crop_ID = c.Crop_ID
JOIN region_dim r ON p.Region_ID = r.Region_ID
JOIN climate_dim c ON r.Climate_ID = c.Climate_ID
GROUP BY c.Climate_Name, c.Crop_Name
ORDER BY c.Climate_Name, c.Crop_Name;
"""

# 4. Revenue and Cost Analysis by Region and Crop
query_4 = """
SELECT r.Region_Name, c.Crop_Name, SUM(p.Revenue) AS Total_Revenue, SUM(p.Cost) AS Total_Cost
FROM production_fact p
JOIN region_dim r ON p.Region_ID = r.Region_ID
JOIN crop_dim c ON p.Crop_ID = c.Crop_ID
GROUP BY r.Region_Name, c.Crop_Name
ORDER BY r.Region_Name, c.Crop_Name;
"""

# 5. Year-over-Year Growth in Crop Production by Region
query_5 = """
SELECT r.Region_Name, t.Year, 
       SUM(p.Quantity) - LAG(SUM(p.Quantity)) OVER (PARTITION BY r.Region_Name ORDER BY t.Year) AS YoY_Growth
FROM production_fact p
JOIN region_dim r ON p.Region_ID = r.Region_ID
JOIN time_dim t ON p.Time_ID = t.Time_ID
GROUP BY r.Region_Name, t.Year
ORDER BY r.Region_Name, t.Year;
"""

# 6. Top 5 Crops by Market Value and Production Volume
query_6 = """
SELECT c.Crop_Name, SUM(p.Quantity) AS Total_Production, SUM(c.Market_Value * p.Quantity) AS Total_Market_Value
FROM production_fact p
JOIN crop_dim c ON p.Crop_ID = c.Crop_ID
GROUP BY c.Crop_Name
ORDER BY Total_Market_Value DESC
LIMIT 5;
"""

# 7. Crop Performance Analysis Across Different Seasons
query_7 = """
SELECT t.Season, c.Crop_Name, AVG(p.Yield) AS Avg_Yield
FROM production_fact p
JOIN crop_dim c ON p.Crop_ID = c.Crop_ID
JOIN time_dim t ON p.Time_ID = t.Time_ID
GROUP BY t.Season, c.Crop_Name
ORDER BY t.Season, c.Crop_Name;
"""

# 8. Soil and Climate Impact on Yield by Region
query_8 = """
SELECT r.Region_Name, s.Soil_Type, c.Climate_Name, AVG(p.Yield) AS Avg_Yield
FROM production_fact p
JOIN region_dim r ON p.Region_ID = r.Region_ID
JOIN soil_dim s ON r.Soil_ID = s.Soil_ID
JOIN climate_dim c ON r.Climate_ID = c.Climate_ID
GROUP BY r.Region_Name, s.Soil_Type, c.Climate_Name
ORDER BY r.Region_Name, s.Soil_Type, c.Climate_Name;
"""

# Running a specific query and printing the results as DataFrame
def run_queries():
    df_1 = execute_query(query_1)
    print("Total Crop Production by Region and Year:")
    print(df_1)

    df_2 = execute_query(query_2)
    print("\nAverage Yield per Crop Type by Region:")
    print(df_2)

    df_3 = execute_query(query_3)
    print("\nTotal Production by Crop and Climate Type:")
    print(df_3)

    df_4 = execute_query(query_4)
    print("\nRevenue and Cost Analysis by Region and Crop:")
    print(df_4)

    df_5 = execute_query(query_5)
    print("\nYear-over-Year Growth in Crop Production by Region:")
    print(df_5)

    df_6 = execute_query(query_6)
    print("\nTop 5 Crops by Market Value and Production Volume:")
    print(df_6)

    df_7 = execute_query(query_7)
    print("\nCrop Performance Analysis Across Different Seasons:")
    print(df_7)

    df_8 = execute_query(query_8)
    print("\nSoil and Climate Impact on Yield by Region:")
    print(df_8)

# Execute all queries
run_queries()
