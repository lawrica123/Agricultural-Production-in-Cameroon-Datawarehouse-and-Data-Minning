import pandas as pd
import sqlite3

# Load the data
data_path = './feature/output/data_with_clusters.csv'
df = pd.read_csv(data_path)

# Create an SQLite in-memory database
conn = sqlite3.connect(':memory:')

# Write the dataframe to an SQL table
df.to_sql('data_with_clusters', conn, if_exists='replace', index=False)

# 1. Regions with Highest Production Variability
query1 = """
SELECT 
    Region_Name, 
    MAX(Production_Variability) AS Max_Production_Variability 
FROM 
    data_with_clusters
GROUP BY 
    Region_Name
ORDER BY 
    Max_Production_Variability DESC;
"""
result1 = pd.read_sql_query(query1, conn)
print("Regions with Highest Production Variability:")
print(result1)
print()

# 2. Relationship Between Temperature and Production
query2 = """
SELECT 
    Region_Name, 
    AVG(Avg_Temperature) AS Avg_Temperature, 
    SUM(Total_Annual_Production) AS Total_Production 
FROM 
    data_with_clusters
GROUP BY 
    Region_Name
ORDER BY 
    Avg_Temperature DESC;
"""
result2 = pd.read_sql_query(query2, conn)
print("Relationship Between Temperature and Production:")
print(result2)
print()

# 3. Correlation Between Rainfall and Production
query3 = """
SELECT 
    Annual_Rainfall, 
    AVG(Total_Annual_Production) AS Avg_Production 
FROM 
    data_with_clusters
GROUP BY 
    Annual_Rainfall
ORDER BY 
    Annual_Rainfall;
"""
result3 = pd.read_sql_query(query3, conn)
print("Correlation Between Rainfall and Production:")
print(result3)
print()

# 4. Cluster Membership Analysis
query4 = """
SELECT 
    Cluster_Label, 
    COUNT(DISTINCT Region_Name) AS Region_Count 
FROM 
    data_with_clusters
GROUP BY 
    Cluster_Label
ORDER BY 
    Region_Count DESC;
"""
result4 = pd.read_sql_query(query4, conn)
print("Cluster Membership Analysis:")
print(result4)
print()

# 5. Highest Production Region by Cluster
query5 = """
SELECT 
    Cluster_Label, 
    Region_Name, 
    MAX(Total_Annual_Production) AS Max_Production 
FROM 
    data_with_clusters
GROUP BY 
    Cluster_Label, 
    Region_Name
ORDER BY 
    Cluster_Label, 
    Max_Production DESC;
"""
result5 = pd.read_sql_query(query5, conn)
print("Highest Production Region by Cluster:")
print(result5)
print()

# 6. Extreme Weather and Its Impact
query6 = """
SELECT 
    Region_Name, 
    MIN(Avg_Temperature) AS Min_Temperature, 
    MAX(Avg_Temperature) AS Max_Temperature, 
    AVG(Total_Annual_Production) AS Avg_Production 
FROM 
    data_with_clusters
GROUP BY 
    Region_Name
ORDER BY 
    Max_Temperature DESC, Min_Temperature;
"""
result6 = pd.read_sql_query(query6, conn)
print("Extreme Weather and Its Impact:")
print(result6)
print()

# Close the database connection
conn.close()
