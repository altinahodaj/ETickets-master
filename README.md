# ETickets – Master Project

ETickets is a web application for managing cinemas, movies, events, tickets, and reviews.
This repository contains the version adapted and extended for the Master studies.

## Features
- Authentication (JWT)
- Cinemas, Halls, Rows & Seats
- Movies, Photos, Actors
- Movie Times / Schedules
- Events
- Tickets & Reservations
- Reviews

## Tech Stack
- Backend: Python (FastAPI)
- Database: PostgreSQL + Alembic migrations
- Frontend: Vue.js
- (Optional) Node.js service: `node/`

## Project Structure
- `backend/` – FastAPI API + database models + migrations
- `client-side/` – Vue.js frontend
- `node/` – optional Node.js service (if used)

## Requirements
- Python 3.x
- Node.js (for frontend)
- PostgreSQL

## Setup

### 1) Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
