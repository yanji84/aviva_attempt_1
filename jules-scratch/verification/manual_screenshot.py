from playwright.sync_api import sync_playwright, expect

def take_screenshot(url, path, text_to_wait_for):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=10000)
            expect(page.get_by_text(text_to_wait_for)).to_be_visible(timeout=10000)
            page.screenshot(path=path)
            print(f"Screenshot saved to {path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    # Take a screenshot of the results page
    take_screenshot("http://localhost:8501", "jules-scratch/verification/02_manual_results_page.png", "Quote Search Results")
