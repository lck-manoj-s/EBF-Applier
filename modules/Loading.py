import sys
import time

def Loading(duration=10):
    # Calculate the time interval for each increment
    total_steps = duration
    sleep_time = duration / total_steps
    
    # Print initial  message
    sys.stdout.write('Loading, please wait...  0%')
    sys.stdout.flush()
    
    # Update percentage progressively
    for i in range(total_steps + 1):
        progress = i / total_steps
        percentage = int(progress * 100)
        
        # Update the display
        sys.stdout.write(f'\rLoading, please wait... {percentage}%')
        sys.stdout.flush()
        
        # Wait before next update
        time.sleep(sleep_time)
