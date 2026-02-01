# MCP Server for moomoo (OpenD)

An MCP server that exposes **moomoo OpenD** market data (and later, guarded trading actions) as simple tools for LLM agents.

**Status:** pre-MVP (building in public)  
**Default mode:** read-only + paper/sim-first (no live trading by default)

## Why
- Agents need a clean tool interface (MCP)
- moomoo connectivity goes through OpenD (local gateway)
- Quants want pandas-ready outputs + notebooks

## Features (MVP)
- [ ] quote.get — last price, bid/ask, volume
- [ ] candles.get — historical bars
- [ ] positions.list
- [ ] account.summary

## Architecture
Agent (LLM)
  → MCP tools
  → This server (Python/FastMCP)
  → OpenD (local gateway)
  → moomoo OpenAPI

## Quickstart (coming this weekend)
1) Install and log into OpenD
2) `uv venv && uv pip install -e .`  (or `pip install -e .`)
3) `python -m mcp_moomoo.server`
4) Connect your MCP client via stdio

## Config
Copy `.env.example` to `.env`:
- MOOMOO_OPEND_HOST=127.0.0.1
- MOOMOO_OPEND_PORT=xxxxx
- MOOMOO_ENV=paper

## Safety
- Not financial advice.
- Live trading disabled by default.
- Trading tools (post-MVP) will require explicit opt-in and hard risk caps.

## Contributing
Issues/PRs welcome, especially:
- OpenD connectivity notes (OS, version, logs)
- tool schema suggestions
- example notebooks
