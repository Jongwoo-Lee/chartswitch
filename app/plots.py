import matplotlib.pyplot as plt

from app import PriceManager
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()

def update_plot(frame):
    df = PriceManager().price_data
    if not df.empty:
      df_tail = df.tail(30)
      ax.clear()  # Clear the previous plot
      ax.table(cellText=df_tail.values,
             colLabels=df_tail.columns,
             cellLoc='center',
             loc='center')
      ax.axis('off')  # Turn off axis
      ax.set_title('Real-time DataFrame Table')

ani = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)

def price_plot():
     return plt
