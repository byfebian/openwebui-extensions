# OpenWebUI-Extensions

A curated collection of [Open WebUI](https://github.com/open-webui/open-webui) tools and functions that I use, modify, and build for myself.

**All extensions have been migrated for Open WebUI 0.9.x compatibility** (async data layer, `await` on model methods, `httpx.AsyncClient` for HTTP).

## Tools

| Tool | Original Author | Source | License | Description |
|------|----------------|--------|---------|-------------|
| [sub-agents](./Tools/sub-agents/) | [skyzi000](https://github.com/Skyzi000) | [original](https://github.com/Skyzi000/open-webui-extensions) | MIT | Run autonomous, tool-heavy tasks in a sub-agent and keep the main chat context clean |
| [deep-research](./Tools/deep-research/) | [byfebian](https://github.com/byfebian) | — | MIT | Crawl4AI Tools — deep research, reading mode, stealth mode via crawl4ai-proxy |

## Functions

| Function | Original Author | Source | License | Description |
|----------|----------------|--------|---------|-------------|
| [smart-mind-map](./Functions/smart-mind-map/) | [Fu-Jie](https://github.com/Fu-Jie) | [original](https://github.com/Fu-Jie/openwebui-extensions) | MIT | Generate interactive mind maps from text content |
| [thinking-off](./Functions/thinking-off/) | [ticoneva](https://github.com/ticoneva) | — | MIT | Toggle reasoning/thinking for OpenRouter, Ollama, and local models |
| [time-awareness](./Functions/time-awareness/) | @abhiraaid | — | — | Pass current time data on each message via filters |
| [token-usage-display](./Functions/token-usage-display/) | assistant | — | MIT | Display input/output/total token counts and generation time below each AI response |
| [zdr-private](./Functions/zdr-private/) | [byfebian](https://github.com/byfebian) | — | — | Toggle Zero Data Retention (ZDR) for OpenRouter requests |

## Attribution

Each tool/function folder contains an `ATTRIBUTION.md` file crediting the original author and detailing modifications. See individual folders for details.

## License

MIT — see [LICENSE](./LICENSE). Each extension retains its original license. Attribution for each extension is provided in its folder's `ATTRIBUTION.md`.
