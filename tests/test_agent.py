import pytest
from src.agents.loan_agents import DisbursementPlannerAgent

def test_disbursement_schedule_math():
    planner = DisbursementPlannerAgent()
    # Test with ₹1,000,000 principal at 8.5% for 40 quarters
    schedule = planner.generate_schedule(principal=1000000, annual_rate=8.5, quarters=40)
    
    # Assertions to ensure FDE system integrity
    assert len(schedule) == 40
    assert schedule[0]["quarter"] == 1
    assert schedule[-1]["remaining_balance"] == 0.0
    print("✅ Disbursement Planner agent math checks out perfectly!")

if __name__ == "__main__":
    test_disbursement_schedule_math()
