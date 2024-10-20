python

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Get the unique device models and their counts
device_model_counts = df['Device Model'].value_counts()

# Print the top 10 device models
print("Top 10 device models:")
print(device_model_counts.head(10))

# Create a bar chart of the top 10 device models
plt.figure(figsize=(10,6))
device_model_counts.head(10).plot(kind='bar')
plt.title('Distribution of Device Models')
plt.xlabel('Device Model')
plt.ylabel('Count')
plt.show()
plt.savefig('plot_output.png')