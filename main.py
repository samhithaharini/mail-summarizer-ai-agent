"""
Email Summarizer Agent - Main Entry Point
Handles CLI arguments and schedules periodic checks.
"""

import sys
import time
import argparse
from rich.console import Console
from rich.panel import Panel
from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from agent import EmailSummarizerAgent

console = Console()

def main():
    """Main entry point for the application."""
    
    # Define CLI arguments
    parser = argparse.ArgumentParser(description="Gmail-to-WhatsApp Email Summarizer Agent")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    parser.add_argument("--force", action="store_true", help="Ignore last check time and process all unread")
    parser.add_argument("--no-announce", action="store_true", help="Don't send startup message to WhatsApp")
    args = parser.parse_args()

    # Title Banner
    console.print(Panel(
        "[bold cyan]📧 GMAIL TO WHATSAPP SUMMARIZER 🤖[/bold cyan]\n"
        "[dim]Powered by Google Gemini AI & Twilio[/dim]",
        border_style="cyan"
    ))

    # Validate configuration
    Config.validate()
    Config.display()

    try:
        # Initialize Agent
        agent = EmailSummarizerAgent()
        
        if args.once:
            console.print("[bold yellow]🏃 Running single manual cycle...[/bold yellow]")
            agent.run_cycle(force=args.force)
            console.print("[green]✅ Manual run finished. Exiting.[/green]")
            return

        # Announce startup
        if not args.no_announce:
            agent.announce_startup()

        # Initialize Scheduler
        scheduler = BlockingScheduler()
        
        # Add the job
        scheduler.add_job(
            agent.run_cycle, 
            'interval', 
            minutes=Config.CHECK_INTERVAL_MINUTES,
            id='email_check',
            kwargs={'force': args.force}
        )

        console.print(Panel(
            f"[bold green]✨ Scheduler Active![/bold green]\n\n"
            f"Checking for emails every [yellow]{Config.CHECK_INTERVAL_MINUTES} minutes[/yellow].\n"
            f"Press [bold red]Ctrl+C[/bold red] to stop the agent.",
            border_style="green"
        ))

        # Run first cycle immediately
        agent.run_cycle(force=args.force)

        # Start the scheduler
        scheduler.start()

    except KeyboardInterrupt:
        console.print("\n[bold yellow]🛑 Agent stopped by user. Goodbye![/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]💥 CRITICAL ERROR: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
