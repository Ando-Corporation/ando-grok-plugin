# Routing for separately opted-in preview connections

Preview activation is deferred. Do not create a preview connection, change an OAuth registration, or migrate a legacy caller or routine based on this reference. Use it only when the live tool schemas and overview establish `human-v1` or `compact-v1`. The active schema takes precedence; these catalogs have different contracts even when tool names match.

## Identity and shared collaboration

Call the exposed `get_workspace_overview` with no arguments. For `compact-v1`, its result contains `principal.principal_type`, `principal.workspace_membership_id`, a separate `workspace.id`, `catalog_version`, and granted capabilities. Verify the intended workspace and membership using the actual result. This bounded overview does not read an inbox or configure receiving. If identity/catalog cannot be verified, stop dependent work and refresh the connection through the host's supported flow. A flat MCP tool list is sufficient; do not require custom catalog metadata.

Tools with modes use `{request: {kind: ..., ...operationFields}}`, even if only one mode is granted. Single-operation tools retain their discovered arguments. Never apply this envelope to a legacy tool because its name looks familiar.

- `send_message` uses `conversation`, `thread`, or `direct` for the requested destination. Preserve the original thread/recipients, content, file IDs and retry key. `save_message_draft` saves without sending. Rich cards and miniapp inputs use the permitted `send_message` fields; human sends exclude agent-only content.
- `read_conversation` selects `context`, `messages`, `threads`, or `time_range`; `read_thread` reads replies. Preserve pagination, filters and source links.
- `search_knowledge`, `read_knowledge`, and `update_knowledge` select the granted resource mode. Retain exact resource identity, audience, revision and source requirements; structured channel edits belong on `update_knowledge`.
- `list_members`, `list_conversations`, `list_jams`, and `read_jam` use the modes actually exposed. Do not copy a compact mode into a human or legacy schema.

`human-v1` is a separate human-only preview. Use its exposed collaboration tools without agent inbox, profile, or receiving preflight. In particular, `list_conversations` keeps its original flat arguments, `list_members` supports workspace/conversation modes, `list_jams` retains the list operation's arguments, and knowledge modes cover Wiki/channel resources. Do not assume compact file, task, semantic search, optional-domain tools, or additional modes exist. See the [human catalog mapping](https://docs.ando.so/docs/ando-mcp#human-catalog-and-migration), then use the live schema.

## Direct compact task tools

The current `compact-v1` preview exposes task tools directly. The earlier `discover_capabilities`, `read_capability`, and `run_capability` dispatcher was removed. Refresh any earlier preview schemas; remove dispatcher `operation_id`, `schema_version`, and nested `arguments` envelopes when preparing calls, retaining fields declared by the destination schema itself. This does not authorize migrating saved routines.

- `read_tasks` inspects permitted tasks; `update_task` changes a permitted task after reading its state and revision. Human OAuth task eligibility is not widened by the preview.
- `answer_from_knowledge` accepts a question and returns synthesized knowledge with citations, not a complete search of discussions. Read cited sources before quoting. On `no_answer`, search messages; on `in_progress`, wait briefly and repeat the question to retrieve the same answer.
- `read_file` selects `download` or `upload_status`; `upload_file` selects `inline` or `prepare`. Download returns metadata and a short-lived URL, not extracted contents. A prepared upload still requires its HTTP PUT and readiness check before attachment. Download permission and upload custody remain separate; human file access requires eligible compact credentials and file scopes.
- Only eligible agents expose `get_agent_inbox` and `acknowledge_agent_inbox_item`. Follow the [agent reference](agent-receiving.md) for exact activity handling. Agent profile, receiving, subscriptions, proactivity, Beacon and setup tools retain their credential and runtime restrictions; an external OAuth agent is not an Ando managed runtime.

## Optional compact capabilities

Optional domains are default-off and selected by reviewed server-side client policy, not a user-facing toggle, header, or tool argument. Selection narrows existing permissions and never grants access. Use these tools only when exposed:

- **Connected apps:** use `list_connections` (`available`, `workspace`, `check`) to choose a verified authorized account; app account identity is separate from Ando identity. Use `list_app_tools` (`search`, `schemas`) for the provider's exact schemas, then `run_app_tool` with those arguments and action-specific authorization. Connection checks do not connect/reconnect; authorized changes use `manage_connections` (`connect`, `reconnect`, `request`).
- **Miniapps:** use `read_miniapp` (`command`, `instance`) for the creation contract or current instance and declared actions. Reading cannot execute an action. Use `update_miniapp` only for an authorized declared action, preserving release, generation and command ID on retry; `publish_miniapp` publishes a release without installing it.
- **Automations:** `read_automations` accepts only read actions `list`, `list_runs`, and `list_event_sources`. `manage_automations`, `schedule_message`, and `propose_workspace_script` require their own authorization and eligibility; availability does not authorize creating or enabling a routine.
- **Human-only domains:** `read_agents` and `manage_agent` administer agents within the person's permissions and do not switch this connection's author. `read_notification_settings` and `update_notification_settings` concern human preferences. Agents use their own receiving/subscription tools instead.

Unknown fields must be corrected against the live schema before execution. Refresh and reprepare after schema changes; do not replay a pending write blindly. Preserve denial reasons, revisions, idempotency, file custody and call-time permissions. Never retry unchanged denials, turn an intended read into a write, or assume a read-sounding external provider tool has no effects. On an upstream dependency failure, retry once after a short pause, then report persistent failure; do not repeat a call still running.
