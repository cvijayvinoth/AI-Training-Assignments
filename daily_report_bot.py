import pyautogui
import time
import pyperclip
from datetime import datetime
import webbrowser

def wait(seconds):
    """Helper function to wait and let the UI load."""
    time.sleep(seconds)

def main():
    # 1. Generate dynamic date/time strings
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    report_name = f"daily_report_{current_date}"
    comment = "Market looks stable today."

    print("Starting bot in 3 seconds. Please do not touch the mouse or keyboard...")
    wait(3)

    # 2. Open Chrome and go to a public website (e.g., Google Finance)
    # Using webbrowser module to reliably open the default browser (Chrome)
    print("Opening data source website...")
    webbrowser.open('https://www.google.com/finance/quote/GOOGL:NASDAQ')
    wait(7) # Wait for page to fully load

    # 3. Copy information from the page
    # Note: For PyAutoGUI, extracting specific text is tricky without coordinates.
    # We will simulate clicking on the price and copying it. 
    # IMPORTANT: You will need to change these X, Y coordinates to match where the price is on your screen!
    print("Copying data...")
    pyautogui.moveTo(400, 350, duration=0.5) # TODO: Adjust these coordinates to hover over the target data
    pyautogui.doubleClick() # Highlight the text
    pyautogui.hotkey('ctrl', 'c') # Use 'command' instead of 'ctrl' if you are on a Mac
    wait(1)
    
    fetched_data = pyperclip.paste()
    if not fetched_data.strip():
        fetched_data = "Fallback Data: $150.00" # Fallback if copy fails

    # 4. Open a new Google Sheet in a new tab
    print("Opening Google Sheets...")
    pyautogui.hotkey('ctrl', 't') # Open new tab ('command', 't' on Mac)
    wait(1)
    pyautogui.write('sheet.new')
    pyautogui.press('enter')
    wait(8) # Google Sheets takes a few seconds to fully initialize

    # 5. Enter Data into the Spreadsheet (Default focus is usually Cell A1)
    print("Entering data into the sheet...")
    # Cell A1: Date & Time
    pyautogui.write(current_datetime)
    pyautogui.press('tab') # Move to B1
    wait(0.5)
    
    # Cell B1: Fetched Data
    pyautogui.write(f"GOOGL Price: {fetched_data}")
    pyautogui.press('tab') # Move to C1
    wait(0.5)
    
    # Cell C1: Comment
    pyautogui.write(comment)
    pyautogui.press('enter')
    wait(1)

    # 6. Rename the Google Sheet
    # In Sheets, we can jump to the title box using the keyboard shortcut: Alt + Shift + F, then press Up/Right (varies by OS), 
    # but clicking the title is much more reliable across different OS setups.
    print("Renaming the Google Sheet...")
    # TODO: Adjust coordinates to click the "Untitled spreadsheet" title text in the top left
    pyautogui.moveTo(150, 100, duration=0.5) 
    pyautogui.click()
    wait(1)
    pyautogui.hotkey('ctrl', 'a') # Select the existing title "Untitled spreadsheet"
    pyautogui.write(report_name)
    pyautogui.press('enter')
    wait(2)

    # 7. Take a screenshot of the final sheet
    print("Taking a screenshot...")
    screenshot_filename = f"{report_name}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)
    print(f"Success! Saved screenshot as {screenshot_filename}")

if __name__ == "__main__":
    main()