import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from the CSV file
df = pd.read_csv('user_behavior_dataset.csv')

# Get the count of each device model
device_model_counts = df['Device Model'].value_counts()

# Create a pie chart of device model distribution
plt.figure(figsize=(10,8))
plt.pie(device_model_counts, labels = device_model_counts.index, autopct='%1.1f%%')
plt.title('Device Model Distribution')
plt.show()
plt.savefig('plot_output.png')