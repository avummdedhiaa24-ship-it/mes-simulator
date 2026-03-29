# 🚀 MES Simulator (Manufacturing Execution System)

A backend system simulating a real-world Manufacturing Execution System (MES) using FastAPI and PostgreSQL.

---

## 🧠 Overview

This project models the complete production lifecycle:

ERP Order → Work Orders → SFC Tracking → Execution → Quality → Analytics

---

## ⚙️ Tech Stack

- FastAPI (Backend)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Python 3.11

---

## 🔥 Features

### 📦 Order Management
- Create and release production orders
- ERP-style references

### 🏭 Production Planning
- Automatic work order generation
- Multi-step operations (Assembly, Testing, Packaging)

### 🔢 SFC Tracking
- Serialized unit tracking (Shop Floor Control)
- Unique serial numbers per unit

### ⚙️ Execution Engine
- Start and complete work orders
- State transitions (NEW → ACTIVE → DONE)

### ✅ Quality Control
- Pass/Fail validation
- Rework loop
- Scrap handling

### 📊 Analytics Dashboard
- Total units
- Yield %
- Scrap %
- WIP tracking

---

## 📡 API Endpoints

### Orders
- `POST /api/orders/`
- `POST /api/orders/{order_id}/release`

### Execution
- `POST /api/execution/workorders/{wo_id}/start`
- `POST /api/execution/workorders/{wo_id}/complete`

### Quality
- `POST /api/quality/{sfc_id}`

### Dashboard
- `GET /api/dashboard/`

---

## 🚀 How to Run

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/mes-simulator.git

cd mes-simulator

# Create virtual env
python3 -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload