"""Example extension: DateTime tools and commands."""

from datetime import datetime, timedelta


def extension(api):
    """DateTime extension providing time-related tools and commands.
    
    Args:
        api: ExtensionAPI instance
    """
    
    # Register tools
    @api.tool(description="Get current date and time")
    def get_datetime() -> str:
        """Get current date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @api.tool(description="Get current date")
    def get_date() -> str:
        """Get current date."""
        return datetime.now().strftime("%Y-%m-%d")
    
    @api.tool(description="Get current time")
    def get_time() -> str:
        """Get current time."""
        return datetime.now().strftime("%H:%M:%S")
    
    @api.tool(description="Calculate date after N days")
    def date_after_days(days: int) -> str:
        """Calculate date after specified days.
        
        Args:
            days: Number of days to add
        """
        future = datetime.now() + timedelta(days=days)
        return future.strftime("%Y-%m-%d")
    
    # Register commands
    @api.command("now", "Show current date and time")
    def cmd_now():
        """Show current date and time."""
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    @api.command("timestamp", "Get Unix timestamp")
    def cmd_timestamp():
        """Get current Unix timestamp."""
        return f"Timestamp: {int(datetime.now().timestamp())}"
    
    # Register event handlers
    @api.on("tool_call_start")
    def log_tool_start(event, context):
        """Log when a tool starts."""
        if "datetime" in event.get("tool_name", "").lower():
            print(f"⏰ DateTime tool: {event['tool_name']}")
    
    print("✓ DateTime extension loaded (4 tools, 2 commands)")
