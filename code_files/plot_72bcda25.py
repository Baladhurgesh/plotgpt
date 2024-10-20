import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Filter the data for users between 20 to 40 years old
df_filtered = df[(df['Age'] >= 20) & (df['Age'] <= 40)]

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the distribution of App Usage Time (min/day) for the filtered data
ax.hist(df_filtered['App Usage Time (min/day)'], bins=20, alpha=0.7, label='App Usage Time (min/day)')

# Set the title and labels
ax.set_title('Distribution of App Usage Time for Users between 20-40 years old')
ax.set_xlabel('App Usage Time (min/day)')
ax.set_ylabel('Frequency')

# Show the plot
plt.show()
plt.savefig('plot_output.png')