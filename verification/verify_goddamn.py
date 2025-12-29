from playwright.sync_api import sync_playwright
import os

def verify_goddamn_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the generated file
        cwd = os.getcwd()
        file_path = f"file://{cwd}/dist/goddamn.html"
        page.goto(file_path)

        # 1. Verify Structure: Board and Footers
        # Check that the board exists
        assert page.is_visible("#board"), "Board not visible"

        # Check for the hardcoded footer
        hardcoded_footer_text = "Get the hell out of my office!"
        assert page.get_by_text(hardcoded_footer_text).is_visible(), "Hardcoded footer not found"

        # Check for the injected global footer (e.g. "All Tools" link)
        all_tools_link = page.get_by_role("link", name="All Tools")
        assert all_tools_link.is_visible(), "Global footer 'All Tools' link not found"

        # 2. Verify Counter
        counter = page.locator("#goddamn-counter")
        assert counter.is_visible(), "Counter not visible"

        count_value = page.locator("#goddamn-count-value")
        assert count_value.inner_text() == "0", "Initial count should be 0"

        # 3. Simulate Click
        # Click a card
        card = page.locator(".character-card").first
        card.click()

        # Wait for count update
        page.wait_for_function("document.getElementById('goddamn-count-value').innerText === '1'")
        assert count_value.inner_text() == "1", "Count did not increment to 1"

        # 4. Take Screenshots
        # Full page to see footer placement
        page.screenshot(path="verification/full_page.png", full_page=True)

        # Close up of counter
        counter.screenshot(path="verification/counter.png")

        print("Verification script completed successfully.")
        browser.close()

if __name__ == "__main__":
    verify_goddamn_page()
