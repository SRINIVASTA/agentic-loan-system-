import pytest
from src.agents.loan_agents import DisbursementPlannerAgent
from src.mcp.server import MCPSecureGateway

def test_disbursement_schedule_math():
    """Validates that the Disbursement Planner Agent maintains balance reduction integrity."""
    planner = DisbursementPlannerAgent()
    # Test parameters: 1,000,000 INR principal, 8.5% annual rate, 40 quarters
    schedule = planner.generate_schedule(principal=1000000, annual_rate=8.5, quarters=40)
    
    # Assertions to ensure FDE system precision
    assert len(schedule) == 40, "Schedule must contain exactly 40 quarters."
    assert schedule[0]["quarter"] == 1, "Schedule must start at Quarter 1."
    assert schedule[-1]["remaining_balance"] == 0.0, "Final outstanding balance must resolve to 0."

def test_mcp_gateway_tools():
    """Validates that the MCP interface accurately extracts core-banking registries."""
    gateway = MCPSecureGateway()
    profile = gateway.execute_tool("fetch_credit_score", {"id": "ABC12345"})
    
    assert "score" in profile, "MCP payload must contain a numeric credit score."
    assert profile["score"] == 765, "Mock credit score should evaluate to 765."
    assert profile["tier"] == "PRIME", "765 bureau score must map to PRIME status tier."
