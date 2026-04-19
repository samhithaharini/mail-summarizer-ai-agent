"""
AI Summarizer Module
Uses Google Gemini AI to generate concise summaries of emails.
"""

from datetime import datetime

import google.generativeai as genai
from rich.console import Console

from config import Config

console = Console()


class EmailSummarizer:
    """Summarizes emails using Google Gemini AI."""

    def __init__(self):
        """Initialize the Gemini AI model."""
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        console.print("[green]✅ Gemini AI model initialized![/green]")

    def summarize_emails(self, emails):
        """
        Generate a WhatsApp-friendly summary digest of important emails.
        
        Args:
            emails: List of email dictionaries with subject, sender, body, etc.
            
        Returns:
            Formatted summary string ready to send via WhatsApp.
        """
        if not emails:
            return None

        console.print(f"[dim]🤖 Summarizing {len(emails)} email(s) with Gemini AI...[/dim]")

        # Build the prompt with all emails
        email_texts = []
        for i, email in enumerate(emails, 1):
            email_texts.append(
                f"--- EMAIL {i} ---\n"
                f"From: {email.get('sender', 'Unknown')}\n"
                f"Subject: {email.get('subject', 'No Subject')}\n"
                f"Date: {email.get('date', 'Unknown')}\n"
                f"Body:\n{email.get('body', email.get('snippet', 'No content'))}\n"
            )

        all_emails = "\n\n".join(email_texts)

        prompt = f"""You are a personal email assistant. Summarize the following important emails into a concise WhatsApp message digest.

Rules:
1. For each email, provide:
   - Who sent it (just the name, not full email)
   - What it's about (1-2 sentences max)
   - Any action required (deadline, reply needed, etc.)
2. Use emojis to make it scannable
3. Keep the entire summary under 1500 characters (WhatsApp friendly)
4. Start with a greeting header with today's date
5. End with the total count
6. If an email is truly trivial, skip it and mention how many were skipped
7. Focus on ACTIONABLE information
8. Use numbering (1️⃣, 2️⃣, etc.) for each email

Today's date: {datetime.now().strftime("%B %d, %Y")}

Here are the emails to summarize:

{all_emails}

Generate the WhatsApp summary message now:"""

        try:
            response = self.model.generate_content(prompt)

            if response and response.text:
                summary = response.text.strip()
                console.print("[green]✅ Summary generated successfully![/green]")

                # Ensure it's not too long for WhatsApp (limit ~1600 chars per message)
                if len(summary) > 1550:
                    summary = summary[:1500] + "\n\n... [summary truncated]"

                return summary
            else:
                console.print("[red]❌ Gemini returned empty response[/red]")
                return self._fallback_summary(emails)

        except Exception as e:
            console.print(f"[red]❌ Gemini AI error: {e}[/red]")
            return self._fallback_summary(emails)

    def _fallback_summary(self, emails):
        """Generate a basic summary without AI if Gemini fails."""
        console.print("[yellow]⚠️ Using fallback summary (no AI)...[/yellow]")

        now = datetime.now().strftime("%B %d, %Y %I:%M %p")
        lines = [f"📧 Email Summary - {now}\n"]

        for i, email in enumerate(emails, 1):
            sender = email.get("sender", "Unknown")
            # Extract just the name from "Name <email>" format
            if "<" in sender:
                sender = sender.split("<")[0].strip().strip('"')

            subject = email.get("subject", "No Subject")
            snippet = email.get("snippet", "")[:100]

            lines.append(f"{i}. 📩 {sender}")
            lines.append(f"   📌 {subject}")
            if snippet:
                lines.append(f"   💬 {snippet}")
            lines.append("")

        lines.append(f"✅ Total: {len(emails)} important email(s)")

        return "\n".join(lines)

    def summarize_single(self, email):
        """
        Summarize a single email (used for real-time notifications).
        
        Args:
            email: Single email dictionary
            
        Returns:
            Short summary string
        """
        prompt = f"""Summarize this email in 2-3 sentences. Focus on the key action or information.

From: {email.get('sender', 'Unknown')}
Subject: {email.get('subject', '')}
Body: {email.get('body', email.get('snippet', ''))}

Brief summary:"""

        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            console.print(f"[red]❌ Single summary error: {e}[/red]")

        return email.get("snippet", "Unable to summarize")
