---
name: ando
description: Use Ando hosted MCP tools to read and write workspace Conversations, Messages, Members, Documents, Calls/Jams, and Tasks. Use when the user mentions Ando, workspace chat, channels, threads, DMs, Jams, documents, or tasks, or asks to search/send/reply in team messaging. Call the live MCP tools; do not invent IDs, schemas, or API payloads.
---

# Ando workspace MCP

This skill is a thin routing layer over the **hosted** Ando MCP at `https://mcp.ando.so/mcp`. The client already exposes the current tool list after connect. **Do not invent tool arguments, object fields, IDs, or REST payloads.** Use only tools and shapes returned by the connected server (or Ando public MCP docs).

Official docs: https://docs.ando.so/docs/ando-mcp  
Tool catalog (generated, may lag the live server): https://docs.ando.so/docs/ando-mcp/tools

## When to use which family

Organize work around Ando workspace objects. Search or list first, then fetch the exact object, then write only if the user asked.

### Conversation
- **When:** list or find channels/DMs, join/create a conversation, see who is in it, add/remove people.
- **Typical tools:** `list_conversations`, `search_conversations`, `list_public_channels`, `list_conversation_members`, `create_conversation`, `join_conversation`, `add_to_conversation`, `remove_from_conversation`.
- Prefer stable conversation IDs over display names such as `#engineering` (names can change).

### Message
- **When:** search chat, read history, open a thread, send/reply/react/delete, or DM someone.
- **Typical tools:** `search_messages`, `get_conversation_messages`, `get_conversation_threads`, `get_thread_replies`, `get_message`, `send_message`, `reply_to_message`, `send_direct_message`, `react_to_message`, `delete_message`.
- Use `get_conversation_messages` for recent history; `search_messages` for a specific query (not wildcards). Confirm the target conversation/message from search or a user-supplied ID before writes.

### Member
- **When:** who is this person/agent, search the directory, invite someone.
- **Typical tools:** `list_workspace_members`, `search_workspace_members`, `get_workspace_member`, `get_current_principal`, `invite_to_workspace`.
- Prefer `list_workspace_members` / `search_workspace_members` / `get_workspace_member` over deprecated `list_members` / `search_members` / `get_member`.

### Document
- **When:** create, read, or update an Ando document in a conversation.
- **Typical tools:** `create_document`, `get_document`, `update_document`.
- For updates, echo the version the get tool returned as `expected_version`. Do not guess version numbers.

### Call / Jam
- **When:** list recent Jams (voice/video), search calls, fetch a call, or read a transcript.
- **Typical tools:** `list_calls`, `search_calls`, `get_call`, `get_call_transcript`.

### Task
- **When:** find or inspect a task, or record an update the user asked for.
- **Typical tools:** `search_tasks`, `get_task`, `record_task_update`.

## First call after connect

If the credential is an **installed external agent**, `get_workspace_orientation` is on the tool list. Call it first. Do not look for Gateway tools (`list_connections`, `list_tools`, `get_tool_schemas`, `execute_tools`); those are not part of this external MCP.

## Writes

Only call write/destructive tools when the user explicitly asks to send, reply, DM, react, invite, join, create, update, remove, or delete. Confirm the target object from a prior search/get (or a precise user-supplied ID).

MCP is request/response. It does not wake the agent on mentions; live events need Ando Realtime or webhooks, which this plugin does not wrap.
