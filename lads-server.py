import asyncio
import pprint
import time

from fastmcp import FastMCP, Client
from fastmcp.exceptions import ToolError

client = Client("http://192.168.0.100:8080/mcp")
mcp = FastMCP("JASIS MCP Wrapper")

@mcp.tool
async def get_ph() -> dict:
    """Get current pH value."""
    async with client:
        result = await client.call_tool("ladsflow_get_ph_meter_value")
    return result.data

@mcp.tool
async def get_unit_status(unit_id: int) -> dict:
    """Get unit status specified by an integer 1 or 2."""
    async with client:
        result = await client.call_tool("ladsflow_get_unit_status", {"unit_id": unit_id})
    return result.data

@mcp.tool
async def inflow_start(duration: int) -> dict:
    """Start inflow pump for duration (s).
    This tool should not be used to adjust pH."""
    args_in = {
        "unit_id": 2,
        "program_template_id": "FLOW_DISPENSE_V1",
        "supervisory_job_id": "mcp-01",
        "supervisory_task_id": "mcp-task-01",
        "properties": [
            {"key": "TargetFlowMlMin", "value": "100"},
            {"key": "RunDurationSec", "value": str(duration)},
        ],
        "samples": [],
    }
    async with client:
        result = await client.call_tool("ladsflow_start_program", args_in)
    return result.data

@mcp.tool
async def inflow_stop() -> dict:
    """Stop inflow pump immediately."""
    args_stop = {
        "unit_id": 2,
    }
    async with client:
        result = await client.call_tool("ladsflow_stop_program", args_stop)
    return result.data

@mcp.tool
async def outflow_start(duration: int) -> dict:
    """Start outflow pump for duration (s).
    This tool should not be used to adjust pH."""
    args_out = {
        "unit_id": 1,
        "program_template_id": "FLOW_DISPENSE_V1",
        "supervisory_job_id": "mcp-01",
        "supervisory_task_id": "mcp-task-01",
        "properties": [
            {"key": "TargetFlowMlMin", "value": "100"},
            {"key": "RunDurationSec", "value": str(duration)},
        ],
        "samples": [],
    }
    async with client:
        result = await client.call_tool("ladsflow_start_program", args_out)
    return result.data

@mcp.tool
async def outflow_stop() -> str:
    """Stop inflow pump immediately."""
    args_stop = {
        "unit_id": 1,
    }
    async with client:
        result = await client.call_tool("ladsflow_stop_program", args_stop)
    return result.data

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=9000)