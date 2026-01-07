from playwright.sync_api import sync_playwright

def verify_bg_controls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the tool
        page.goto("file:///app/tools/photo-to-cell-shading.html")

        # 1. Check if the Background Control exists
        bg_mode_select = page.locator("#input-bg-mode")
        if bg_mode_select.count() == 0:
            print("Error: Background Mode select not found")
            browser.close()
            return

        print("Found Background Mode select")

        # 2. Check if default is 'none'
        value = bg_mode_select.input_value()
        if value != 'none':
            print(f"Error: Default value is {value}, expected 'none'")
        else:
            print("Default value is 'none'")

        # 3. Select 'custom' and check if color picker appears
        bg_mode_select.select_option("custom")

        color_input = page.locator("#input-bg-color")
        if color_input.is_visible():
            print("Color input is visible after selecting 'custom'")
        else:
            print("Error: Color input is NOT visible after selecting 'custom'")

        # 4. Take a screenshot of the UI with controls
        page.screenshot(path="verification/verify_bg_ui.png")
        print("Screenshot saved to verification/verify_bg_ui.png")

        browser.close()

if __name__ == "__main__":
    verify_bg_controls()
