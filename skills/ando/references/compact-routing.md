# Routing for compact and human catalog connections

Do not create another connection, change an OAuth registration, or migrate a legacy caller or routine based on this reference. Use it only when the live tool schemas and overview establish `human-v1` or `compact-v1`. Reviewed new OAuth client registrations may receive `compact-v1` by server policy; existing clients keep their saved catalog unless explicitly migrated. The active schema takes precedence because these catalogs have different contracts even when tool names match.

## Identity and shared collaboration

Call the exposed `get_workspace_overview` with no arguments. For `compact-v1`, its result contains `principal.principal_type`, `principal.workspace_membership_id`, a separate `workspace.id`, `catalog_version`, and granted capabilities. Verify the intended workspace and membership using the actual result. This bounded overview does not read an inbox or configure receiving. If identity/catalog cannot be verified, stop dependent work and refresh the connection through the host's supported flow. A flat MCP tool list is sufficient; do not require custom catalog metadata.

Tools with modes use `{request: {kind: ..., ...operationFields}}`, even if only one mode is granted. Single-operation tools retain their discovered arguments. Never apply this envelope to a legacy tool because its name looks familiar.

- `send_message` uses `conversation`, `thread`, or `direct` for the requested destination. Preserve the original thread/recipients, content, file IDs and retry key. `save_message_draft` saves without sending. Rich cards and miniapp inputs use the permitted `send_message` fields; human sends exclude agent-only content.
- `read_conversation` selects `context`, `messages`, `threads`, or `time_range`; `read_thread` reads replies. Preserve pagination, filters and source links.
- `search_knowledge` and `read_knowledge` select the granted resource mode. Use `save_wiki_page` for Wiki publication and `update_channel_context` for structured channel edits. Retain exact resource identity, audience, revision and source requirements.
- `list_members`, `list_conversations`, `list_calls`, and `read_call` use the modes actually exposed. Do not copy a compact mode into a human or legacy schema.

`human-v1` is a separate human-only preview. Use its exposed collaboration tools without agent inbox, profile, or receiving preflight. In particular, `list_conversations` keeps its original flat arguments, `list_members` supports workspace/conversation modes, `list_jams` retains the list operation's arguments, and knowledge modes cover Wiki/channel resources. Do not assume compact file, task, semantic search, optional-domain tools, or additional modes exist. See the [human catalog mapping](https://docs.ando.so/docs/ando-mcp#human-catalog-and-migration), then use the live schema.

## Direct compact task tools

The current `compact-v1` catalog exposes task tools directly. The earlier `discover_capabilities`, `read_capability`, and `run_capability` dispatcher was removed. Refresh any earlier preview schemas; remove dispatcher `operation_id`, `schema_version`, and nested `arguments` envelopes when preparing calls, retaining fields declared by the destination schema itself. This does not authorize migrating saved routines.

- `read_tasks` inspects permitted tasks. Use the exact advertised task action after reading current state and revision, such as `create_task`, `report_task_progress`, or `change_task_status`. Human OAuth task eligibility is not widened by compact registration.
- `answer_from_knowledge` accepts a question and returns synthesized knowledge with citations, not a complete search of discussions. Read cited sources before quoting. On `no_answer`, search messages; on `in_progress`, wait briefly and repeat the question to retrieve the same answer.
- `read_file` selects `download` or `upload_status`; `upload_file` selects `inline` or `prepare`. Download returns metadata and a short-lived URL, not extracted contents. A prepared upload still requires its HTTP PUT and readiness check before attachment. Download permission and upload custody remain separate; human file access requires eligible compact credentials and file scopes.
- Only eligible agents expose inbox and receiving tools. Follow the [agent reference](agent-receiving.md) for exact activity handling. Current reviewed names include `acknowledge_agent_inbox_batch`, `authorize_agent_event_connection`, `revoke_agent_event_connection`, `update_agent_profile_details`, and `set_agent_profile_picture` when eligible. Agent profile, receiving, subscriptions, proactivity, event connections, and setup tools retain their credential and runtime restrictions; an external OAuth agent is not an Ando managed runtime.

## Optional compact capabilities

Optional domains are default-off and selected by reviewed server-side client policy, not a user-facing toggle, header, or tool argument. Selection narrows existing permissions and never grants access. Use these tools only when exposed:

- **Connected apps:** use `list_connections` (`available`, `workspace`, `check`) to choose a verified authorized account; app account identity is separate from Ando identity. Use `search_app_tools` and `get_app_tool_schemas` for exact provider contracts, then call only the authorized typed `app_…` action exposed by the live catalog. Connection checks do not connect or reconnect; authorized changes use `connect_app_account` (`connect`, `reconnect`, `request`).
- **Miniapps:** use `get_miniapp_command` for a creation contract and `get_miniapp_instance` for current records and declared actions. Reading cannot execute an action. Use only an authorized typed `mini_…` action advertised by the instance, preserving installation, release, generation and command ID on retry; `publish_miniapp` publishes a release without installing it.
- **Automations:** `read_automations` accepts only read actions `list`, `list_runs`, and `list_event_sources`. `manage_automations`, `schedule_message`, and `propose_workspace_script` require their own authorization and eligibility; availability does not authorize creating or enabling a routine.
- **Human-only domains:** `read_agents` and `manage_agent` administer agents within the person's permissions and do not switch this connection's author. `read_notification_settings` and `update_notification_settings` concern human preferences. Agents use their own receiving/subscription tools instead.

Unknown fields must be corrected against the live schema before execution. Refresh and reprepare after schema changes; do not replay a pending write blindly. Preserve denial reasons, revisions, idempotency, file custody and call-time permissions. Never retry unchanged denials, turn an intended read into a write, or assume a read-sounding external provider tool has no effects. On an upstream dependency failure, retry once after a short pause, then report persistent failure; do not repeat a call still running.

## Find names, correct arguments, and finish

Read the full tool declaration, not only a truncated discovery summary. For `compact-v1` name lookup, use `list_members({"request":{"kind":"workspace","query":"Chief Approval"}})` and `list_conversations({"request":{"kind":"list","q":"pr-approvals"}})`, replacing names with the requested target. Do not assume a separate search mode exists. Use `conversation_kind` only when it appears in the live schema.

An invalid-mode error should be corrected using its supported modes. Correct unknown fields using the full schema; refresh only when that schema disagrees with the server. Reconnect only for authentication or identity recovery. After a read succeeds, resume the original authorized task. Finding a recipient is not completion of a requested send. Message bodies use `markdown_content` where required by the declaration.

Follow returned `next_page.tool` and `next_page.arguments`, even on an empty page. Older servers may expose only their existing cursor envelope: preserve all filters and follow it to exhaustion. A Jam query failure means results are unavailable, not that no Jams exist. Report partial coverage when continuation is unavailable.

Plugin version, server revision, and catalog version are distinct. When available, read the overview's `server_revision`, `catalog_fingerprint`, `supported_modes` and unavailable-capability reasons. A null server revision is unknown. Compare the server catalog with this host's full declarations; the host may expose a subset. The canonical task guide is https://docs.ando.so/docs/ando-mcp#complete-a-task-with-the-current-catalog.
