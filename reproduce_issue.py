
import json
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # problematic prompt content
    prompt_text = """# 🧪 Testing Improvement Task

You are a testing-focused agent. Your mission is to analyze and implement a testing improvement that will increase the reliability and coverage of the codebase.

## Task Details

**File:** `frontend/src/components/grades/SkillList.tsx:11`
**Issue:** Add tests for SkillList component

**Language:** javascript

**Current Code:**
javascript
export function SkillList({ grade, onAddSkill, onEditSkill, onDeleteSkill }: SkillListProps) {
 const [hoveredSkill, setHoveredSkill] = useState<string | null>(null)

 return (
 <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 h-full flex flex-col">
 <div className="flex justify-between items-center mb-6 border-b border-gray-100 pb-4">
 <div>
 <h2 className="text-xl font-bold text-gray-900">{grade.name}</h2>
 {grade.description && <p className="text-gray-500 mt-1">{grade.description}</p>}
 </div>
 <button
 onClick={onAddSkill}
 className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
 >
 <Plus size={18} />
 <span>Add Skill</span>
 </button>
 </div>
"""

    mock_sessions = {
        "sessions": [
            {
                "name": "projects/p/locations/l/sessions/session-123",
                "state": "ACTIVE",
                "prompt": prompt_text,
                "createTime": "2023-10-27T10:00:00Z",
                "updateTime": "2023-10-27T10:05:00Z",
                "sourceContext": {
                    "source": "sources/github/owner/repo"
                }
            }
        ]
    }

    # Intercept requests to sessions endpoint
    def handle_sessions(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_sessions)
        )

    page.route("**/sessions?pageSize=20", handle_sessions)

    # Load the page
    # Assuming tools/google-jules-dashboard.html is in current directory or relative path
    # I'll use absolute path in the tool call, but here relative to repo root
    import os
    cwd = os.getcwd()
    file_url = f"file://{cwd}/tools/google-jules-dashboard.html"

    page.goto(file_url)

    # Set API key in local storage to trigger fetchSessions
    page.evaluate("localStorage.setItem('jules_api_key', 'dummy-key')")

    # Reload to trigger the DOMContentLoaded logic
    page.reload()

    # Wait for session list to populate
    page.wait_for_selector("#sessionList")

    # Give it a moment to render
    page.wait_for_timeout(2000)

    # Take screenshot
    page.screenshot(path="reproduction.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
