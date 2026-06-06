# 💭 Thought Board

A public, open journal where anyone can share a passing thought. Built with **FastAPI** + **SQLite** + vanilla HTML/CSS/JS.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- Post anonymous or named thoughts (up to 500 chars)
- Live feed with relative timestamps
- Delete any thought
- Stats counter
- Fully self-contained — no external DB required

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/thoughts-board.git
cd thoughts-board
```

**2. Create a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**
```bash
cp .env.example .env
# Edit .env if needed
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🐳 Run with Docker

```bash
docker build -t thoughts-board .
docker run -p 8000:8000 thoughts-board
```

---

## ☁️ Deploy to Render (Free)

1. Fork this repo
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your forked repo — Render auto-detects `render.yaml`
4. Click **Deploy**

> Note: Render's free tier uses an ephemeral filesystem, so the SQLite DB resets on redeploy. For persistent storage, set `DATABASE_URL` to a PostgreSQL connection string (Render offers a free Postgres instance).

---

## 🔧 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./thoughts.db` | SQLAlchemy DB connection string |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated allowed CORS origins |

---

## 📡 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/thoughts` | List thoughts (newest first) |
| `POST` | `/api/thoughts` | Create a new thought |
| `DELETE` | `/api/thoughts/{id}` | Delete a thought |
| `GET` | `/api/stats` | Total thought count |

Interactive docs available at `/docs` when running locally.

---

## 📄 License

MIT
