# 🎬 E-Tickets - Startup Guide

## Problemi: "Vetëm loading po shfaqet"

Kjo ndodh kur:
- ❌ Backend-et (Python + Node) nuk janë duke u ekzekutuar
- ❌ Frontend-i nuk di URL-në e backend-eve
- ❌ Databaza nuk është duke u ekzekutuar

## ✅ Zgjidhja: Fillo të gjitha serverat

### 1️⃣ Fillo Python Backend (Port 8001)

```powershell
cd backend
# Nëse nuk e ke virtual environment:
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalo dependencies (herën e parë):
pip install -r requirements.txt

# Fillo serverin:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 2️⃣ Fillo Node Backend (Port 3000)

Hap një terminal të ri:
```powershell
cd node

# Instalo dependencies (herën e parë):
npm install

# Fillo serverin:
npm start
```

### 3️⃣ Fillo Vue Frontend (Port 8080)

Hap një terminal të tretë:
```powershell
cd client-side

# Instalo dependencies (herën e parë):
npm install

# Fillo serverin:
npm run serve
```

### 4️⃣ Kontrollo Databasën

Sigurohu që PostgreSQL është duke u ekzekutuar dhe databaza `etickets_py_db` ekziston.

## 🚀 Hapi më i shpejtë (3 terminale njëkohësisht):

**Terminal 1:**
```powershell
cd backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000
```

**Terminal 2:**
```powershell
cd node; npm start
```

**Terminal 3:**
```powershell
cd client-side; npm run serve
```

## 🌐 Hap në Browser

Pas 30 sekondave, hap:
- **Frontend:** http://localhost:8080
- **Python API:** http://localhost:8001
- **Node API:** http://localhost:3000

## ❗ Nëse problemi vazhdon:

1. Kontrollo Console në browser (F12)
2. Shiko për gabime si "Failed to fetch" ose "Network Error"
3. Sigurohu që të 3 serverat janë duke u ekzekutuar pa gabime
