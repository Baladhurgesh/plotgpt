import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
df = pd.read_csv('/Users/bala/Downloads/user_behavior_dataset.csv')

# get the count of each device model
device_models = df['device model'].value_counts()

# plot the distribution of device models
plt.figure(figsize=(10,6))
device_models.plot(kind='bar')
plt.title('distribution of device models')
plt.xlabel('device model')
plt.ylabel('count')
plt.show()
plt.savefig('plot_output.png')