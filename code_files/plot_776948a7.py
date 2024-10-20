python
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/Users/bala/Downloads/user_behavior_dataset.csv')

# Get the count of each device model
device_model_counts = df['Device Model'].value_counts()

# Plot the distribution of device models
plt.figure(figsize=(10, 6))
plt.bar(device_model_counts.index, device_model_counts.values)
plt.xlabel('Device Model')
plt.ylabel('Count')
plt.title('Distribution of Device Models')
plt.show()
plt.savefig('plot_output.png')