# AI Agent Guide

Welcome, Agent. This repository is a collection of standalone, single-file HTML tools. To maintain consistency and ensure your contributions are correctly indexed, please follow these guidelines.

## Adding a New Tool

1.  **Standalone File**: Create a single `.html` file in the `tools/` directory.
2.  **Modern UI**: Use **Tailwind CSS** (via CDN) for styling and **Lucide Icons** for iconography. Aim for a "glassmorphism" or clean Material Design aesthetic.
3.  **Metadata**: Every tool MUST include a `TOOL_OVERVIEW` metadata block at the very beginning of the file. This block is used by the index generator to create the dashboard.
    - Copy the structure from `TOOL_OVERVIEW_TEMPLATE`.
    - Ensure the JSON is valid.
4.  **Local Storage**: For configuration (like API keys), use `localStorage` to keep the tool standalone and serverless.

## Metadata Format

The `TOOL_OVERVIEW` block should look like this:

```html
<!--
TOOL_OVERVIEW_START
{
  "name": "Your Tool Name",
  "description": "What it does.",
  "functionality": {
    "feature_name": "Short description of feature"
  },
  "dependencies": ["Tailwind CSS", "Lucide Icons"],
  "last_updated": "2025-12-26"
}
TOOL_OVERVIEW_END
-->
```

## Maintenance Tasks

### Regenerating the Index
After adding or modifying a tool, you must regenerate the `index.html` file in the `dist/` directory.

```bash
python3 scripts/generate_index.py
```

The script performs the following:
1.  Scans the `tools/` directory for `.html` files.
2.  Extracts `TOOL_OVERVIEW` metadata.
3.  Injects an auto-generated footer into every tool.
4.  Generates a rich index page in `dist/index.html`.

### Testing
To preview your changes, serve the `dist` directory:

```bash
python3 -m http.server --directory dist
```

## Style Guidelines
- **Font**: Prefer 'Inter' or 'Roboto'.
- **Interactivity**: Use vanilla JavaScript. Avoid heavy frameworks unless absolutely necessary.
- **Responsiveness**: Ensure the tool works on mobile and desktop using Tailwind's responsive utilities.
