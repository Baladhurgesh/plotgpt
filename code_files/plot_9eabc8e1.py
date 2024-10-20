import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# count the number of male and female users
gender_counts = df['gender'].value_counts()

# print the distribution of male and female users
print("distribution of male and female users:")
print(gender_counts)

# plot a bar chart to visualize the distribution
plt.bar(gender_counts.index, gender_counts.values)
plt.xlabel('gender')
plt.ylabel('count')
plt.title('distribution of male and female users')
plt.show()
plt.savefig('plot_output.png')