import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Load all CSV files from the features directory
features_dir = "./features/output"
feature_files = [
    "Annual_Rainfall.csv",
    "Avg_Annual_Production.csv",
    "Avg_Temperature.csv",
    "Drought_Index.csv",
    "Growing_Season_Length.csv",
    "Moisture_Index.csv",
    "Production_Growth_Rate.csv",
    "Production_Variability.csv",
]

# Add meaningful column names to each file and merge
all_features = []
for file in feature_files:
    file_path = os.path.join(features_dir, file)
    df = pd.read_csv(file_path, header=None)  # Assuming no header exists
    feature_name = os.path.splitext(file)[0]  # Use the file name (without extension) as the column name
    
    # If the DataFrame has more than 2 columns, include all columns
    if df.shape[1] > 2:
        column_names = ["ID"] + [f"{feature_name}_col{i}" for i in range(1, df.shape[1])]

    else:  # If it has exactly 2 columns
        column_names = ["ID", feature_name]
    
    df.columns = column_names  # Assign meaningful column names
    all_features.append(df)

# Merge all features into a single DataFrame
merged_df = all_features[0]
for df in all_features[1:]:
    merged_df = pd.merge(merged_df, df, on="ID", how="outer")

# Ensure all non-numeric columns are excluded for clustering
for col in merged_df.columns:
    if col != "ID":  # Exclude the ID column
        merged_df[col] = pd.to_numeric(merged_df[col], errors="coerce")

# Drop non-numeric columns (such as Region_Name)
merged_df = merged_df.select_dtypes(include=[np.number])

# Handle missing values (e.g., fill NaN with 0 or drop rows with NaN)
merged_df.fillna(0, inplace=True)

# Debugging output after fixing data
print("Merged DataFrame shape:", merged_df.shape)
print("Merged DataFrame columns:", merged_df.columns)
print("Column Data Types:\n", merged_df.dtypes)

# Select only numeric columns for clustering
numeric_df = merged_df

# Debugging output for numeric DataFrame
print("Numeric DataFrame shape:", numeric_df.shape)
print("Numeric DataFrame columns:", numeric_df.columns)

if numeric_df.empty:
    raise ValueError("The numeric DataFrame is empty. Ensure the input data contains numeric columns.")

# Standardize the numeric data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_df)

# Determine the optimal number of clusters using the Elbow Method and Silhouette Analysis
sse = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)
    silhouette_avg = silhouette_score(scaled_data, kmeans.labels_)
    silhouette_scores.append(silhouette_avg)

# Plot Elbow Method
plt.figure(figsize=(10, 5))
plt.plot(K_range, sse, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('SSE')
plt.show()

# Plot Silhouette Analysis
plt.figure(figsize=(10, 5))
plt.plot(K_range, silhouette_scores, marker='o', color='orange')
plt.title('Silhouette Analysis')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()

# Select the optimal number of clusters based on the above analyses
optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2

# Fit the final k-Means model
kmeans_final = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
kmeans_final.fit(scaled_data)
labels = kmeans_final.labels_

# Add cluster labels to the original DataFrame
merged_df['Cluster'] = labels

# Cluster Profiling
cluster_profiles = merged_df.groupby('Cluster').mean()
print(cluster_profiles)

# Visualize clusters (in 2D using PCA if needed)
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 8))
sns.scatterplot(
    x=pca_data[:, 0],
    y=pca_data[:, 1],
    hue=labels,
    palette='viridis',
    s=100
)
plt.title('Cluster Visualization (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.show()