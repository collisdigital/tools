import os
import glob
import sys
import re
import shutil

# Constants
REPO = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')

INDEX_PLACEHOLDER_LINKS = '{{ LINKS_PLACEHOLDER }}'

FOOTER_PLACEHOLDER_REPO_URL = '{{ REPO_URL }}'
FOOTER_PLACEHOLDER_SOURCE_URL = '{{ SOURCE_URL }}'
FOOTER_PLACEHOLDER_VIEW_TEXT = '{{ VIEW_TEXT }}'

LINK_PLACEHOLDER_FILENAME = '{{ FILENAME }}'
LINK_PLACEHOLDER_TITLE = '{{ TITLE }}'

# Determine the absolute path to the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'index_template.html')
FOOTER_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'footer_template.html')
LINK_TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'link_template.html')
OUTPUT_FILE = 'index.html'
DIST_DIR = 'dist'

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
        with open(FOOTER_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            footer_html = t.read()
    except FileNotFoundError:
        print(f"Error: {FOOTER_TEMPLATE_PATH} not found.")
        sys.exit(1)

    return footer_html.replace(FOOTER_PLACEHOLDER_REPO_URL, repo_url)\
                      .replace(FOOTER_PLACEHOLDER_SOURCE_URL, source_url)\
                      .replace(FOOTER_PLACEHOLDER_VIEW_TEXT, view_text)

def remove_existing_footer(content):
    """Removes the auto-generated footer from the content if it exists."""
    # Regex to match the footer block:
    # Starts with the specific comment, matches anything (dotall), ends with </footer>
    pattern = r'\s*<!-- Auto-generated Footer -->.*</footer>'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def main():
    # 0. Create dist directory
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # 1. List HTML files in the root
    html_files = [f for f in glob.glob("*.html") if f != OUTPUT_FILE]
    html_files.sort()

    # 2. Read Link Template
    try:
        with open(LINK_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            link_template = t.read()
    except FileNotFoundError:
        print(f"Error: {LINK_TEMPLATE_PATH} not found.")
        sys.exit(1)

    # 3. Generate Link List
    links_html = ""
    for f in html_files:
        # Prettify title
        title = f.replace("-", " ").replace("_", " ").replace(".html", "").title()

        links_html += link_template.replace(LINK_PLACEHOLDER_FILENAME, f)\
                                   .replace(LINK_PLACEHOLDER_TITLE, title)

    # 4. Read Index Template
    try:
        with open(INDEX_TEMPLATE_PATH, "r", encoding="utf-8") as t:
            template_content = t.read()
    except FileNotFoundError:
        print(f"Error: {INDEX_TEMPLATE_PATH} not found.")
        sys.exit(1)

    # 5. Prepare index.html content
    index_content = template_content.replace(INDEX_PLACEHOLDER_LINKS, links_html)
    
    # 6. Process all files (including generated index) and write to dist
    print(f"Processing {len(html_files) + 1} files into {DIST_DIR}...")
    
    # Process regular HTML files
    for f_name in html_files:
        with open(f_name, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = remove_existing_footer(content)
        footer = get_footer_html(f_name, is_index=False)
        
        if "</body>" in content:
            parts = content.rsplit("</body>", 1)
            new_content = parts[0] + footer + "\n</body>" + parts[1]
        else:
            new_content = content + footer
            
        with open(os.path.join(DIST_DIR, f_name), "w", encoding="utf-8") as f:
            f.write(new_content)

    # Process index.html
    index_content = remove_existing_footer(index_content)
    footer = get_footer_html(OUTPUT_FILE, is_index=True)
    if "</body>" in index_content:
        parts = index_content.rsplit("</body>", 1)
        new_content = parts[0] + footer + "\n</body>" + parts[1]
    else:
        new_content = index_content + footer
        
    with open(os.path.join(DIST_DIR, OUTPUT_FILE), "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Done.")

if __name__ == "__main__":
    main()
