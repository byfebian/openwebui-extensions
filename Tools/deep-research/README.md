# Deep Research

Crawl4AI-powered deep research tool for Open WebUI.

## Prerequisites

This tool requires a running **[Crawl4AI Proxy](https://github.com/byfebian/crawl4ai-proxy)** service. It will not work without it.

Follow the setup instructions in the Crawl4AI Proxy repo to get it running before installing this tool.

The proxy URL defaults to `http://crawl4ai-proxy:8000` and can be configured via the `CRAWL4AI_PROXY_URL` environment variable.

## Installation

1. Open your Open WebUI instance
2. Go to Workspace → Tools → + Add
3. Switch to the "Code" editor tab
4. Paste the contents of `crawl4ai-tools.py`
5. Click Save

## Configuration

After saving, click the gear icon on the tool to configure the Valves:

| Valve | Description | Default |
|-------|-------------|---------|
| Deep Research | ON/OFF — crawl linked pages for comprehensive coverage | OFF |
| Research Depth | Low / Medium / High — link-follow depth | Medium |
| Max Pages | Max pages to crawl when Deep Research is ON | 10 |
| Reading Mode | Best / Focused / All — content extraction mode | Best |
| Stealth Mode | ON/OFF — bypass bot detection | OFF |

### Reading Mode details

- **Best** — PruningContentFilter (removes boilerplate, keeps quality content)
- **Focused** — BM25ContentFilter (extracts only content matching the user's question)
- **All** — No filter (returns the full page unfiltered)

When "Focused" is selected, the user's last chat message is automatically used as the BM25 search query.