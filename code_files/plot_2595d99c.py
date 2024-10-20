import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/Users/bala/Downloads/user_behavior_dataset.csv')

# Count the frequency of each device model
device_model_counts = df['Device Model'].value_counts()

# Plot the distribution of device models
plt.figure(figsize=(10,6))
device_model_counts.plot(kind='bar')
plt.title('Distribution of Device Models')
plt.xlabel('Device Model')
plt.ylabel('Frequency')
plt.show()
plt.savefig('plot_output.png')