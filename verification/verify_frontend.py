from playwright.sync_api import sync_playwright
import os

def verify_settings(page):
    page.goto("http://localhost:8080/index.html")

    # On fresh load, settings modal might auto-open if no API key
    # Wait a bit to see if it appears
    try:
        page.wait_for_selector("#settingsModal", state="visible", timeout=2000)
        print("Modal auto-opened.")
    except:
        print("Modal did not auto-open, clicking button.")
        page.click("button[onclick='openSettings()']")
        page.wait_for_selector("#settingsModal", state="visible")

    # 2. Check if Username Input exists
    username_input = page.locator("#usernameInput")
    if not username_input.is_visible():
        raise Exception("Username Input not visible")

    # 3. Enter Username and Save
    username_input.fill("Hikaru")
    page.click("#saveKeyBtn")

    # Wait for modal to close
    page.wait_for_selector("#settingsModal", state="hidden")

    # 4. Verify LocalStorage
    stored = page.evaluate("localStorage.getItem('chess_username')")
    if stored != "Hikaru":
        raise Exception(f"Failed to save username. Got: {stored}")

    # 5. Open Settings Again to verify persistence
    page.click("button[onclick='openSettings()']")
    page.wait_for_selector("#settingsModal", state="visible")
    val = page.locator("#usernameInput").input_value()
    if val != "Hikaru":
        raise Exception(f"Failed to load username. Got: {val}")

    # 6. Take Screenshot of Settings Modal
    if not os.path.exists("verification"): os.makedirs("verification")
    page.screenshot(path="verification/settings_modal.png")
    print("Settings Verification Passed.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_settings(page)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
        finally:
            browser.close()
