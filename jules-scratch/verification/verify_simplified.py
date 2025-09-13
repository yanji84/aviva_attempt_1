from playwright.sync_api import sync_playwright, expect

def run_simplified_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("http://localhost:8501", timeout=10000)

            # Wait for the main page to load
            expect(page.get_by_text("QUOTE SEARCH")).to_be_visible(timeout=10000)
            page.screenshot(path="jules-scratch/verification/01_simplified_start.png")

            # Enter the valid reference number
            reference_input = page.get_by_role("textbox", name="Reference Number")
            reference_input.fill("P11162731HAB0003")

            # Click the search button
            page.get_by_role("button", name="Search").click()

            # Wait for navigation to the results page with a longer timeout
            expect(page.get_by_text("Prospect")).to_be_visible(timeout=15000)
            page.screenshot(path="jules-scratch/verification/02_simplified_results.png")

            print("Verification script completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_simplified_verification()
