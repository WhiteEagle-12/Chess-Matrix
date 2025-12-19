from playwright.sync_api import sync_playwright
import time

def verify(page):
    page.goto("http://localhost:8080")

    # Wait for board to load
    page.wait_for_selector("#board")

    # Inject JS to trigger heatmap
    page.evaluate("""
        const g = new Chess();
        g.move('e4');
        g.move('e5');
        g.move('Nf3');
        g.move('Nc6');
        g.move('Bb5'); // Ruy Lopez

        // Analyze position
        const report = HeatMap.analyze(g);

        // Mock analysisData
        analysisData = [{
            control: report,
            color: 'w', // Last move was White (Bb5)
            fenBefore: '...'
        }];
        currentMoveIndex = 0;
        isHeatmapActive = true;

        renderHeatmap();
    """)

    # Wait for CSS transition if any, though heatmap is immediate
    time.sleep(1)

    page.screenshot(path="verification/heatmap.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    verify(page)
    browser.close()
