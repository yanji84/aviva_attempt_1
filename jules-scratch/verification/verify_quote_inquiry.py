from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to the app and take a screenshot of the blank page.
        page.goto("http://localhost:8501")
        page.wait_for_selector("text=QUOTE SEARCH")
        page.screenshot(path="jules-scratch/verification/01_blank_inquiry_page.png")

        # 2. Enter the valid reference number and verify navigation.
        reference_input = page.get_by_role("textbox", name="Reference Number")
        reference_input.fill("P11162731HAB0003")
        page.get_by_role("button", name="Search").click()

        # Wait for navigation to the results page
        expect(page.get_by_text("Prospect")).to_be_visible()
        page.screenshot(path="jules-scratch/verification/02_results_page.png")

        # 3. Go back and test invalid reference number.
        prev_button = page.get_by_role("button", name="Prev")
        prev_button.click()

        # Wait for the inquiry page to load
        expect(page.get_by_text("QUOTE SEARCH")).to_be_visible()

        # The radio button for 'Reference Number' should still be selected.
        reference_input_again = page.get_by_role("textbox", name="Reference Number")
        reference_input_again.fill("INVALID123")
        page.get_by_role("button", name="Search").click()

        # Check for the "No result found" message
        expect(page.get_by_text("No result found")).to_be_visible()
        page.screenshot(path="jules-scratch/verification/03_invalid_reference.png")

        browser.close()

if __name__ == "__main__":
    run_verification()
