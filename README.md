# Ando Agent Plugin

[Agent Plugins](https://agent-plugins.org/) package for [Ando](https://ando.so) (Asari Inc.). It points the client at Ando's hosted streamable HTTP MCP and adds one skill that says **when** to call which workspace-object tools. It does **not** reimplement a stdio proxy of the REST API.

- Product: [Ando](https://ando.so)
- Hosted MCP: `https://mcp.ando.so/mcp` (streamable HTTP)
- MCP docs: https://docs.ando.so/docs/ando-mcp
- Format: Agent Plugin (`plugin.json` at repo root + `skills/` + `mcp.json`), not a Cursor Plugin (no rules/hooks/agents)
- License: MIT (Copyright 2026 Asari Inc.)

## Usage

Install from the Cursor Marketplace, or copy this folder to `~/.cursor/plugins/local/ando` and reload the Cursor window. Then:

1. Open **Customize** and confirm the `ando` plugin, skill, and MCP server.
2. Complete Ando OAuth (workspace + consent) when the client prompts.
3. Use the agent against Ando workspace objects (Conversations, Messages, Members, Documents, Calls/Jams, Tasks). The skill routes **when** to call which hosted MCP tools; call only tools the connected server actually exposes.

## Config

`mcp.json` is **URL-only**. Agent Plugins 1.0.0 defines no portable OAuth or credential-reference fields, and forbids secrets in `headers`.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "ando": {
      "type": "streamable-http",
      "url": "https://mcp.ando.so/mcp"
    }
  }
}
```

Do not put API keys in this repo. Do not add `Authorization` headers or Cursor `${VAR}` placeholders to this Agent Plugin `mcp.json` (placeholders are not expanded on remote URLs/headers in the Agent Plugins spec).

## OAuth

Interactive clients (including Cursor Marketplace installs) authenticate with **OAuth**. Cursor discovers Ando's OAuth metadata from the MCP URL and runs the browser consent flow. Ando publishes:

- Resource metadata: `https://mcp.ando.so/.well-known/oauth-protected-resource`
- Authorization server: `https://mcp.ando.so/.well-known/oauth-authorization-server` (`authorization_endpoint`, `token_endpoint`, `registration_endpoint`)

Headless / no-OAuth fallback (manual Cursor MCP config, **not** this plugin): member API key as `Authorization: Bearer <key>`. See https://docs.ando.so/docs/ando-mcp

## Files

```
ando-plugin/
├── LICENSE
├── README.md
├── plugin.json
├── mcp.json
├── assets/
│   └── logo.png
└── skills/
    └── ando/
        └── SKILL.md
```

## Marketplace

Public submit flow: https://cursor.com/marketplace/publish  
Publisher terms: https://cursor.com/marketplace-publisher-terms  
Template (Cursor Plugin multi-plugin layout; this package is a single Agent Plugin): https://github.com/cursor/plugin-template
