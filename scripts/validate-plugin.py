"""Validate the static Ando plugin package without network access or secrets."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = json.loads((root / 'plugin.json').read_text())
mcp = json.loads((root / 'mcp.json').read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


require(plugin.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Unexpected plugin format')
require(plugin.get('name') == 'ando', 'Plugin identity must remain ando')
require(isinstance(plugin.get('version'), str) and re.fullmatch(r'\d+\.\d+\.\d+', plugin['version']), 'Expected a release version')
require(isinstance(plugin.get('description'), str) and plugin['description'].strip(), 'Description is required')
require(mcp == {
    '$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
    'mcpServers': {'ando': {'type': 'streamable-http', 'url': 'https://mcp.ando.so/mcp'}},
}, 'The MCP manifest must remain URL-only with the production HTTPS endpoint')

skills = list((root / 'skills').glob('*/SKILL.md'))
require(bool(skills), 'At least one skill is required')
for skill in skills:
    text = skill.read_text()
    require(text.startswith('---\n'), f'{skill}: missing frontmatter')
    sections = text.split('---\n', 2)
    require(len(sections) == 3 and sections[2].strip(), f'{skill}: missing closing delimiter or body')
    fields = {}
    for line in sections[1].splitlines():
        key, separator, value = line.partition(':')
        require(separator and key not in fields, f'{skill}: invalid or duplicate frontmatter field')
        fields[key] = value.strip()
    require(fields.get('name') == skill.parent.name, f'{skill}: name must match its directory')
    require(bool(fields.get('description')), f'{skill}: description is required')

compact_routing = (root / 'skills/ando/references/compact-routing.md').read_text()
for tool_name in (
    'save_wiki_page',
    'update_channel_context',
    'list_calls',
    'read_call',
    'create_task',
    'report_task_progress',
    'change_task_status',
    'connect_app_account',
    'search_app_tools',
    'get_app_tool_schemas',
    'get_miniapp_command',
    'get_miniapp_instance',
):
    require(f'`{tool_name}`' in compact_routing, f'compact-routing.md: missing reviewed tool {tool_name}')

for retired_name in (
    'update_knowledge',
    'read_jam',
    'update_task',
    'manage_connections',
    'list_app_tools',
    'run_app_tool',
    'read_miniapp',
    'update_miniapp',
    'manage_beacon',
    'update_agent_profile',
):
    require(f'`{retired_name}`' not in compact_routing, f'compact-routing.md: retired preview tool {retired_name}')

receiving = (root / 'skills/ando/references/agent-receiving.md').read_text()
require(
    '**Settings → Members → Agents**' in receiving
    and '**Replies → Webhook URL / Sender key**' in receiving,
    'agent-receiving.md: missing current Replies settings path',
)
require('Message delivery**' not in receiving, 'agent-receiving.md: stale Message delivery settings path')

readme = (root / 'README.md').read_text()
require(
    f'Version {plugin["version"]}' in readme,
    'README.md: release notes must match plugin.json version',
)
print(f'Validated plugin {plugin["version"]}, URL-only MCP configuration and {len(skills)} skill(s).')
