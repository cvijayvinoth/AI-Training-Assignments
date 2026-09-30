from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
import json
from datetime import datetime
import urllib.parse

def human_delay(min_sec=2, max_sec=5):
    """Adds a random delay to mimic human behavior and avoid bans."""
    time.sleep(random.uniform(min_sec, max_sec))

def main():
    # 1. Read from Google Sheet
    # IMPORTANT: Your Google Sheet must be set to "Anyone with the link can view".
    # Replace the ID below with your actual Google Sheet ID.
    SHEET_ID = "XXXX-XXXX-XXXX-XXXX" 
    sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    
    print("Fetching contacts from Google Sheet...")
    try:
        df = pd.read_csv(sheet_url)
        contacts = df.to_dict('records')
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    report_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 2. Log in to WhatsApp Web
        print("Opening WhatsApp Web. Please scan the QR code...")
        page.goto("https://web.whatsapp.com")
        
        # Wait for the chat list to load (indicates successful login)
        page.wait_for_selector('#pane-side', timeout=90000)
        print("Login successful! Starting automation...")

        for contact in contacts:
            name = contact.get('Name', 'Unknown')
            phone = str(contact.get('Phone', ''))
            msg_template = contact.get('Message', 'Hello {name}!')
            # Blank sheet cells come back from pandas as NaN (a float), and dict.get()
            # won't fall back since the key exists — so normalise it here.
            if msg_template is None or (isinstance(msg_template, float) and pd.isna(msg_template)):
                msg_template = 'Hello {name}!'
            msg_template = str(msg_template)
            
            # Format message
            personalized_msg = msg_template.replace('{name}', name)
            
            contact_report = {
                "Name": name,
                "Phone": phone,
                "Status": "Failed",
                "Extracted_Messages": []
            }

            try:
                # 3. Search and send message using the URL scheme (more reliable than UI clicking)
                print(f"Messaging {name} ({phone})...")
                encoded_msg = urllib.parse.quote(personalized_msg)
                page.goto(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")
                
                # Give the chat a moment to open. An unregistered number shows a popup
                # instead of a composer, so surface that as a clear error rather than
                # letting it fall through to a generic selector timeout.
                page.wait_for_timeout(5000)
                dialogs = page.locator('div[role="dialog"]')
                if dialogs.count() > 0:
                    dialog_text = dialogs.first.inner_text().strip()
                    if 'invalid' in dialog_text.lower() or 'not on whatsapp' in dialog_text.lower():
                        raise RuntimeError(f"Number not on WhatsApp: {dialog_text}")

                # WhatsApp Web renames its icons often, so try each known send-button
                # selector rather than depending on a single one.
                send_button = None
                for selector in ('button[aria-label="Send"]',
                                 'span[data-icon="send"]',
                                 'span[data-icon="wds-ic-send-filled"]'):
                    try:
                        page.wait_for_selector(selector, timeout=5000, state='visible')
                        send_button = page.locator(selector).last
                        break
                    except Exception:
                        continue

                if send_button is not None:
                    human_delay(2, 4)
                    send_button.click()
                else:
                    # Fallback: the text is already pre-filled by the ?text= URL param,
                    # so focusing the composer and pressing Enter sends it without
                    # needing to match any icon selector at all.
                    message_box = 'div[contenteditable="true"][data-tab="10"]'
                    page.wait_for_selector(message_box, timeout=15000)
                    page.locator(message_box).last.click()
                    human_delay(1, 2)
                    page.keyboard.press('Enter')
                human_delay(2, 4)

                # 4. Take Screenshot
                screenshot_file = f"screenshot_{name.replace(' ', '_')}_{today_str}.png"
                page.screenshot(path=screenshot_file)
                contact_report["Screenshot"] = screenshot_file

                # 5. Extract the last 3 received messages (Smart Data Extraction)
                # 'message-in' is the typical class for received messages in WA Web
                messages = page.locator('div.message-in span.selectable-text')
                msg_count = messages.count()
                
                extracted = []
                # Get up to the last 3 messages
                start_index = max(0, msg_count - 3)
                for i in range(start_index, msg_count):
                    extracted.append(messages.nth(i).inner_text())
                
                contact_report["Extracted_Messages"] = extracted
                contact_report["Status"] = "Success"
                print(f"Successfully processed {name}.")

            except Exception as e:
                print(f"Failed to process {name} ({phone}): {e}")
                contact_report["Error"] = str(e)
                # Capture what the page actually looked like, so a selector timeout
                # can be diagnosed without re-running the whole bot.
                try:
                    error_shot = f"error_{name.replace(' ', '_')}_{today_str}.png"
                    page.screenshot(path=error_shot)
                    contact_report["Error_Screenshot"] = error_shot
                except Exception as shot_err:
                    print(f"Could not capture error screenshot: {shot_err}")

            report_data.append(contact_report)
            human_delay(3, 6) # Delay between contacts

        # 6. Save Reports
        json_filename = f"whatsapp_report_{today_str}.json"
        excel_filename = f"whatsapp_report_{today_str}.xlsx"

        # Save JSON
        # UTF-8 is explicit because scraped WhatsApp text routinely contains emoji /
        # non-Latin script, which Windows' default cp1252 codepage cannot encode.
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        
        # Save Excel
        report_df = pd.DataFrame(report_data)
        # Convert list of extracted messages to a single string for Excel
        report_df['Extracted_Messages'] = report_df['Extracted_Messages'].apply(lambda x: " | ".join(x) if isinstance(x, list) else x)
        report_df.to_excel(excel_filename, index=False)

        print(f"Run complete! Reports saved as {json_filename} and {excel_filename}.")
        browser.close()

if __name__ == "__main__":
    main()