install-backend:
	cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt

test:
	cd backend && .venv/bin/pytest ../tests -q

backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev
