# Universal OpenADR Hybrid System (2.0b & 3.0)

This project implements a complete OpenADR environment featuring a **Hybrid VTN Server** and a **Universal VEN Simulator** that supports both legacy 2.0b (XML) and modern 3.0 (JSON) protocols simultaneously.

## 🚀 Features
- **Universal VEN Simulator:** An asynchronous client that manages telemetry and events for both 2.0b and 3.0 standards in one runtime.
- **Hybrid VTN Infrastructure:**
  - **OpenADR 3.0:** Implemented with Django and REST Framework (JSON/REST).
  - **OpenADR 2.0b:** Implemented with OpenLEADR (XML/SOAP).
- **Auto-Generated API Docs:** Integrated Swagger UI for testing OpenADR 3.0 endpoints.

---

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   
2. **Install dependencies:**
    ```bash
   pip install -r requirements.txt
3. **Initialize Database for Django (OpenADR 3.0):**
   ```bash
   python manage.py migrate
   
# 🚦 How to Run
To see the full simulation in action, open three separate terminals:

## Terminal 1: Start OpenADR 3.0 VTN (Django)

1.  **This runs the modern REST-based server:**
    ```bash
    python manage.py runserver
Access Swagger UI at:http://127.0.0.1:8000/swagger/
2.  **Terminal 2 : Start OpenADR 2.0b VTN**
    ```bash
    python vtn_server_2.py
3. **Terminal 3: Start Universal VEN Simulator**
    ```bash
    python VEN_Simulation.py
   
# 🧠 Implementation Details
#### Asynchronous Engine: Built on asyncio to handle multiple protocol drivers without blocking.

#### Shared State Logic: The VEN simulator uses a single internal state. If a "Demand Response" event is received via 2.0b, the simulator automatically adjusts its power consumption, which is then reflected in the reports sent to both 2.0b and 3.0 servers.

#### Standard Compliance: Uses drf-spectacular for OpenAPI 3.0 schemas and openleadr for robust 2.0b XML handshake and reporting.
