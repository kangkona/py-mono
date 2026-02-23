"""Universal messenger bot core."""

import asyncio
from typing import Dict, Optional
from pathlib import Path

from py_agent_core import Agent, Session

from .platform import MessagePlatform
from .message import UniversalMessage, UniversalResponse
from .session_manager import MultiPlatformSessionManager


class MessengerBot:
    """Universal multi-platform bot."""

    def __init__(
        self,
        agent: Agent,
        workspace: Optional[Path] = None,
        enable_sessions: bool = True,
    ):
        """Initialize messenger bot.

        Args:
            agent: Agent instance
            workspace: Workspace directory
            enable_sessions: Enable session management
        """
        self.agent = agent
        self.workspace = Path(workspace) if workspace else Path.cwd() / ".messenger"
        self.workspace.mkdir(exist_ok=True)

        self.platforms: Dict[str, MessagePlatform] = {}
        self.session_manager = None

        if enable_sessions:
            self.session_manager = MultiPlatformSessionManager(self.workspace)

    def add_platform(self, platform: MessagePlatform) -> None:
        """Add a platform adapter.

        Args:
            platform: Platform adapter instance
        """
        self.platforms[platform.name] = platform
        platform.set_message_handler(self.handle_message)
        print(f"✓ Added platform: {platform.name}")

    def remove_platform(self, platform_name: str) -> None:
        """Remove a platform adapter.

        Args:
            platform_name: Platform name
        """
        if platform_name in self.platforms:
            platform = self.platforms[platform_name]
            platform.stop()
            del self.platforms[platform_name]
            print(f"✓ Removed platform: {platform_name}")

    async def handle_message(self, message: UniversalMessage) -> None:
        """Handle incoming message from any platform.

        Args:
            message: Universal message
        """
        try:
            # Get or create session for this channel
            session = None
            if self.session_manager:
                session_key = f"{message.platform}:{message.channel_id}"
                session = self.session_manager.get_session(session_key)

                # Add user message to session
                session.add_message("user", message.text)

            # Run agent
            response = self.agent.run(message.text)

            # Add response to session
            if session:
                session.add_message("assistant", response.content)

            # Send response back to platform
            platform = self.platforms.get(message.platform)
            if platform:
                await platform.send_message(
                    message.channel_id,
                    response.content,
                    thread_id=message.thread_id if message.is_thread else None,
                )

        except Exception as e:
            print(f"Error handling message: {e}")

            # Try to send error message back
            platform = self.platforms.get(message.platform)
            if platform:
                try:
                    await platform.send_message(
                        message.channel_id,
                        f"❌ Error: {e}",
                        thread_id=message.thread_id if message.is_thread else None,
                    )
                except Exception:
                    pass

    def start(self) -> None:
        """Start all platforms.

        This is a blocking call.
        """
        if not self.platforms:
            print("No platforms configured!")
            return

        print(f"\n🤖 Starting MessengerBot with {len(self.platforms)} platform(s)...")
        for name in self.platforms:
            print(f"   • {name}")
        print()

        # Start all platforms in parallel
        tasks = []
        for platform in self.platforms.values():
            tasks.append(asyncio.create_task(self._run_platform(platform)))

        # Wait for all
        try:
            asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        except KeyboardInterrupt:
            print("\n\nStopping bot...")
            self.stop()

    async def _run_platform(self, platform: MessagePlatform) -> None:
        """Run a platform in async context.

        Args:
            platform: Platform to run
        """
        try:
            await asyncio.to_thread(platform.start)
        except Exception as e:
            print(f"Platform {platform.name} error: {e}")

    def stop(self) -> None:
        """Stop all platforms."""
        for platform in self.platforms.values():
            try:
                platform.stop()
            except Exception as e:
                print(f"Error stopping {platform.name}: {e}")

        print("✓ Bot stopped")
