import pyautogui
import time
import random
import threading
import keyboard

# Shared variable to track the pause state
is_paused = False
start_time = time.time()  # Record the script's start time

def listen_for_pause():
    """Background thread to listen for the '`' key."""
    global is_paused
    while True:
        if keyboard.is_pressed('`'):
            is_paused = not is_paused
            state = "paused" if is_paused else "resumed"
            print(f"Script {state}.")
            time.sleep(0.5)  # Debounce to avoid rapid toggling

def random_pause():
    """Generate a random pause duration between 3 and 8 seconds."""
    return random.uniform(.5, 1)

# Note -120+(-120) notation is important to mimic Human Finger Scroll Function
# Rather than input of singualar Values
def random_scroll_amount():
    """Choose a random scroll amount from -120, -240, or -360."""
    return random.choice([-120, -120, -120, -120+(-120), -120+(-120), -120+(-120),
	-120+(-120)+(-120),-120+(-120)+(-120)+(-120), -120+(-120)+(-120),-120+(-120)+(-120)+(-120)])


def format_elapsed_time(elapsed):
    """Format elapsed time into HH:MM:SS."""
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def continuous_scroll():
    """Main scrolling function."""
    global is_paused, start_time
    print("Press '`' to pause or resume. Press Ctrl+C to stop.")

    try:
        while True:
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            formatted_time = format_elapsed_time(elapsed_time)
            print(f"Elapsed Time: {formatted_time}", end="\r")  # Print the timer in real time
            
            if not is_paused:
                # Scroll by a random amount
                scroll_amount = random_scroll_amount()
                pyautogui.scroll(scroll_amount)
                print(f"\nScrolled by {scroll_amount}.")
                
                # Pause for a random duration between 3 and 8 seconds
                pause_duration = random_pause()
                print(f"Pausing for {pause_duration:.2f} seconds.")
                time.sleep(pause_duration)
            else:
                time.sleep(0.1)  # Short sleep to reduce CPU usage while paused
    except KeyboardInterrupt:
        print("\nScroll script stopped by user.")

if __name__ == "__main__":
    # Start the key listening thread
    listener_thread = threading.Thread(target=listen_for_pause, daemon=True)
    listener_thread.start()
    
    # Start the scrolling function
    continuous_scroll()
