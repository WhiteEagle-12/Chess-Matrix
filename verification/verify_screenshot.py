from playwright.sync_api import sync_playwright
import os

def verify_board_ui(page):
    page.goto("http://localhost:8080/index.html")

    # Set Username
    try:
        page.wait_for_selector("#settingsModal", state="visible", timeout=2000)
    except:
        page.click("button[onclick='openSettings()']")
        page.wait_for_selector("#settingsModal", state="visible")

    page.fill("#usernameInput", "Kasparov")
    page.click("#saveKeyBtn")
    page.wait_for_selector("#settingsModal", state="hidden")

    # Load PGN
    page.click("button[onclick=\"document.getElementById('pgnModal').classList.remove('hidden')\"]")
    page.wait_for_selector("#pgnModal", state="visible")

    pgn = """[Event "Test"]
[White "DeepBlue"]
[Black "Kasparov"]
[Result "0-1"]

1. e4 c5 0-1"""

    page.fill("#pgnInput", pgn)
    page.click("#loadPgnBtn")

    page.wait_for_timeout(1000) # Wait for processing

    # Check orientation logic
    orient = page.evaluate("board.orientation()")
    print(f"Board is oriented: {orient}")

    if orient != "black":
         raise Exception("Board should be black")

    # Take Screenshot of the board to visually verify flip
    if not os.path.exists("verification"): os.makedirs("verification")
    page.screenshot(path="verification/flipped_board.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_board_ui(page)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
        finally:
            browser.close()
