MES Simulator
A backend system simulating a real-world Manufacturing Execution System (MES) built with FastAPI and PostgreSQL. Models the complete production lifecycle from ERP order release through shop floor execution, quality disposition, and analytics — the same flow found in enterprise systems like Siemens Opcenter and SAP ME.

Business Context
Manufacturing Execution Systems are the operational layer between ERP planning (SAP, Oracle) and the physical shop floor. They answer the real-time question: what is happening on the factory floor right now?
This simulator models that layer end-to-end:

An ERP system releases a production order
The MES generates work orders and serialized shop floor control (SFC) units
Operators start and complete work orders, advancing units through operations
Quality checks disposition each unit: Pass, Rework, or Scrap
Analytics surface yield %, scrap %, WIP count, and bottleneck detection in real time


Tech Stack
LayerTechnologyAPI FrameworkFastAPIDatabasePostgreSQL 15ORMSQLAlchemy 2.0MigrationsAlembicRuntimePython 3.11+ServerUvicorn

Architecture
ERP Order
    │
    ▼
POST /api/orders/release
    │
    ▼
Work Orders created (Assembly → Testing → Packaging)
    │
    ▼
SFC units serialised and assigned to Work Order 1
    │
    ▼
POST /api/execution/workorders/{wo_id}/start
POST /api/execution/workorders/{wo_id}/complete  ──► SFCs advance to next op
    │
    ▼
POST /api/quality/{sfc_id}  ──► PASS / REWORK / SCRAP
    │
    ▼
GET /api/dashboard/   ──► Yield %, Scrap %, WIP, OEE
GET /api/analytics/   ──► State distribution, bottleneck detection

API Endpoints
Orders
MethodEndpointDescriptionPOST/api/orders/Create a production orderGET/api/orders/{order_id}Get order statusPOST/api/orders/{order_id}/releaseRelease order to shop floor
Execution
MethodEndpointDescriptionPOST/api/execution/workorders/{wo_id}/startStart a work orderPOST/api/execution/workorders/{wo_id}/completeComplete and advance SFCs
Quality
MethodEndpointDescriptionPOST/api/quality/{sfc_id}Run quality check (Pass / Rework / Scrap)
Dashboard & Analytics
MethodEndpointDescriptionGET/api/dashboard/Yield %, scrap %, WIP, completed unitsGET/api/analytics/SFC state distribution, bottleneck stageGET/api/machine/statusSimulated machine health status
Full interactive documentation available at /docs (Swagger UI) when running locally.

Data Model
Order → has many WorkOrders (one per operation) → each WorkOrder has many SFCs (one per serialised unit)

Order — ERP reference, product code, quantity, status lifecycle
WorkOrder — operation sequence, name, machine/operator assignment, actual start/end timestamps
SFC — serial number, state machine (NEW → IN_QUEUE → ACTIVE → DONE / IN_REWORK / SCRAPPED), defect code, rework count
AuditLog — full change history on every order state transition


Getting Started
Prerequisites

Python 3.11+
PostgreSQL running locally

Setup
bash# Clone the repo
git clone https://github.com/avummdedhiaa24-ship-it/mes-simulator.git
cd mes-simulator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://mes_user:mes_pass123@localhost/mes_db" > .env

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
Open http://127.0.0.1:8000/docs to access the Swagger UI.
Example: Full production lifecycle
bash# 1. Create an order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"erp_ref": "ERP-001", "product_code": "PCB-MKII", "quantity": 10}'

# 2. Release it to the shop floor
curl -X POST http://localhost:8000/api/orders/{order_id}/release

# 3. Start the first work order
curl -X POST http://localhost:8000/api/execution/workorders/{wo_id}/start

# 4. Complete it — SFCs automatically advance to next operation
curl -X POST http://localhost:8000/api/execution/workorders/{wo_id}/complete

# 5. Check the dashboard
curl http://localhost:8000/api/dashboard/

Key MES Concepts Modelled
Shop Floor Control (SFC) — Each serialised unit is tracked individually through every operation. If a unit fails quality, it enters a rework loop (max 1 rework) before being scrapped.
Operation sequencing — Work orders are created for Assembly (seq 1), Testing (seq 2), and Packaging (seq 3). When a work order completes, SFCs are automatically reassigned to the next operation's work order.
Quality disposition — Each unit is measured against upper/lower control limits. Results are persisted with defect codes, enabling downstream Pareto analysis.
Audit trail — Every order state transition is logged to audit_logs with old/new values and a timestamp, matching ISA-95 traceability requirements.

Project Structure
mes-simulator/
├── app/
│   ├── db/
│   │   └── database.py          # SQLAlchemy engine and session
│   ├── models/
│   │   ├── order.py             # Order, AuditLog models
│   │   └── production.py        # WorkOrder, SFC models
│   ├── routers/
│   │   ├── orders.py
│   │   ├── execution.py
│   │   ├── quality.py
│   │   ├── dashboard.py
│   │   ├── analytics.py
│   │   └── machine.py
│   ├── schemas/
│   │   └── order.py             # Pydantic request/response models
│   ├── services/
│   │   ├── order_service.py
│   │   ├── production_service.py
│   │   ├── execution_service.py
│   │   ├── quality_service.py
│   │   ├── dashboard_service.py
│   │   ├── analytics_service.py
│   │   └── machine_service.py
│   └── main.py
├── alembic/                     # Database migration scripts
├── alembic.ini
├── requirements.txt
└── README.md
