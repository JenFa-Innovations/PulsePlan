# PulsePlan – Backend

This is the backend service for **PulsePlan**, a smart, adaptive scheduling assistant.  
It is built with **FastAPI**, uses **SQLite** for local development, and provides a REST API for mobile and desktop clients.

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – high-performance Python web framework
- [SQLite](https://sqlite.org) – embedded relational database
- [Pydantic](https://pydantic-docs.helpmanual.io/) – for data validation and config
- [Docker](https://www.docker.com/) – containerized deployment

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-user/pulseplan.git
cd pulseplan/backend
```

### 2. Set up environment variables

Create a `.env` file from the provided template:

```bash
cp .env.template .env
```

Edit the `.env` file to configure secrets and DB URL.

### 3. Start the backend (Docker)

```bash
docker compose up --build
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

### 4. Test the API

Open the auto-generated Swagger UI:

```
http://localhost:8000/docs
```

---

## 🗂️ Project Structure

```
app/
├── main.py          # FastAPI entry point
├── models.py        # ORM and Pydantic models
├── database.py      # DB connection/session setup
├── routers/         # API routes (auth, tasks)
├── core/config.py   # Environment config
```

---

## 🔐 Authentication

Authentication is based on **JWT tokens**.  
To access protected routes, you must:

1. Register (`POST /register`)
2. Login (`POST /login`) to receive an access token
3. Use `Authorization: Bearer <token>` in requests

---

## 🧪 Development Tips

- Use [httpie](https://httpie.io/) or Postman for API testing
- To run without Docker:
  ```bash
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```

---

## 📌 Todo

- [ ] User and Task models
- [ ] Auth routes with JWT
- [ ] Task scheduling logic
- [ ] Push notifications (optional)

---

## 📄 License

MIT – feel free to use, modify, and contribute.
