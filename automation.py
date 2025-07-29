from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def wait_for_element_clickable(driver, by, identifier, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, identifier)))

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)
    try:
        # Step 1: Open the site
        driver.get("https://indeedemo-fyc.watch.indee.tv/")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Page loaded.")


        # Optional: Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"🔍 Found {len(iframes)} iframe(s). Switching to first.")
            driver.switch_to.frame(iframes[0])

        # Step 2: Enter the PIN
        try:
            pin_input = wait_for_element_clickable(driver, By.NAME, "pin")
        except:
            pin_input = wait_for_element_clickable(driver, By.CSS_SELECTOR, "input[type='text']")

        driver.execute_script("arguments[0].scrollIntoView(true);", pin_input)
        pin_input.click()
        pin_input.send_keys("WVMVHWBS")
        print("✅ PIN entered.")

        submit_btn = wait_for_element_clickable(driver, By.XPATH, "//button[contains(text(),'Enter')]")
        submit_btn.click()
        print("✅ Logged in.")

        # Step 3: Click "Test Automation Project"
        project = wait_for_element_clickable(driver, By.XPATH, "//*[contains(text(),'Test Automation Project')]")
        project.click()
        print("✅ Opened Test Automation Project.")

        # Step 4: Play video
        from selenium.webdriver.common.action_chains import ActionChains

        try:
            # Hover over the video container to reveal controls
            video_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='video'], div[class*='player']")))
            ActionChains(driver).move_to_element(video_container).perform()
            print("🖱 Hovered over video.")

            # Wait for play button to become clickable
            play_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@aria-label, 'Play') or contains(@class, 'play')]"
            )))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play_btn)
            time.sleep(1)
            play_btn.click()
            print("▶️ Video playing...")

            time.sleep(10)  # Let video play for 10 seconds

        except Exception as e:
            # Save screenshot and page HTML
            driver.save_screenshot("step4_play_error.png")
            with open("step4_debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("❌ Step 4 failed. Screenshot: step4_play_error.png | Page: step4_debug_page.html")
            raise e

        # Step 5: Pause video
        pause_btn = wait_for_element_clickable(driver, By.CSS_SELECTOR, "button[class*='pause']")
        pause_btn.click()
        print("⏸ Paused after 10 seconds.")

        # Step 6: Click "Continue Watching"
        continue_btn = wait_for_element_clickable(driver, By.XPATH, "//button[contains(text(),'Continue Watching')]")
        continue_btn.click()
        print("🔁 Clicked Continue Watching.")
        time.sleep(5)

        # Step 7: Pause again
        pause_btn = wait_for_element_clickable(driver, By.CSS_SELECTOR, "button[class*='pause']")
        pause_btn.click()
        print("⏸ Paused again.")

        # Step 8: Press Back button
        back_btn = wait_for_element_clickable(driver, By.CSS_SELECTOR, "button[class*='back']")
        back_btn.click()
        print("⬅️ Navigated back.")

        # Step 9: Logout
        logout_btn = wait_for_element_clickable(driver, By.XPATH, "//button[contains(text(),'Logout')]")
        logout_btn.click()
        print("✅ Logged out.")

    except Exception as e:
        print("❌ Error encountered:", e)
        screenshot_path = os.path.join(os.getcwd(), "error_screenshot.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to {screenshot_path}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()
