# Web Search

Use this skill when the user asks you to search for information online or needs current information not in your training data.

This skill helps you search the web and provide accurate, up-to-date information.

## When to Use

- User explicitly asks to "search", "look up", or "find online"
- Need current information (news, stock prices, weather)
- Need factual data you're not certain about
- Verifying claims or statistics

## Steps

1. Identify the search query from user's request
2. Use the search tool to find relevant information
3. Review the search results
4. Summarize the findings in a clear, concise manner
5. Cite sources when possible

## Example Usage

**User**: "Search for the latest Python 3.12 features"

**Agent steps**:
1. Extract query: "Python 3.12 new features"
2. Call: search_web("Python 3.12 new features")
3. Review results
4. Provide summary with key features
5. Mention source: "According to python.org..."

## Output Format

When presenting search results:
- Start with a brief summary
- List key findings as bullet points
- Mention 1-2 most relevant sources
- Offer to search for more specific information

## Notes

- Always verify information looks current and accurate
- If results seem outdated, mention that to user
- Offer to search with different terms if results aren't helpful
