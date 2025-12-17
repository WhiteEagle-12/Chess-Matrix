
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Open the index.html file
        page.goto('file://' + os.path.abspath('index.html'))

        # Verify Match Header is hidden initially
        match_header = page.locator('#matchHeader')
        assert not match_header.is_visible(), 'Match Header should be hidden initially'

        # Verify Sidebar toggle
        sidebar_btn = page.locator('button[title=\'Game Library\']')
        sidebar = page.locator('#librarySidebar')
        overlay = page.locator('#sidebarOverlay')

        # Sidebar should be closed (-translate-x-full)
        assert 'translate-x-full' in sidebar.get_attribute('class'), 'Sidebar should be closed'

        # Click toggle
        sidebar_btn.click()

        # Sidebar should be open (no -translate-x-full)
        # Note: Playwright might not see class updates instantly without a wait, but we can check visibility
        page.wait_for_timeout(500) # wait for transition

        # Verify Sidebar is visible
        assert sidebar.is_visible()

        # Take Screenshot 1: Sidebar Open
        page.screenshot(path='verification/sidebar_open.png')

        # Mock Game Data and force UI update to show Match Header
        page.evaluate('''() => {
            const white = { accuracy: '92.5', archetype: { label: 'The Sniper', icon: 'fa-crosshairs' } };
            const black = { accuracy: '65.0', archetype: { label: 'The Gambler', icon: 'fa-dice' } };
            const complexity = '3.5';

            // Mock function call
            updateMatchHeader(white, black, complexity);

            // Close sidebar for clear view
            toggleSidebar();
        }''')

        page.wait_for_timeout(500)

        # Verify Match Header is now visible
        assert match_header.is_visible(), 'Match Header should be visible after update'

        # Take Screenshot 2: Match Header Visible
        page.screenshot(path='verification/match_header.png')

        browser.close()

if __name__ == '__main__':
    run()
