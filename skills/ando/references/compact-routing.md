# Compact routing for a separately opted-in connection

Preview activation is deferred. Do not create a preview connection, change an OAuth registration, or migrate a legacy caller or routine based on this reference. Use these instructions only after the connected server actually exposes and reports `compact-v1`; the live schema takes precedence over these examples.

## Identity and shared core

Call the exposed `get_workspace_overview` with its current schema. Its compact result contains `principal.principal_type`, `principal.workspace_membership_id`, a separate `workspace.id`, `catalog_version`, and granted capabilities. Verify the intended workspace and membership. This bounded overview does not read an inbox or configure receiving. If identity/catalog cannot be verified, stop dependent work and refresh the connection through the host's supported flow.

Common bundles use `{request: {kind: ..., ...operationFields}}`; single-operation tools keep the arguments shown by discovery. Never apply this envelope to a legacy tool because its name looks familiar.

- `send_message` uses `conversation`, `thread`, or `direct` for the requested destination. Preserve the original thread/recipients, content, file IDs and retry key. `save_message_draft` saves without sending.
- `read_conversation` selects the required read mode; `read_thread` reads replies. Preserve pagination, filters and source links.
- `search_knowledge`, `read_knowledge`, and `update_knowledge` select the granted resource mode. Retain exact resource identity, audience, revision and source requirements; do not confuse semantic file search with Wiki or channel Context.
- `read_file` selects `download` or `upload_status`; `upload_file` selects `inline` or `prepare`. A prepared upload still requires its HTTP PUT and readiness check before attachment. Download permission and upload custody remain separate.
- Only eligible agent connections expose `get_agent_inbox` and `acknowledge_agent_inbox_item`. Follow the agent reference for exact activity handling; a shared overview never authorizes inbox processing.

## Specialist discovery

Use `discover_capabilities` for a bounded category/query search. Fetch exact schemas for at most three returned operation IDs at a time, only as needed. Execute with the discovered `operation_id`, current `schema_version`, and exact `arguments`. Never guess IDs or copy the entire schema inventory into instructions.

Use `read_capability` only for a discovered read. It refuses mutations and unknown external effects. Use `run_capability` for an authorized mutation/external action only after reviewing its exact operation, target and arguments; approval for one operation does not authorize others behind the same executor. Rich message authoring and other specialist features require their own eligible discovered schemas.

Unknown fields and stale schema versions must be corrected before execution. Refresh and reprepare after schema changes; do not replay a pending write blindly. Discovery does not grant access to a resource. Preserve denial reasons, revisions, idempotency, file custody and call-time permissions; never retry unchanged denials or turn an intended read into a write.
