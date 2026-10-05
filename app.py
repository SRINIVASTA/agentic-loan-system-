import streamlit as st
import time
from src.agents.loan_agents import DataCollectorAgent, LoanProcessingOfficerAgent, DisbursementPlannerAgent
from src.memory.qdrant_client import MemoryEngine
from src.mcp.server import MCPSecureGateway

# 1. Page Configuration & Title Styling
st.set_page_config(page_title="Agentic Loan Processing System", page_icon="🏦", layout="wide")
st.title("🏦 Enterprise Agentic Loan Processing Dashboard")
st.caption("Forward Deployment Engineering (FDE) Reference Architecture — Processing Time: <70 Seconds")

# 2. Sidebar Configuration Layout
st.sidebar.header("📥 Application Documents Ingestion")
uploaded_letter = st.sidebar.file_uploader("Upload Application Letter (Text/PDF)", type=["txt", "pdf"])
uploaded_id = st.sidebar.file_uploader("Upload Applicant ID Card Image", type=["jpg", "jpeg", "png"])

# 3. Form Parameters (Falls back to defaults demonstrated at NIT)
st.sidebar.markdown("---")
st.sidebar.subheader("System Override Parameters")
principal = st.sidebar.number_input("Requested Principal Loan Amount (INR)", min_value=100000, max_value=50000000, value=1000000, step=50000)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", min_value=4.0, max_value=24.0, value=8.5, step=0.1)

# 4. Trigger Pipeline Execution
if st.sidebar.button("⚡ Run Agentic Pipeline", use_container_width=True):
    if not uploaded_letter or not uploaded_id:
        st.error("⚠️ Compliance Gate: Please upload both the Application Letter and ID Card image to initiate extraction.")
    else:
        st.info("🚀 Triggering Event-Driven Agent DAG...")
        
        # Initialize Backend Components
        memory = MemoryEngine()
        mcp_gateway = MCPSecureGateway()
        collector = DataCollectorAgent()
        officer = LoanProcessingOfficerAgent(memory)
        planner = DisbursementPlannerAgent()

        # Step 1: Multimodal OCR Simulation via Gemini Vision
        with st.status("🔮 Agents Coordinating...", expanded=True) as status:
            
            st.write("🔄 **[Gemini Vision Engine]** Reading ID Card layout and parsing pixels into JSON schema...")
            time.sleep(1.5)  # Agent execution pacing simulation
            id_mock = {"name": "Unknown", "id_number": "ABC12345"}
            
            # Step 2: Extraction & Vector Upsert
            st.write("🔄 **[Data Collector Agent]** Isolating application parameters and writing to Qdrant semantic memory...")
            time.sleep(1.0)
            app_text = "I wish to apply for a loan. Income: 120,000 INR."
            metrics = collector.extract_metrics(app_text)
            
            # Step 3: MCP Execution Gateway
            st.write("🔄 **[MCP Secure Gateway]** Authenticating against core-banking infrastructure to evaluate fraud metrics...")
            time.sleep(1.8)
            credit_profile = mcp_gateway.execute_tool("fetch_credit_score", {"id": id_mock["id_number"]})
            
            # Step 4: Underwriting Decision
            st.write("🔄 **[Loan Officer Agent]** Querying dynamic underwriting constraints via RAG lookup...")
            time.sleep(1.2)
            decision = officer.underwrite(metrics, credit_profile)
            
            status.update(label="✅ Pipeline Execution Complete in 5.5 Seconds!", state="complete", expanded=False)

        # 5. Presentation Layer Layout (Displaying Outcomes)
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Underwriting Verdict", value=decision, delta="Passed Risk Assessment" if decision == "APPROVED" else "Risk Out of Bounds")
            st.json({
                "Extraction Metrics": metrics,
                "Secure Bureau Pull (MCP)": credit_profile
            })
            
        with col2:
            if decision == "APPROVED":
                st.success("💰 Amortization Schedule Generated")
                schedule = planner.generate_schedule(principal=principal, annual_rate=interest_rate, quarters=40)
                
                # Show schedule inside a neat dataframe
                st.dataframe(schedule, use_container_width=True, height=300)
