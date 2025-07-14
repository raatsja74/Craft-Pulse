import os
import threading

import openai
from AppKit import (
    NSApp,
    NSApplication,
    NSStatusBar,
    NSVariableStatusItemLength,
    NSMenu,
    NSMenuItem,
    NSWindow,
    NSTextField,
    NSButton,
    NSTextView,
    NSMakeRect,
    NSBackingStoreBuffered,
    NSTitledWindowMask,
)
from Foundation import NSObject
from PyObjCTools import AppHelper
from pynput import keyboard


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.create_status_item()
        self.create_window()
        self.start_hotkey_listener()

    # Status bar
    def create_status_item(self):
        status_bar = NSStatusBar.systemStatusBar()
        self.status_item = status_bar.statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setTitle_("💬")
        menu = NSMenu.alloc().init()
        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Ask ChatGPT", "openWindow:", ""
        )
        menu.addItem_(item)
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", "terminate:", "q"
        )
        menu.addItem_(quit_item)
        self.status_item.setMenu_(menu)

    # Hotkey
    def start_hotkey_listener(self):
        listener = keyboard.GlobalHotKeys({"<cmd>+<shift>+g": self.openWindow})
        listener.start()
        self.listener = listener

    # UI
    def create_window(self):
        rect = ((200.0, 200.0), (400.0, 200.0))
        style = NSTitledWindowMask
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, style, NSBackingStoreBuffered, False
        )
        self.window.setTitle_("ChatGPT Prompt")

        self.input_field = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 150, 360, 24))
        self.output_view = NSTextView.alloc().initWithFrame_(NSMakeRect(20, 20, 360, 120))
        self.output_view.setEditable_(False)

        button = NSButton.alloc().initWithFrame_(NSMakeRect(300, 170, 80, 24))
        button.setTitle_("Send")
        button.setTarget_(self)
        button.setAction_("sendPrompt:")

        self.window.contentView().addSubview_(self.input_field)
        self.window.contentView().addSubview_(self.output_view)
        self.window.contentView().addSubview_(button)

    def openWindow(self):
        self.window.makeKeyAndOrderFront_(None)
        NSApp.activateIgnoringOtherApps_(True)

    def openWindow_(self, sender):
        self.openWindow()

    def sendPrompt_(self, sender):
        prompt = self.input_field.stringValue()
        if not prompt:
            return
        thread = threading.Thread(target=self.call_openai, args=(prompt,))
        thread.start()

    def call_openai(self, prompt):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp["choices"][0]["message"]["content"]
        except Exception as e:
            text = f"Error: {e}"
        self.output_view.performSelectorOnMainThread_withObject_waitUntilDone_(
            "setString:", text, False
        )


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
