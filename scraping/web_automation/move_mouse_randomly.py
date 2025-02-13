
import random
import time
import logging


def move_mouse_randomly(driver):
    """Moves the mouse cursor randomly like a human."""
    
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        action = ActionChains(driver)

        for _ in range(random.randint(5, 15)):  # Random movement count
            x_offset = random.randint(-300, 300)
            y_offset = random.randint(-200, 200)
            action.move_by_offset(x_offset, y_offset).perform()
            time.sleep(random.uniform(0.1, 0.5))
        
        logging.info("✅ Human-like mouse movements simulated.")
    
    except Exception as e:
        logging.warning(f"⚠️ Mouse movement simulation failed: {e}")