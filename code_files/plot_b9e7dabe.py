import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
df = pd.read_csv('user_behavior_dataset.csv')

# get the distribution of device models
device_model_dist = df['device model'].value_counts()

# plot the distribution
plt.figure(figsize=(10,6))
device_model_dist.plot(kind='bar')
plt.title('distribution of device models')
plt.xlabel('device model')
plt.ylabel('count')
plt.show()
plt.savefig('plot_output.png')