import os
import glob

# Configuration
REPO = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
BRANCH = 'main'

def get_footer_html(filename, is_index=False):
    """Generates the footer HTML with inline styles for maximum compatibility."""

    # Determine the "View Source" link
    if is_index:
        # For index.html, we link to the repository root
        source_url = f"https://github.com/{REPO}"
        view_text = "Repository Root"
    else:
        # For other files, link to the specific file blob
        source_url = f"https://github.com/{REPO}/blob/{BRANCH}/{filename}"
        view_text = "View Source"

    repo_url = f"https://github.com/{REPO}"

    # Inline SVG for GitHub Icon (Font Awesome style)
    # Added width/height attributes and inline style for sizing
    github_icon = """<svg aria-hidden="true" focusable="false" data-prefix="fab" data-icon="github" width="16" height="16" style="display: inline-block; vertical-align: text-bottom; width: 1em; height: 1em;" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><path fill="currentColor" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path></svg>"""

    html = f"""
    <!-- Auto-generated Footer -->
    <footer style="margin-top: 3rem; padding-top: 2rem; padding-bottom: 2rem; border-top: 1px solid #e5e7eb; background-color: #f9fafb; text-align: center; font-size: 0.875rem; color: #4b5563; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
            <span style="font-weight: 500;">&copy; Chris Collis</span>
            <span style="color: #d1d5db;">|</span>
            <a href="{repo_url}" style="display: flex; align-items: center; gap: 0.25rem; text-decoration: none; color: inherit; transition: color 0.2s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='inherit'" target="_blank" rel="noopener noreferrer">
                {github_icon} <span>GitHub Repo</span>
            </a>
            <span style="color: #d1d5db;">|</span>
            <a href="{source_url}" style="text-decoration: none; color: inherit; transition: color 0.2s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='inherit'" target="_blank" rel="noopener noreferrer">
                {view_text}
            </a>
        </div>
    </footer>
    """
    return html

def main():
    # 1. List HTML files in the root
    html_files = [f for f in glob.glob("*.html") if f != "index.html"]
    html_files.sort()

    # 2. Generate Link List for Template
    links_html = ""
    for f in html_files:
        # Prettify title
        title = f.replace("-", " ").replace("_", " ").replace(".html", "").title()

        links_html += f"""
        <a href="{f}" class="block p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-100 group">
            <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-gray-800 group-hover:text-blue-600 transition-colors">{title}</h2>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 group-hover:text-blue-600 transition-colors"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
            <p class="text-gray-500 text-sm mt-2 font-mono bg-gray-50 inline-block px-2 py-1 rounded border border-gray-200">{f}</p>
        </a>
        """

    # 3. Read Template
    try:
        with open("scripts/index_template.html", "r") as t:
            template_content = t.read()
    except FileNotFoundError:
        print("Error: scripts/index_template.html not found.")
        return

    # 4. Write index.html
    index_content = template_content.replace("{{ LINKS_PLACEHOLDER }}", links_html)
    with open("index.html", "w") as f:
        f.write(index_content)

    # Add index.html to list of files to process for footer
    html_files_to_modify = html_files + ["index.html"]

    # 5. Inject Footer
    print(f"Injecting footer into {len(html_files_to_modify)} files...")
    for f_name in html_files_to_modify:
        with open(f_name, "r") as f:
            content = f.read()

        is_index = (f_name == "index.html")
        footer = get_footer_html(f_name, is_index)

        # Inject before </body>
        if "</body>" in content:
            # Use rsplit to replace only the last occurrence
            parts = content.rsplit("</body>", 1)
            new_content = parts[0] + footer + "\n</body>" + parts[1]
        else:
            # Fallback: Append to end
            new_content = content + footer

        with open(f_name, "w") as f:
            f.write(new_content)

    print("Done.")

if __name__ == "__main__":
    main()
