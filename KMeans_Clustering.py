import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Load all CSV files from the features directory
features_dir = "./Features/output"
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
    df = pd.read_csv(file_path, header=None, encoding='utf-8')  # Explicitly set UTF-8 encoding
    feature_name = os.path.splitext(file)[0]
    column_names = ["ID"] + [f"{feature_name}_col{i}" for i in range(1, df.shape[1])]
    df.columns = column_names[:df.shape[1]]  # Handle variable column lengths
    all_features.append(df)

# Merge all features into a single DataFrame
merged_df = all_features[0]
for df in all_features[1:]:
    merged_df = pd.merge(merged_df, df, on="ID", how="outer")

# Ensure all non-numeric columns are excluded for clustering
for col in merged_df.columns:
    if col != "ID":  # Exclude the ID column
        merged_df[col] = pd.to_numeric(merged_df[col], errors="coerce")

merged_df.fillna(0, inplace=True)

# Standardize the numeric data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(merged_df.drop(columns=["ID"]))

# Determine the optimal number of clusters
sse, silhouette_scores, K_range = [], [], range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))

# Plot Elbow and Silhouette Analysis
plt.figure(figsize=(10, 5))
plt.plot(K_range, sse, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('SSE')
plt.savefig('elbow_method.png')

plt.figure(figsize=(10, 5))
plt.plot(K_range, silhouette_scores, marker='o', color='orange')
plt.title('Silhouette Analysis')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.savefig('silhouette_analysis.png')

# Fit the final k-Means model
optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2
kmeans_final = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42, n_init=10)
kmeans_final.fit(scaled_data)
merged_df['Cluster'] = kmeans_final.labels_

# Visualize clusters using PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 8))
sns.scatterplot(
    x=pca_data[:, 0],
    y=pca_data[:, 1],
    hue=kmeans_final.labels_,
    palette='viridis',
    s=100
)
plt.title('Cluster Visualization (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.savefig('cluster_visualization.png')