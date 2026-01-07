from playwright.sync_api import sync_playwright, expect

def verify_tool_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the tool
        page.goto("http://localhost:8080/tools/photo-to-comic.html")

        # Check if the title is correct
        expect(page).to_have_title("Vector Tool")

        # Check for the new slider "Gap Correction"
        gap_slider = page.locator("#input-gap")
        expect(gap_slider).to_be_visible()

        # Check for the label text
        label = page.get_by_text("Gap Correction (Stroke)")
        expect(label).to_be_visible()

        # Take a screenshot of the controls
        page.screenshot(path="verification/ui_verification.png")
        print("UI verification successful, screenshot saved.")

        browser.close()

if __name__ == "__main__":
    verify_tool_ui()
