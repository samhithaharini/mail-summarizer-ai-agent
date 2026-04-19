"""
Configuration module for the Email Summarizer Agent.
Loads environment variables and validates required credentials.
"""

import os
import sys
import io
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Fix for Windows terminal encoding issues
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

console = Console()

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for the Email Summarizer Agent."""

    # Google Gemini AI
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    # Twilio WhatsApp
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "+14155238886")

    # User Details
    MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER", "+919865576818")
    MY_EMAIL = os.getenv("MY_EMAIL", "samhitha2613@gmail.com")

    # Agent Settings
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
    MAX_EMAILS_PER_CHECK = int(os.getenv("MAX_EMAILS_PER_CHECK", "20"))

    # Gmail API Scopes
    GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
    TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
    STATE_FILE = os.path.join(BASE_DIR, "agent_state.json")
    LOG_FILE = os.path.join(BASE_DIR, "agent.log")

    # Email categories to SKIP (these are not important)
    SKIP_CATEGORIES = ["CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "CATEGORY_FORUMS"]

    # Gemini Model
    GEMINI_MODEL = "gemini-3-flash-preview"

    @classmethod
    def validate(cls):
        """Validate that all required credentials are configured."""
        missing = []

        if not cls.GOOGLE_API_KEY or cls.GOOGLE_API_KEY == "your_gemini_api_key_here":
            missing.append("GOOGLE_API_KEY")

        if not cls.TWILIO_ACCOUNT_SID or cls.TWILIO_ACCOUNT_SID == "your_twilio_account_sid_here":
            missing.append("TWILIO_ACCOUNT_SID")

        if not cls.TWILIO_AUTH_TOKEN or cls.TWILIO_AUTH_TOKEN == "your_twilio_auth_token_here":
            missing.append("TWILIO_AUTH_TOKEN")

        if not os.path.exists(cls.CREDENTIALS_FILE):
            missing.append("credentials.json (Gmail OAuth2 file)")

        if missing:
            console.print(Panel(
                "[bold red]❌ Missing Configuration![/bold red]\n\n"
                "The following are not configured:\n" +
                "\n".join(f"  • [yellow]{item}[/yellow]" for item in missing) +
                "\n\n[dim]See setup_guide.md for step-by-step instructions.[/dim]",
                title="⚙️ Configuration Error",
                border_style="red"
            ))
            sys.exit(1)

        console.print("[green]✅ All credentials validated successfully![/green]")
        return True

    @classmethod
    def display(cls):
        """Display current configuration (hiding sensitive values)."""
        def mask(value):
            if not value or len(value) < 8:
                return "***"
            return value[:4] + "•" * (len(value) - 8) + value[-4:]

        console.print(Panel(
            f"[cyan]📧 Email:[/cyan] {cls.MY_EMAIL}\n"
            f"[green]📱 WhatsApp:[/green] {cls.MY_WHATSAPP_NUMBER}\n"
            f"[yellow]🤖 Gemini Key:[/yellow] {mask(cls.GOOGLE_API_KEY)}\n"
            f"[magenta]📡 Twilio SID:[/magenta] {mask(cls.TWILIO_ACCOUNT_SID)}\n"
            f"[blue]⏰ Check Interval:[/blue] Every {cls.CHECK_INTERVAL_MINUTES} minutes\n"
            f"[blue]📨 Max Emails:[/blue] {cls.MAX_EMAILS_PER_CHECK} per check",
            title="📋 Agent Configuration",
            border_style="cyan"
        ))
