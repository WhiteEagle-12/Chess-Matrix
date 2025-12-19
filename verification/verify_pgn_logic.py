from playwright.sync_api import sync_playwright

def verify_auto_orient(page):
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

    # Open PGN Modal
    page.click("button[onclick=\"document.getElementById('pgnModal').classList.remove('hidden')\"]")
    page.wait_for_selector("#pgnModal", state="visible")

    # Load PGN
    pgn = """[Event "Test"]
[White "DeepBlue"]
[Black "Kasparov"]
[Result "0-1"]

1. e4 c5 0-1"""

    page.fill("#pgnInput", pgn)
    page.click("#loadPgnBtn")

    # Wait a moment for the timeout/process in loadPGN
    page.wait_for_timeout(1000)

    # DEBUG: Get Headers and Username
    debug_info = page.evaluate("""() => {
        return {
            headers: game.header(),
            storedUser: localStorage.getItem('chess_username'),
            boardOrient: board.orientation()
        }
    }""")
    print(f"DEBUG INFO: {debug_info}")

    if debug_info['boardOrient'] != "black":
        raise Exception(f"Expected orientation 'black' but got '{debug_info['boardOrient']}'")

    print("Verification Passed: Board correctly oriented to Black.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_auto_orient(page)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
        finally:
            browser.close()
