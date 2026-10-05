from src.agents.loan_agents import DataCollectorAgent, LoanProcessingOfficerAgent, DisbursementPlannerAgent
from src.memory.qdrant_client import MemoryEngine
from src.mcp.server import MCPSecureGateway

def run_pipeline():
    print("🚀 Initializing Agentic Loan Processing Pipeline...")
    
    # Initialize Core Engines
    memory = MemoryEngine()
    mcp_gateway = MCPSecureGateway()
    
    # Execution Payload Simulated
    app_text = "I wish to apply for a loan of 1,000,000 INR. My monthly income is 120,000 INR."
    id_mock = {"name": "Unknown", "id_number": "ABC12345"}
    
    # 1. Metric Extraction
    collector = DataCollectorAgent()
    metrics = collector.extract_metrics(app_text)
    print(f"[Collector] Extracted data: {metrics}")
    
    # 2. Secure External MCP calls
    credit_profile = mcp_gateway.execute_tool("fetch_credit_score", {"id": id_mock["id_number"]})
    print(f"[MCP Gateway] Credit profile verified: {credit_profile}")
    
    # 3. Dynamic Underwriting
    officer = LoanProcessingOfficerAgent(memory)
    decision = officer.underwrite(metrics, credit_profile)
    print(f"[Underwriter] Decision: {decision}")
    
    # 4. Amortization Allocation
    if decision == "APPROVED":
        planner = DisbursementPlannerAgent()
        schedule = planner.generate_schedule(principal=1000000, annual_rate=8.5, quarters=40)
        print(f"[Planner] Generated schedule successfully. First quarter EQI: {schedule[0]['eqi']} INR")

if __name__ == "__main__":
    run_pipeline()
