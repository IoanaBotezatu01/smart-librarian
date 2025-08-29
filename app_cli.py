# app_cli.py
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from chatbot import RAGChatbot
from utils import is_offensive, maybe_tts, maybe_image


def main():
    load_dotenv()
    console = Console()
    bot = RAGChatbot()

    console.print(
        Panel.fit("[bold]📚 Smart Librarian[/bold] – Ask me about books (Ctrl+C to exit)")
    )

    while True:
        try:
            q = console.input("[bold cyan]>[/bold cyan] ")

            # Check for offensive language
            if is_offensive(q):
                console.print(
                    "[yellow]⚠️ Please phrase your question politely. Your input was blocked.[/yellow]"
                )
                continue

            # Query the bot
            ans = bot.ask(q)
            console.print(Panel(ans, title="Recommendation"))

            # Optional: TTS / Image
            audio_path = maybe_tts(ans)
            if audio_path:
                console.print(f"[green]🔊 Audio saved at[/green] {audio_path}")

            img_path = maybe_image(q, ans)
            if img_path:
                console.print(f"[green]🖼️ Book cover generated at[/green] {img_path}")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
