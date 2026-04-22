# Attribution: sub-agents

- **Original author**: [skyzi000](https://github.com/Skyzi000)
- **Original source**: [open-webui-extensions](https://github.com/Skyzi000/open-webui-extensions)
- **License**: MIT
- **Original version**: 0.4.9
- **Modified by**: [byfebian](https://github.com/byfebian)
- **Modified version**: 0.0.1

## Modifications

- Added concurrency control via `MAX_CONCURRENT_API_CALLS` semaphore (default 2, reserves 1 slot for main chat)
- Added `PARALLEL_EXECUTION` valve (default `False` / sequential) — toggle between parallel and sequential task execution
- Added `TOOL_CALL_COOLDOWN` valve (default 1.0s) — async sleep between tool iterations to respect rate-limited APIs (e.g., Brave Search free tier)
- Added retry with exponential backoff (3 retries, 2s/4s/8s) on transient API errors (HTTP 429, 5xx, connection errors)
- Fixed `request.body()` double-read bug affecting `terminal_id` and `tool_servers` resolution
- Deduplicated ~90% shared setup code between `run_sub_agent` and `run_parallel_sub_agents` into `_prepare_sub_agent_context()`
- Reduced `MAX_PARALLEL_AGENTS` default from 5 to 2
- Bumped version to 0.5.0
- Migrated to Open WebUI 0.9.0 async API:
  - Added `await` to `get_sorted_filter_ids()`, `get_updated_tool_function()`, `get_builtin_tools()`, `Functions.get_function_by_id()`
  - Converted `Functions.get_function_by_id()` list comprehension to `asyncio.gather()` for parallel async fetch
  - Made `register_view_skill()` async and updated its caller to `await`
