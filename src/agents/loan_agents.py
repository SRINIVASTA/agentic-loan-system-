import math

class DataCollectorAgent:
    def extract_metrics(self, application_text: str) -> dict:
        # FDE Parse logic
        return {"income": 120000, "requested_amount": 1000000, "employment_status": "Employed"}

class DataVerifierAgent:
    def verify(self, id_data: dict, letter_data: dict) -> bool:
        # Deterministic trust gate cross-checking
        return id_data.get("name") == letter_data.get("name", "Unknown")

class LoanProcessingOfficerAgent:
    def __init__(self, memory_engine):
        self.memory = memory_engine

    def underwrite(self, financial_profile: dict, credit_data: dict) -> str:
        policy = self.memory.query_policy("Check debt to income ratios")
        if credit_data.get("score", 0) > 700:
            return "APPROVED"
        return "REJECTED"

class DisbursementPlannerAgent:
    def generate_schedule(self, principal: float, annual_rate: float, quarters: int = 40) -> list:
        r = (annual_rate / 100) / 4
        eqi = principal * (r * ((1 + r) ** quarters)) / (((1 + r) ** quarters) - 1)
        
        schedule = []
        remaining_balance = principal
        for q in range(1, quarters + 1):
            interest = remaining_balance * r
            principal_paydown = eqi - interest
            remaining_balance -= principal_paydown
            schedule.append({
                "quarter": q,
                "eqi": round(eqi, 2),
                "principal_paydown": round(principal_paydown, 2),
                "interest_paid": round(interest, 2),
                "remaining_balance": max(0, round(remaining_balance, 2))
            })
        return schedule
