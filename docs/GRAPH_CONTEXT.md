# Graph context setup

`graphify` is a lightweight local static graph. No external API, database, or paid embeddings. Graph is generated on demand in `.graphify/graph.json`, refreshed incrementally, and ignored by Git.

```bash
python3 .agents/skills/graphify/scripts/graph.py sync --root .
python3 .agents/skills/graphify/scripts/graph.py query --root . --term payment
```

Optional MCP integration requires `pip install mcp` and an **absolute path** in your Codex configuration. Example (replace both placeholders):

```toml
[mcp_servers.graphify]
command = "python3"
args = ["/ABSOLUTE/PROJECT/.agents/skills/graphify/scripts/mcp_server.py", "/ABSOLUTE/PROJECT"]
```

Do not use a relative script path in global configuration; the MCP process may start in another working directory. Do not commit environment-specific absolute paths into a shared repo. Restart Codex after configuring MCP. Confirm the server and its tools appear in Codex before relying on them.

Automatic activation means Codex instructions select graph context for complex navigation tasks; **not** an always-running filesystem watcher. MCP refreshes graph on tool calls, CLI refreshes on invocation. For small edits `rg` is preferable. Static imports can miss dynamic imports, reflection, runtime dependencies and unresolved relative imports. Verify important edges in code.
