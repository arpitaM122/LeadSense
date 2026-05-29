# Lead Intelligence Backend

## Setup
1. Copy `.env.example` to `.env` and fill in your Twilio credentials.
2. Run `docker-compose up --build`
3. API will be available at `http://localhost:8000`

## Endpoints
- `POST /api/v1/webhook/twilio` – Twilio incoming message webhook
- `POST /api/v1/feedback` – Human feedback (override)
- `GET /health` – Health check

## Training
Run `python -m app.training.train_model` after collecting ~2000 labeled conversations.