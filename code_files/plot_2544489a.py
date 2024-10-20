import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# Create a box plot of Screen On Time (hours/day) by Gender
plt.figure(figsize=(8, 6))
df.boxplot(column='Screen On Time (hours/day)', by='Gender')
plt.title('Screen On Time (hours/day) by Gender')
plt.xlabel('Gender')
plt.ylabel('Screen On Time (hours/day)')
plt.show()
plt.savefig('plot_output.png')