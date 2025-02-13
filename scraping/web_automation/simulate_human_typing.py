
import time 

def simulate_human_typing(element, text, speed_factor=1):
    """Simulates human typing with random delays."""
    
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2) * speed_factor)  # Random typing delay