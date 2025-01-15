import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

# Replace these dummy database credentials with your actual database details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Chunelson123'
DB_NAME = 'agric_cameroon'

# Queries for fetching and summarizing data
queries = [
    # Add your list of queries here as in the original code
#Basic join for production analysis
    """
    SELECT 
        pf.Production_ID,
        rd.Region_Name,
        cd.Crop_Name,
        td.Year,
        td.Month,
        td.Season,
        pf.Area_Harvested,
        pf.Quantity,
        pf.Yield
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    JOIN time_dim td ON pf.Time_ID = td.Time_ID
    ORDER BY td.Year, td.Month;
    """,
    #Total production by region and year
    """
    SELECT 
        rd.Region_Name,
        td.Year,
        SUM(pf.Quantity) AS Total_Quantity,
        AVG(pf.Yield) AS Average_Yield
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    JOIN time_dim td ON pf.Time_ID = td.Time_ID
    GROUP BY rd.Region_Name, td.Year
    ORDER BY rd.Region_Name, td.Year;
    """,
    #Crop performance by region
    """
    SELECT 
        cd.Crop_Name,
        rd.Region_Name,
        SUM(pf.Quantity) AS Total_Quantity,
        SUM(pf.Area_Harvested) AS Total_Area,
        AVG(pf.Yield) AS Average_Yield
    FROM production_fact pf
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    GROUP BY cd.Crop_Name, rd.Region_Name
    ORDER BY cd.Crop_Name, Total_Quantity DESC;
    """,
    #Seasonal production trends
    """
    SELECT 
        td.Season,
        cd.Crop_Name,
        SUM(pf.Quantity) AS Total_Quantity,
        AVG(pf.Yield) AS Average_Yield
    FROM production_fact pf
    JOIN time_dim td ON pf.Time_ID = td.Time_ID
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    GROUP BY td.Season, cd.Crop_Name
    ORDER BY td.Season, Total_Quantity DESC;
    """,
    #Climate impact on production
    """
    SELECT 
        cld.Climate_Name,
        cd.Crop_Name,
        AVG(pf.Yield) AS Average_Yield,
        SUM(pf.Quantity) AS Total_Quantity
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    JOIN climate_dim cld ON rd.Climate_ID = cld.Climate_ID
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    GROUP BY cld.Climate_Name, cd.Crop_Name
    ORDER BY cld.Climate_Name, Average_Yield DESC;
    """,
    #Production summary by soil type
    """
    SELECT 
        sd.Soil_Type,
        cd.Crop_Name,
        SUM(pf.Quantity) AS Total_Quantity,
        AVG(pf.Yield) AS Average_Yield
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    JOIN soil_dim sd ON rd.Soil_ID = sd.Soil_ID
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    GROUP BY sd.Soil_Type, cd.Crop_Name
    ORDER BY sd.Soil_Type, Average_Yield DESC;
    """,
    #Yearly crop production comparison
    """
    SELECT 
        cd.Crop_Name,
        td.Year,
        SUM(pf.Quantity) AS Total_Quantity,
        AVG(pf.Yield) AS Average_Yield
    FROM production_fact pf
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    JOIN time_dim td ON pf.Time_ID = td.Time_ID
    GROUP BY cd.Crop_Name, td.Year
    ORDER BY cd.Crop_Name, td.Year;
    """,
    #Regional production summary
    """
    SELECT 
        rd.Region_Name,
        SUM(pf.Quantity) AS Total_Quantity,
        SUM(pf.Area_Harvested) AS Total_Area,
        AVG(pf.Yield) AS Average_Yield,
        rd.Population AS Region_Population
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    GROUP BY rd.Region_Name, rd.Population
    ORDER BY Total_Quantity DESC;
    """,
    #Detailed Production Report
    """
    SELECT 
        pf.Production_ID,
        rd.Region_Name,
        cld.Climate_Name,
        sd.Soil_Type,
        cd.Crop_Name,
        td.Year,
        td.Season,
        pf.Area_Harvested,
        pf.Quantity,
        pf.Yield
    FROM production_fact pf
    JOIN region_dim rd ON pf.Region_ID = rd.Region_ID
    JOIN climate_dim cld ON rd.Climate_ID = cld.Climate_ID
    JOIN soil_dim sd ON rd.Soil_ID = sd.Soil_ID
    JOIN crop_dim cd ON pf.Crop_ID = cd.Crop_ID
    JOIN time_dim td ON pf.Time_ID = td.Time_ID
    ORDER BY td.Year, rd.Region_Name, cd.Crop_Name;
    """
]

# Corresponding table names for saving results
table_names = [
    "production_analysis",
    "total_production_by_region",
    "crop_performance_by_region",
    "seasonal_production_trends",
    "climate_impact_on_production",
    "production_summary_by_soil_type",
    "yearly_crop_production_comparison",
    "regional_production_summary",
    "detailed_production_report"
]

def run_queries_and_save():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            cursor = connection.cursor()

            for index, (query, table_name) in enumerate(zip(queries, table_names), start=1):
                print(f"Executing Query {index} and saving results into '{table_name}'...")
                cursor.execute(query)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]  # Fetch column names

                # Display results in a table format
                print(tabulate(results, headers=columns, tablefmt="grid"))

                # Create table to save results
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join([f'{col} TEXT' for col in columns])}
                );
                """
                cursor.execute(create_table_query)

                # Insert results into the table
                insert_query = f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(columns))})
                """
                cursor.executemany(insert_query, results)
                connection.commit()

                print(f"Results saved into table '{table_name}'.\n")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    run_queries_and_save()
