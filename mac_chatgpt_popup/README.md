# mac_chatgpt_popup

This directory contains a small macOS menu bar application that lets you send quick prompts to ChatGPT. Clicking the status bar icon or pressing a global hotkey opens a text input popup. The contents are sent to OpenAI and the response is shown in the popup window.

## Installation

1. Ensure Python 3 is installed on your Mac.
2. Install PyObjC and other dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your OpenAI API key so the application can authenticate:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Global Hotkey

The app listens for `⌘`+`⇧`+`G` using `pynput`. On first run macOS will prompt for accessibility permissions. Grant your terminal (or Python) permission under System Settings → Privacy & Security → Accessibility.

## Usage

- Click the "💬" icon in the menu bar or press `⌘`+`⇧`+`G`.
- Enter your question in the text field and press **Send** (or hit Return).
- The response from OpenAI will appear in the lower pane.

This is a simple example meant for experimentation. You can extend it with history, better error handling, or additional shortcuts.
