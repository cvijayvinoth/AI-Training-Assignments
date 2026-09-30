# Social Eagle Automation Architect Assignments

This repository contains the deliverables for the Social Eagle Automation Architect Program. It includes two distinct RPA (Robotic Process Automation) bots built using Python, focusing on desktop UI automation and browser-based web automation.

## Repository Structure

*   `daily_report_bot.py`: The PyAutoGUI automation script for Assignment 1.
*   `whatsapp_bot.py`: The Playwright automation script for Assignment 2.
*   `requirements.txt`: List of Python dependencies required to run the bots.
*   `outputs/`: Directory containing the sample execution outputs (Excel files, JSON reports, and screenshots).

---

## Assignment 1: Daily Status Report Bot (PyAutoGUI)

This bot automates the daily task of fetching financial data and creating a daily status report[cite: 1]. It utilizes PyAutoGUI to physically control the mouse and keyboard, simulating human interaction to open Google Chrome, copy data, and paste it into a newly generated Google Sheet.

### Features
*   **Web Navigation:** Automatically opens Chrome and navigates to Google Finance.
*   **Data Extraction:** Highlights and copies the target data using keyboard shortcuts.
*   **Spreadsheet Generation:** Opens a new Google Sheet (`sheet.new`), inputs the current timestamp, pasted data, and a custom comment, then renames the file.
*   **Proof of Execution:** Captures and saves a screenshot of the final generated spreadsheet.

---

## Assignment 2: WhatsApp Message Sender & Data Extractor (Playwright)

This bot automates daily customer communication by driving a real browser instance through WhatsApp Web[cite: 4]. It reads contact information dynamically from a published Google Sheet CSV and sends personalized messages. 

### Features
*   **Dynamic Data Ingestion:** Reads contacts (Name, Phone, Message Template) from a live Google Sheet, sanitizing empty cells and formatting phone numbers.
*   **Personalized Messaging:** Replaces template variables (e.g., `{name}`) with the actual contact name and dispatches the message via WhatsApp Web's URL API.
*   **Smart Data Extraction:** After sending a message, the bot scrapes the last 3 received messages from that specific contact's chat history.
*   **Human-like Behavior:** Implements randomized delays (2-5 seconds) and explicit selector waits to prevent bans and handle network latency.
*   **Reporting:** Generates a comprehensive execution summary saved as both a `.json` and `.xlsx` file, alongside screenshots of sent messages.

---

## Setup & Installation

**1. Clone the repository and navigate to the project directory:**
```bash
git clone <your-repository-url>
cd <project-folder>
