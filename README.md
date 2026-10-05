# 🏦 Agentic Loan Processing System

An end-to-end, multi-agent automated loan underwriting workflow that processes unstructured credit requests and ID verifications in under 70 seconds. Built using an FDE (Forward Deployment Engineer) architectural framework.

## ⚙️ Architecture & Features
- **Multimodal Extraction:** Gemini Vision reads applicant IDs directly into structured JSON schemas.
- **Semantic Memory:** Qdrant vector database indexes application letters and handles zero-code policy retrieval.
- **Secure Integration:** Model Context Protocol (MCP) securely orchestrates legacy core banking APIs and fraud networks.
- **Deterministic Math:** Automated disbursement scheduler plotting 40-quarter fixed-payment schedules.

## 🗺️ System Design Architecture Topology

```mermaid
graph TD
    %% Styling and Configuration
    classDef storage fill:#1e1e24,stroke:#3a3a4a,stroke-width:2px,color:#ffffff;
    classDef agent fill:#0d47a1,stroke:#1565c0,stroke-width:2px,color:#ffffff;
    classDef gate fill:#b71c1c,stroke:#e53935,stroke-width:2px,color:#ffffff;
    classDef compute fill:#1b5e20,stroke:#2e7d32,stroke-width:2px,color:#ffffff;
    classDef ui fill:#e65100,stroke:#f57c00,stroke-width:2px,color:#ffffff;

    %% Presentation Layer
    subgraph UI_Layer ["🌐 USER PRESENTATION LAYER (Streamlit App)"]
        A["📥 Input Documents Ingestion <br> (LETTER TO BANK.txt + ID CARD.png)"] --> B{"🔑 Is GEMINI_API_KEY <br> Provided in Sidebar?"}
    end
    class A ui;
    class B gate;

    %% Routing Decisions & Ingestion
    subgraph Ingestion_Layer ["⚡ INGESTION & RUNTIME VECTOR ENGINE"]
        B -- "YES" --> C["🔮 Live OCR Processing Mode <br> (Gemini 2.5 Flash API)"]
        B -- "NO / Quota Over" --> D["🟡 Adaptive Demo Simulation Mode <br> (Stable Local Fallback Buffer)"]
        
        C --> E["🪪 Extract Dynamic Name String <br> from Photo Pixels"]
        D --> F["🪪 Fallback Identifier Token <br> Set to 'SRINIVASTA'"]
    end
    class C,E compute;
    class D,F storage;

    %% Multi-Agent Directed Acyclic Graph (DAG) Execution
    subgraph Agent_Core ["🧠 EVENT-DRIVEN MULTI-AGENT DAG CORE"]
        E --> G["🔄 Data Verifier Agent"]
        F --> G
        G --> H{"🕵️‍♂️ Identity Mismatch Check <br> (Is Name inside Letter Text?)"}
        
        H -- "FAIL (False)" --> I["❌ Compliance Rejection <br> (Halt Processing Gate)"]
        H -- "PASS (True)" --> J["📊 Data Collector Agent"]
        
        J --> K["🔍 Isolate Income & Quantum <br> Write to Qdrant Semantic Memory"]
        
        K --> L["🔌 MCP Secure Gateway <br> (JSON-RPC External Protocol)"]
        L --> M["🏦 Query Core Banking APIs <br> (Pull Credit Score & AML Indicators)"]
    end
    class G,J agent;
    class H,I gate;
    class K,L,M compute;

    %% Decision & Execution Outputs
    subgraph Underwriting_Disbursement ["💰 RISK EVALUATION & STRUCTURING ENGINE"]
        M --> N["📋 Loan Processing Officer Agent"]
        N --> O{"🛡️ Underwriting Evaluation <br> (Score > 650 & DTI Ratio Clear?)"}
        
        O -- "REJECTED" --> P["⚠️ Risk Suspension Alert <br> (Render Failure Logs)"]
        O -- "APPROVED" --> Q["📈 Disbursement Planner Agent"]
        
        Q --> R["🧮 Compute Reducing-Balance <br> Amortization Logic Formula"]
        R --> S["💰 Amortization Trend Visualizer <br> (Render Area Charts & Data Grid Table)"]
    end
    class N,Q agent;
    class O gate;
    class P,R,S compute;

    %% Global Triggers to UI Presenter
    I --> T["🚨 UI Error Banner Display"]
    P --> U["📊 Underwriting JSON Telemetry Log"]
    S --> V["📋 Sortable 40-Quarter Enterprise Matrix Grid"]
    class T,U,V ui;
```

## 🚀 Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export GEMINI_API_KEY="your-key"
export QDRANT_URL="http://localhost:6333"
```

3. Run the processing engine:
```bash
python src/main.py
```
