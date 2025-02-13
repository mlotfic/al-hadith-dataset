
import random
import time

def simulate_human_scroll(driver, speed_factor=1):
    """Scrolls the page like a human, smoothly and unpredictably."""
    
    total_scrolls = random.randint(5, 15)  # Number of small scrolls
    for _ in range(total_scrolls):
        scroll_amount = random.randint(200, 600)  # Random scroll height
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.3, 1.5) * speed_factor)  # Varying delay
