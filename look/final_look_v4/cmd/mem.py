import sys, shutil; sys.path.insert(0, r'C:\Users\raresense\sim_wbt'); import isaac_slot
print('RAM avail / commit free GB', isaac_slot.ram(), 'C: free', round(shutil.disk_usage('C:/').free/2**30, 1))
