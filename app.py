import streamlit as st
import time
import json
from google import genai
from google.genai import types

# CORE LINKAGE TO YOUR EXACT FILES
from src.agents.loan_agents import DataCollectorAgent, LoanProcessingOfficerAgent, DisbursementPlannerAgent
from src.mcp.server import MCPSecureGateway
from src.memory.qdrant_client import MemoryEngine

# ==========================================
# STREAMLIT PRESENTATION CONFIGURATION
# ==========================================
st.set_page_config(page_title="Agentic Loan Processing System", page_icon="🏦", layout="wide")
st.title("🏦 Enterprise Agentic Loan Processing Dashboard")
st.caption("Forward Deployment Engineering (FDE) Reference Architecture — Processing Time: Real-Time Verification")

# Sidebar Configuration Control Panel
st.sidebar.header("📥 Application Documents Ingestion")

# Password input field for the Gemini API Key
api_key = st.sidebar.text_input(
    "🔑 Enter your GEMINI_API_KEY", 
    type="password", 
    help="Get a free key from Google AI Studio. It is safely used locally in this session and never saved."
)

uploaded_letter = st.sidebar.file_uploader("Upload Application Letter (Text/PDF)", type=["txt"])
uploaded_id = st.sidebar.file_uploader("Upload Applicant ID Card Image", type=["jpg", "jpeg", "png"])

st.sidebar.markdown("---")
st.sidebar.subheader("System Override Parameters")
principal_override = st.sidebar.number_input("Requested Principal Loan Amount (INR)", min_value=100000, max_value=50000000, value=1000000, step=50000)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", min_value=4.0, max_value=24.0, value=8.5, step=0.1)

# Trigger Event-Driven Pipeline DAG Execution
if st.sidebar.button("⚡ Run Agentic Pipeline", use_container_width=True):
    if not api_key:
        st.error("❌ **Authentication Error:** A valid GEMINI_API_KEY is required to run real-time dynamic document verification. Please input your key in the sidebar.")
    elif not uploaded_letter or not uploaded_id:
        st.error("⚠️ Compliance Gate: Please upload both the Application Letter and ID Card image to initiate extraction.")
    else:
        st.info("🚀 Triggering Event-Driven Agent DAG...")
        
        # Initialize Google GenAI client directly with the provided key
        client = genai.Client(api_key=api_key)
        
        # Initialize your repository classes
        memory_engine = MemoryEngine()
        mcp_gateway = MCPSecureGateway()
        collector = DataCollectorAgent()
        officer = LoanProcessingOfficerAgent(memory_engine=memory_engine)
        planner = DisbursementPlannerAgent()

        # Phase 1: Parse the uploaded letter text file contents dynamically
        raw_letter_text = uploaded_letter.read().decode("utf-8")
        id_data = {}
        
        with st.status("🔮 Agents Coordinating & Verifying...", expanded=True) as status:
            # Phase 2: Dynamic Multi-modal OCR Analysis via Gemini Vision
            st.write("🔄 **[Gemini Vision Engine]** Interrogating ID Card layout and parsing pixels into structural JSON...")
            
            vision_prompt = """
            Analyze this ID card image. Extract the full name printed on it.
            Return your answer as a strict JSON object with no formatting markdown blocks, backticks, or extra text.
            Schema: {"name": "EXTRACTED_NAME"}
            """
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        types.Part.from_bytes(data=uploaded_id.getvalue(), mime_type=uploaded_id.type),
                        vision_prompt
                    ],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                id_data = json.loads(response.text)
            except Exception as e:
                status.update(label="❌ Vision Processing Failed", state="error")
                st.error(f"❌ **API Error:** Gemini Vision failed to extract data from the image: {e}")
                st.stop()

            # Dynamic extraction check
            extracted_id_name = id_data.get("name", "").strip().lower()
            st.write(f"🧬 **[Gemini Vision Engine]** Dynamically Found Name on ID Card: `{id_data.get('name')}`")
            
            # Phase 3: Dynamic Identity Verification Fraud Gate Check (FORCE OVERRIDE TRACE)
            st.write("🔄 **[Data Verifier Agent]** Cross-checking identity parameters against application letter contents...")
            time.sleep(0.8)
            
            # Force the sidebar to update immediately with values to bypass browser memory bugs
            st.sidebar.markdown("### 🛠️ Diagnostics (Last Run)")
            st.sidebar.text(f"🪪 ID Name Found: {id_data.get('name')}")
            st.sidebar.text(f"📄 Letter Match Status: {extracted_id_name in raw_letter_text.lower()}")
            
            # Checks if the DYNAMICALLY extracted name exists in the DYNAMICALLY read text file
            if not extracted_id_name or (extracted_id_name not in raw_letter_text.lower()):
                status.update(label="❌ Security Pipeline Tripped: Mismatch Found!", state="error")
                st.markdown("---")
                
                # Show explicit string contents directly in the main screen window
                st.error(f"❌ **FRAUD DETECTED BY VERIFIER AGENT:** Identity Mismatch.")
                st.warning(f"🪪 **Name Extracted from ID Card Image:** `{id_data.get('name')}`")
                st.info(f"📄 **Raw Text Found Inside Application Letter:**\n\n```text\n{raw_letter_text}\n```")
                st.stop() # Hard stop pipeline execution safely

            # Phase 4: Metric Extraction via your original Collector Agent
            st.write("🔄 **[Data Collector Agent]** Isolating systemic metrics from application text...")
            metrics = collector.extract_metrics(raw_letter_text)
            metrics["requested_amount"] = principal_override 

            # Phase 5: Fetch Credit Bureau Metrics through your real MCP Server class
            st.write("🔄 **[MCP Secure Gateway]** Standardizing JSON-RPC call arrays over system pipe registries...")
            time.sleep(1.0)
            credit_profile = mcp_gateway.execute_tool("fetch_credit_score", {"id": "ABC12345"})

            # Phase 6: Underwriting Evaluation Trace
            st.write("🔄 **[Loan Officer Agent]** Fetching dynamic RAG parameters from Qdrant vector memory indices...")
            time.sleep(0.7)
            decision = officer.underwrite(metrics, credit_profile)
            
            status.update(label="✅ Pipeline Execution Complete!", state="complete")

        # ==========================================
        # MULTI-COLUMN PRESENTATION DISPLAY
        # ==========================================
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Underwriting Metric Telemetry")
            if "REJECTED" in decision:
                st.error(f"Verdict: {decision}")
            else:
                st.success(f"Verdict: {decision} - Passed Risk Assessment")
                
            st.json({
                "Identity Scan (Gemini Vision)": id_data,
                "Extraction Metrics (Collector)": metrics,
                "Core-Banking Bureau Pull (MCP)": credit_profile
            })
            
        with col2:
            st.subheader("💰 Amortization Trend Visualizer")
            if "APPROVED" in decision:
                schedule_list = planner.generate_schedule(principal=principal_override, annual_rate=interest_rate, quarters=40)
                
                chart_data = {
                    "Principal Component": [item.get("principal_paydown", 0) for item in schedule_list],
                    "Interest Component": [item.get("interest_paid", 0) for item in schedule_list]
                }
                
                st.area_chart(chart_data, color=["#2e7d32", "#c62828"])
                st.write("📋 Complete Amortization Matrix Trace:")
                st.write(schedule_list)
