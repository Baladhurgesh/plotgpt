import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Get the device model distribution
device_model_distribution = df['Device Model'].value_counts()

# Plot the distribution
plt.figure(figsize=(10, 6))
device_model_distribution.plot(kind='bar')
plt.title('Distribution of Device Models')
plt.xlabel('Device Model')
plt.ylabel('Count')
plt.show()
plt.savefig('plot_output.png')