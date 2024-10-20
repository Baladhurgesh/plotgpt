import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Filter the dataset for OnePlus and Google devices
oneplus_users = df[df['Device Model'].str.contains('OnePlus')]
google_users = df[df['Device Model'].str.contains('Google')]

# Count the number of users for each device
oneplus_count = len(oneplus_users)
google_count = len(google_users)

# Create a bar chart
labels = ['OnePlus', 'Google']
values = [oneplus_count, google_count]

plt.bar(labels, values)
plt.xlabel('Device Model')
plt.ylabel('Number of Users')
plt.title('Device Model Usage')
plt.show()
plt.savefig('plot_output.png')