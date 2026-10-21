#!/usr/bin/env python3
"""Optional MCP stdio server. pip install mcp. Root passed as CLI arg."""
import sys
from pathlib import Path
from graph import sync, query, neighbors
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.exit('Missing dependency: pip install mcp')
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mcp=FastMCP('graphify-local')
@mcp.tool()
def graphify_query(term: str, limit: int = 12) -> list[dict]:
    """Find relevant local source files and Python symbols by term; incremental refresh."""
    g,_=sync(root)
    return query(g,term,max(1,min(limit,50)))
@mcp.tool()
def graphify_neighbors(node: str, limit: int = 20) -> list[dict]:
    """Return static Python import edges touching a repository-relative file path."""
    g,_=sync(root)
    return neighbors(g,node)[:max(1,min(limit,50))]
@mcp.tool()
def graphify_stats() -> dict:
    """Return local graph size after incremental refresh."""
    g,changed=sync(root)
    return {'files':len(g['nodes']),'edges':len(g['edges']),'changed':changed}
if __name__=='__main__':mcp.run(transport='stdio')
