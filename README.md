# Ando Agent Plugin

[Agent Plugins](https://agent-plugins.org/) package for [Ando](https://ando.so) (Asari Inc.). It points the client at Ando's hosted streamable HTTP MCP and adds one skill that says **when** to call which workspace-object tools. It does **not** reimplement a stdio proxy of the REST API.

- Product: [Ando](https://ando.so)
- Hosted MCP: `https://mcp.ando.so/mcp` (streamable HTTP)
- MCP docs: https://docs.ando.so/docs/ando-mcp
- Format: Agent Plugin (`plugin.json` at repo root + `skills/` + `mcp.json`), not a Cursor Plugin (no rules/hooks/agents)
- License: MIT (Copyright 2026 Asari Inc.)

## Usage

After loading this plugin in Grokbot or another compatible Agent Plugins client:

1. Confirm the `ando` plugin, skill, and MCP server are enabled.
2. Complete Ando OAuth when the client prompts. The plugin checks the returned identity: generic OAuth may connect as a person, so authentication alone does not finish agent setup.
3. For Grokbot agent setup, open **Ando → Studio → Agents**, select the intended agent, and open its **Grokbot Cloud** setup. Copy the Grok Bot setup prompt / exact OAuth MCP URL into Grokbot. During approval, choose **Pair an existing agent** and select that agent (or explicitly create one). Keep the scoped URL intact; the generic plugin URL cannot carry this workspace-specific pairing request.
4. After approval, the plugin verifies the new connection's agent and workspace identity before starting agent work. If the client cannot add MCP connections itself, it guides you through settings; it cannot perform a browser redirect or change the authenticated identity by prompt alone. Existing generic connections must be paired this way too; merely updating the plugin does not change their OAuth grant.
5. Use the agent against Ando workspace objects (Conversations, Messages, Members, Documents, Calls/Jams, Tasks). The skill routes **when** to call which hosted MCP tools; call only tools the connected server actually exposes.

## Agent behavior and live replies

After identity verification, continue work the user already requested within their authorization. For an otherwise empty setup session, recommend one evidence-backed starting point. Do not require another approval for work that is already authorized.

Connection and incoming-message delivery are separate milestones. For live replies, use the selected agent's **Runtime → Grokbot → Message delivery** setup prompt to configure a webhook-triggered routine with the verified Ando connection. Keep the sender key out of chat. Test a new DM while Grok is idle, then a second roundtrip in the original thread; neither installing this plugin nor receiving a webhook 2xx proves that replies work.

## Release verification

A merge updates this repository, not necessarily the marketplace artifact. Update the existing listing through its publisher account, then inspect the version and source commit actually installed by Grok. Do not treat a version bump or an install refresh as proof of distribution, or create a duplicate listing to work around publisher access.

For each release, exercise these decisions in the real client:

- Human or wrong-agent connection: detect the mismatch and recover through scoped pairing.
- Correct agent: keep the identity and continue already-authorized work without redundant setup or approval.
- Missing tools or expired pairing URL: report the specific incomplete step and recover without changing other connections.
- Incoming replies: use the verified custom connection, respect the authorized response scope, and prove two idle roundtrips.

Private-skill invocation tests instruction behavior only. Marketplace loading, automatic invocation after authentication, OAuth completion, and idle delivery each require their own live verification.

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
