import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from fuzzywuzzy import process

# Load the merged CSV data
merged_data_path = "./feature/output/merged_data.csv"
region_dim_path = "./csv files/region_dim.csv"

df = pd.read_csv(merged_data_path)

# Print the first and last records of the dataframe
print("Entry Records of the DataFrame:")
print(df.head())
print("\nEnding Records of the DataFrame:")
print(df.tail())

# Handle missing data
df = df.dropna()  # Drop rows with missing values
# Optionally: df.fillna(value, inplace=True) to impute missing values

# Load and preprocess the Region_Name data
region_df = pd.read_csv(region_dim_path)

# Filter out non-string values in Region_Name and drop duplicates
region_df["Region_Name"] = region_df["Region_Name"].astype(str)
region_df = region_df[region_df["Region_Name"].str.isalpha()]  # Keep only alphabetic region names
region_df = region_df.drop_duplicates(subset=["Region_Name"])  # Drop duplicate region names

# Select only the necessary columns and remove duplicates
region_df = region_df[["Region_ID", "Region_Name"]].drop_duplicates()

# Ensure the Region_ID columns are of the same data type (e.g., str) before merging
df["Region_ID"] = df["Region_ID"].astype(str)
region_df["Region_ID"] = region_df["Region_ID"].astype(str)

# Merge Region_Name with the main dataframe on Region_ID
df = df.merge(region_df, on="Region_ID", how="left")

# Fuzzy match region names to handle mismatches
def fuzzy_match_region_names(region_df, target_df):
    region_names = region_df["Region_Name"].tolist()
    # Ensure all values in the Region_Name column are treated as strings
    target_df["Region_Name"] = target_df["Region_Name"].astype(str)
    # Apply fuzzy matching, and ignore non-string values (such as NaN)
    target_df["Region_Name"] = target_df["Region_Name"].apply(
        lambda x: process.extractOne(x, region_names)[0] if isinstance(x, str) else None
    )
    return target_df

df = fuzzy_match_region_names(region_df, df)

# Handle categorical data
categorical_cols = df.select_dtypes(include=["object"]).columns
if categorical_cols.any():
    encoder = OneHotEncoder(sparse_output=False, drop="first")
    encoded_data = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))
    df = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

# Feature selection
selector = VarianceThreshold(threshold=0.1)  # Remove low variance features
X = selector.fit_transform(df)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dimensionality reduction
pca = PCA(n_components=0.95)  # Retain 95% of variance
X_pca = pca.fit_transform(X_scaled)

# Cluster validation with multiple values of k
metrics = {
    "Silhouette": [],
    "Davies-Bouldin": [],
    "Calinski-Harabasz": []
}
k_values = range(2, 11)
for k in k_values:
    kmeans = KMeans(n_clusters=k, init="k-means++", random_state=42)
    labels = kmeans.fit_predict(X_pca)
    silhouette = silhouette_score(X_pca, labels)
    davies_bouldin = davies_bouldin_score(X_pca, labels)
    calinski_harabasz = calinski_harabasz_score(X_pca, labels)

    # Append values to metrics
    metrics["Silhouette"].append(silhouette)
    metrics["Davies-Bouldin"].append(davies_bouldin)
    metrics["Calinski-Harabasz"].append(calinski_harabasz)
    
    # Print the metrics values for each k
    print(f"\nMetrics for k={k}:")
    print(f"Silhouette Score: {silhouette}")
    print(f"Davies-Bouldin Index: {davies_bouldin}")
    print(f"Calinski-Harabasz Index: {calinski_harabasz}")

# Plot metrics for k values
plt.figure(figsize=(12, 6))
plt.plot(k_values, metrics["Silhouette"], label="Silhouette Score")
plt.plot(k_values, metrics["Davies-Bouldin"], label="Davies-Bouldin Index")
plt.plot(k_values, metrics["Calinski-Harabasz"], label="Calinski-Harabasz Index")
plt.title("Cluster Validation Metrics")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Score")
plt.legend()
plt.grid(True)
plt.show()

# Choose optimal k based on combined evaluation
optimal_k = 4  # Update based on evaluation
print(f"\nOptimal number of clusters (k): {optimal_k}")

# Perform KMeans clustering with optimal k
kmeans = KMeans(n_clusters=optimal_k, init="k-means++", random_state=42)
labels = kmeans.fit_predict(X_pca)

# Assign meaningful names to clusters
cluster_names = {0: "High Capacity", 1: "Moderate Capacity", 2: "Low Capacity", 3: "Emerging"}
df["Cluster"] = labels
df["Cluster_Label"] = df["Cluster"].map(cluster_names)

# Visualization with t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_pca)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=df["Cluster_Label"], palette="viridis")
plt.title("Cluster Visualization with t-SNE")
plt.xlabel("t-SNE Component 1")  # Label for the x-axis
plt.ylabel("t-SNE Component 2")  # Label for the y-axis
plt.show()

# Merge with Region_Name
df_with_regions = df.join(region_df, how="left").dropna(subset=["Region_Name"])

# Save unmatched regions
unmatched_regions = set(region_df["Region_Name"]) - set(df_with_regions["Region_Name"])
unmatched_output_path = "./feature/output/unmatched_regions.csv"
pd.DataFrame({"Unmatched_Regions": list(unmatched_regions)}).to_csv(unmatched_output_path, index=False)

# Save final data
output_csv_path = "./feature/output/data_with_clusters.csv"
df_with_regions.to_csv(output_csv_path, index=False)

print(f"Clustered data saved at {output_csv_path}")
print(f"Unmatched regions saved at {unmatched_output_path}")
