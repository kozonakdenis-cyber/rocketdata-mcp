# RocketData MCP

Read-only MCP bridge between ChatGPT and the RocketData REST API.

Exposed tools:
- `list_companies`
- `get_reviews`
- `get_review_statistics`

Required environment variable: `ROCKETDATA_TOKEN`.
Optional: `ROCKETDATA_BASE_URL` (defaults to `https://api.rocketdata.io`).

The MCP HTTP endpoint is `/mcp`.
