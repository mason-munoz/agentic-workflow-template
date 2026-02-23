# Summarize URL

## Goal
Given a URL, scrape its content and produce a concise summary using an LLM.

## Inputs
- `url` — The webpage URL to summarize

## Tools / Scripts
- `execution/summarize_url.py` — Fetches the page, extracts text, calls OpenAI to summarize

## Steps
1. User provides a URL
2. Run `execution/summarize_url.py <url>`
3. Script returns a markdown summary
4. Present the summary to the user

## Outputs
- A concise, bullet-pointed summary of the page content
- Printed to stdout (can be piped to a file if needed)

## Edge Cases
- **Paywalled content**: Script will return whatever text is publicly accessible. Note this to the user.
- **Very long pages**: Script truncates to ~8,000 tokens before sending to OpenAI to stay within context limits.
- **Rate limits**: If OpenAI returns a 429, wait 10 seconds and retry once.

## Learnings
<!-- This section gets updated as the agent discovers new edge cases -->
