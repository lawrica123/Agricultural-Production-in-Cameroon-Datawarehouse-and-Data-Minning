import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load the data
data_path = './feature/output/data_with_clusters.csv'
df = pd.read_csv(data_path)

# Create an SQLite in-memory database
conn = sqlite3.connect(':memory:')

# Write the dataframe to an SQL table
df.to_sql('data_with_clusters', conn, if_exists='replace', index=False)

# Query 1: Regions with Highest Production Variability
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

# Visualization: Bar chart for query 1
plt.figure(figsize=(10, 6))
plt.bar(result1['Region_Name'], result1['Max_Production_Variability'], color='skyblue')
plt.title('Regions with Highest Production Variability')
plt.xlabel('Region Name')
plt.ylabel('Production Variability')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Query 2: Relationship Between Temperature and Production
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

# Visualization: Scatter plot for query 2
plt.figure(figsize=(10, 6))
plt.scatter(result2['Avg_Temperature'], result2['Total_Production'], color='green')
plt.title('Relationship Between Temperature and Production')
plt.xlabel('Average Temperature')
plt.ylabel('Total Annual Production')
plt.grid()
plt.tight_layout()
plt.show()

# Query 3: Correlation Between Rainfall and Production
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

# Visualization: Line plot for query 3
plt.figure(figsize=(10, 6))
plt.plot(result3['Annual_Rainfall'], result3['Avg_Production'], marker='o', color='purple')
plt.title('Correlation Between Rainfall and Production')
plt.xlabel('Annual Rainfall')
plt.ylabel('Average Production')
plt.grid()
plt.tight_layout()
plt.show()

# Query 4: Cluster Membership Analysis
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

# Visualization: Bar chart for query 4
plt.figure(figsize=(10, 6))
plt.bar(result4['Cluster_Label'], result4['Region_Count'], color='orange')
plt.title('Cluster Membership Analysis')
plt.xlabel('Cluster Label')
plt.ylabel('Number of Regions')
plt.tight_layout()
plt.show()

# Query 5: Highest Production Region by Cluster
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

# Visualization: Stacked bar chart for query 5
result5_pivot = result5.pivot(index='Cluster_Label', columns='Region_Name', values='Max_Production')
result5_pivot.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')
plt.title('Highest Production Region by Cluster')
plt.xlabel('Cluster Label')
plt.ylabel('Max Production')
plt.tight_layout()
plt.show()

# Query 6: Extreme Weather and Its Impact
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

# Visualization: Multi-bar chart for query 6
plt.figure(figsize=(12, 6))
x = range(len(result6['Region_Name']))
plt.bar(x, result6['Min_Temperature'], width=0.4, label='Min Temperature', align='center', color='blue')
plt.bar(x, result6['Max_Temperature'], width=0.4, label='Max Temperature', align='edge', color='red')
plt.xticks(x, result6['Region_Name'], rotation=45, ha='right')
plt.title('Extreme Weather and Its Impact')
plt.xlabel('Region Name')
plt.ylabel('Temperature')
plt.legend()
plt.tight_layout()
plt.show()

# Close the database connection
conn.close()
