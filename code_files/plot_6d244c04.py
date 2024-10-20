import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset from the CSV file
df = pd.read_csv('user_behavior_dataset.csv')

# Select the columns of interest
cols = ['Screen On Time (hours/day)', 'Battery Drain (mAh/day)']

# Create a correlation matrix
corr_matrix = df[cols].corr()

# Create a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation between Screen On Time and Battery Drain')
plt.xlabel('Features')
plt.ylabel('Features')
plt.show()
plt.savefig('plot_output.png')