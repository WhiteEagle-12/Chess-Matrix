
import json
from playwright.sync_api import sync_playwright

def verify_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 1. Inject Data into localStorage
        # We need to navigate first to set localStorage for the domain
        page.goto("http://localhost:8080/index.html")

        sample_game = {
            "id": "test_game_id",
            "pgn": "[Event \"Test Game\"] [Site \"Chess.com\"] [Date \"2023.10.27\"] [Round \"-\"] [White \"Hero\"] [Black \"Villain\"] [Result \"1-0\"] 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 h6 15. Bh4 Re8 16. a3 Nh7 17. Bxe7 Qxe7 18. Qd2 exd4 19. Nxd4 Nc5 20. Bc2 Nf6 21. Nf5 Qe6 22. Qxd6 Qxd6 23. Nxd6 Re7 24. b4 Ne6 25. e5 Ne8 26. Nce4 Nd4 27. Bd3 Bc8 28. Nc5 Nc7 29. f4 Nce6 30. Nxe6 Bxe6 31. Be4 Rea7 32. Rad1 Nb3 33. f5 Bd5 34. Bxd5 cxd5 35. Nxb5 Rd7 36. Rd3 1-0",
            "opening": "Ruy Lopez: Closed Defense",
            "date": "10/27/2023",
            "gameStats": {
                "white": { "acpl": 15, "accuracy": 92.5, "archetype": { "label": "The Grandmaster", "icon": "fa-chess-king" } },
                "black": { "acpl": 45, "accuracy": 86.0, "archetype": { "label": "The Magician", "icon": "fa-wand-magic-sparkles" } },
                "complexity": "3.8"
            },
            "analysisData": [
                { "classification": "Best", "eval": "0.20", "color": "w", "san": "e4" },
                # ... (minimal data needed for logic) ...
                { "classification": "Blunder", "eval": "M2", "color": "b", "san": "Rd3", "isMate": False }
                # Last move dictates result badge logic
            ],
            "geminiComments": {}
        }

        # Inject into localStorage
        page.evaluate(f"localStorage.setItem('chess_coach_library', JSON.stringify([{json.dumps(sample_game)}]))")

        # Reload to pick up data (though code reads on Sidebar open, let's refresh to be sure)
        page.reload()

        # 2. Verify Sidebar
        # Click Hamburger
        page.click("button[onclick='toggleSidebar()']")
        page.wait_for_timeout(500) # Wait for animation

        # Screenshot Sidebar
        page.screenshot(path="verification/sidebar_test.png")
        print("Sidebar screenshot taken.")

        # 3. Verify Match Header & Loading
        # Click the game in the list
        page.click("#gameListContainer > div")
        page.wait_for_timeout(500) # Wait for load and sidebar close

        # Check if Match Header is visible
        header = page.locator("#matchHeader")
        if header.is_visible():
            print("Match Header is visible.")
        else:
            print("Match Header NOT visible.")

        # Screenshot Match Header area
        page.screenshot(path="verification/match_header_test.png")
        print("Match Header screenshot taken.")

        browser.close()

if __name__ == "__main__":
    verify_ui()
