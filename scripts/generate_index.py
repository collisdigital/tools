import os
import glob

# Constants
REPO = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
BRANCH = 'main'

INDEX_PLACEHOLDER_LINKS = '{{ LINKS_PLACEHOLDER }}'

FOOTER_PLACEHOLDER_REPO_URL = '{{ REPO_URL }}'
FOOTER_PLACEHOLDER_SOURCE_URL = '{{ SOURCE_URL }}'
FOOTER_PLACEHOLDER_VIEW_TEXT = '{{ VIEW_TEXT }}'

LINK_PLACEHOLDER_FILENAME = '{{ FILENAME }}'
LINK_PLACEHOLDER_TITLE = '{{ TITLE }}'

INDEX_TEMPLATE_PATH = 'scripts/index_template.html'
FOOTER_TEMPLATE_PATH = 'scripts/footer_template.html'
LINK_TEMPLATE_PATH = 'scripts/link_template.html'
OUTPUT_FILE = 'index.html'

def get_footer_html(filename, is_index=False):
    """Generates the footer HTML using the template."""

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

    try:
        with open(FOOTER_TEMPLATE_PATH, "r") as t:
            footer_html = t.read()
    except FileNotFoundError:
        print(f"Error: {FOOTER_TEMPLATE_PATH} not found.")
        return ""

    return footer_html.replace(FOOTER_PLACEHOLDER_REPO_URL, repo_url)\
                      .replace(FOOTER_PLACEHOLDER_SOURCE_URL, source_url)\
                      .replace(FOOTER_PLACEHOLDER_VIEW_TEXT, view_text)

def main():
    # 1. List HTML files in the root
    html_files = [f for f in glob.glob("*.html") if f != OUTPUT_FILE]
    html_files.sort()

    # 2. Read Link Template
    try:
        with open(LINK_TEMPLATE_PATH, "r") as t:
            link_template = t.read()
    except FileNotFoundError:
        print(f"Error: {LINK_TEMPLATE_PATH} not found.")
        return

    # 3. Generate Link List
    links_html = ""
    for f in html_files:
        # Prettify title
        title = f.replace("-", " ").replace("_", " ").replace(".html", "").title()

        links_html += link_template.replace(LINK_PLACEHOLDER_FILENAME, f)\
                                   .replace(LINK_PLACEHOLDER_TITLE, title)

    # 4. Read Index Template
    try:
        with open(INDEX_TEMPLATE_PATH, "r") as t:
            template_content = t.read()
    except FileNotFoundError:
        print(f"Error: {INDEX_TEMPLATE_PATH} not found.")
        return

    # 5. Write index.html
    index_content = template_content.replace(INDEX_PLACEHOLDER_LINKS, links_html)
    with open(OUTPUT_FILE, "w") as f:
        f.write(index_content)

    # Add index.html to list of files to process for footer
    html_files_to_modify = html_files + [OUTPUT_FILE]

    # 6. Inject Footer
    print(f"Injecting footer into {len(html_files_to_modify)} files...")
    for f_name in html_files_to_modify:
        with open(f_name, "r") as f:
            content = f.read()

        is_index = (f_name == OUTPUT_FILE)
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
