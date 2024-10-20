import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Filter the data for Google devices
google_devices = df[df['Device Model'].str.contains('Google', case=False)]

# Group by User ID and count the number of users
google_users = google_devices.groupby('User ID').size()

# Create a bar chart
plt.figure(figsize=(10,6))
google_users.plot(kind='bar')
plt.title('Number of Users with Google Devices')
plt.xlabel('User ID')
plt.ylabel('Count')
plt.show()
plt.savefig('plot_output.png')