import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import pandas as pd
import seaborn as sns

def visualize_data(incidents):
    figs = []
    
    # Clustering visualization
    le_location = LabelEncoder()
    le_nature = LabelEncoder()
    
    locations = le_location.fit_transform([incident[2] for incident in incidents])
    natures = le_nature.fit_transform([incident[3] for incident in incidents])
    
    X = np.array(list(zip(locations, natures)))
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # DBSCAN with optimized parameters
    dbscan = DBSCAN(eps=0.2, min_samples=3)
    clusters = dbscan.fit_predict(X_scaled)
    
    plt.figure(figsize=(15, 10))
    scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], 
                         c=clusters, 
                         cmap='viridis',
                         alpha=0.7,
                         s=80)
    
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel('Location (standardized)', fontsize=12)
    plt.ylabel('Nature of Incident (standardized)', fontsize=12)
    plt.title('Clustering of Incidents by Location and Nature', fontsize=14, pad=20)
    plt.grid(True, linestyle='--', alpha=0.2)
    fig1 = plt.gcf()
    figs.append(fig1)
    
    # Bar Graph
    nature_counts = {}
    for incident in incidents:
        nature = incident[3]
        nature_counts[nature] = nature_counts.get(nature, 0) + 1
    
    nature_counts = dict(sorted(nature_counts.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:15])
    
    plt.figure(figsize=(15, 8))
    bars = plt.bar(nature_counts.keys(), 
                  nature_counts.values(),
                  color=plt.cm.viridis(np.linspace(0, 1, len(nature_counts))))
    
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Nature of Incident', fontsize=12)
    plt.ylabel('Number of Incidents', fontsize=12)
    plt.title('Top 15 Most Frequent Incident Types', fontsize=14, pad=20)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig2 = plt.gcf()
    figs.append(fig2)
    
    # Heatmap
    pivot_table = pd.crosstab(
        pd.Series([incident[2] for incident in incidents], name='Location'),
        pd.Series([incident[3] for incident in incidents], name='Nature')
    )
    
    top_locations = pivot_table.sum(axis=1).nlargest(10).index
    top_natures = pivot_table.sum().nlargest(10).index
    
    plt.figure(figsize=(16, 10))
    sns.heatmap(pivot_table.loc[top_locations, top_natures],
                cmap='YlOrRd',
                annot=True,
                fmt='d',
                cbar_kws={'label': 'Number of Incidents'},
                square=True)
    
    plt.title('Heatmap of Top 10 Locations and Incident Types', 
              fontsize=14, pad=20)
    plt.xlabel('Nature of Incident', fontsize=12)
    plt.ylabel('Location', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig3 = plt.gcf()
    figs.append(fig3)
    
    return figs