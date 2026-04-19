# 📧 Gmail-to-WhatsApp Email Summarizer Agent 🤖

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google-gemini&logoColor=white)](https://aistudio.google.com/)
[![Twilio](https://img.shields.io/badge/Messaging-Twilio%20WhatsApp-red?logo=twilio&logoColor=white)](https://www.twilio.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI agent that monitors your Gmail inbox, summarizes your unread emails using **Google Gemini Pro**, and sends a concise digest directly to your **WhatsApp**. Never miss an important email again while staying away from your inbox!

---

## ✨ Key Features

-   **🔍 Smart Monitoring:** Periodically checks your Gmail for new, unread messages.
-   **🧠 AI-Powered Summarization:** Uses Google's Gemini AI to distill long emails into actionable WhatsApp-friendly digests.
-   **📱 Instant WhatsApp Delivery:** Sends summaries via Twilio's WhatsApp API.
-   **📅 Intelligent Scheduling:** Runs automatically in the background at configurable intervals.
-   **🛠️ CLI Flexibility:** Manual triggers, force-checks, and silent modes available.
-   **🎨 Beautiful Console UI:** Rich, color-coded terminal output for easy debugging and status tracking.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
-   Python 3.8+
-   A Google Cloud Project (for Gmail API)
-   A Google AI Studio API Key (for Gemini)
-   A Twilio Account (for WhatsApp Messaging)

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/yourusername/email-summarizer-agent.git
cd email-summarizer-agent
pip install -r requirements.txt
```

### 3. Configuration
1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and fill in your credentials:
    -   `GOOGLE_API_KEY`: Your Gemini API key.
    -   `TWILIO_ACCOUNT_SID` & `TWILIO_AUTH_TOKEN`: From your Twilio console.
    -   `TWILIO_WHATSAPP_NUMBER`: The Twilio sandbox number (e.g., `+14155238886`).
    -   `MY_WHATSAPP_NUMBER`: Your personal number (format: `+91XXXXXXXXXX`).
    -   `MY_EMAIL`: Your Gmail address.

3.  Place your `credentials.json` (from Google Cloud) in the project root.

---

## 🛠️ Usage

### Standard Background Mode
Runs the agent in the background, checking for emails every X minutes (as defined in `.env`).
```bash
python main.py
```

### Manual Trigger
Run a single check and exit immediately:
```bash
python main.py --once
```

### Force All Unread
Ignore the "last checked" timestamp and summarize all currently unread emails:
```bash
python main.py --force
```

### Argument Reference
| Argument | Description |
| :--- | :--- |
| `--once` | Run a single cycle and exit. |
| `--force` | Process all unread emails, ignoring the last check time. |
| `--no-announce` | Stop the agent from sending a "Started up" message to WhatsApp. |

---

## 🏗️ Architecture

-   **`gmail_client.py`**: Handles OAuth2 authentication and Gmail API interactions.
-   **`summarizer.py`**: The AI engine using Gemini to process email content.
-   **`whatsapp_client.py`**: Manages communication with the Twilio API.
-   **`agent.py`**: The orchestrator that ties all components together.
-   **`main.py`**: The CLI entry point and scheduler.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ for productivity</p>
