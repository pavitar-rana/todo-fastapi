# 🚀 **todo-fastapi**

---

## 🎯 **Overview**
**Description:** An open-source project built with modern tooling to help developers get started quickly, featuring a robust ToDo API using FastAPI.

---

## ✨ **Features**
*   **CRUD Operations:** Create, Read, Update, and Delete ToDo items.
*   **Interactive API Documentation:** Automatically generated Swagger UI and ReDoc using OpenAPI.
*   **Asynchronous Endpoints:** Leverage Python's `async/await` for high performance.
*   **Data Validation:** Pydantic models for request and response data validation.
*   **Scalable Architecture:** Designed with FastAPI's performance and extensibility in mind.
*   **Docker Support:** (Potentially) Easy deployment with containerization.

---

## ⚡ **Installation**
Clone the repository and install dependencies:

```bash
git clone https://github.com/pavitar-rana/todo-fastapi.git
cd todo-fastapi

# 1. Create a Python virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt
# If you don't have a requirements.txt, you might need to install:
# pip install "fastapi[all]" uvicorn python-multipart
```

---

## 🔥 **Tech Stack**
This project uses modern Python tooling:

*   **Python:** The core programming language.
*   **FastAPI:** High-performance web framework for building APIs.
*   **Pydantic:** Data validation and settings management using Python type hints.
*   **Uvicorn:** Lightning-fast ASGI server for running FastAPI applications.
*   **(Optional/Future):** SQLAlchemy, Alembic (for database ORM and migrations), PostgreSQL/SQLite (for database).

---

## 🛠️ **Usage**
First, ensure your virtual environment is activated (see installation steps).

Run the project:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

You can access the interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Or ReDoc at:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Example usage with `curl`:

```bash
# Create a new todo item
curl -X POST "http://127.0.0.1:8000/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete the official tutorial"}'

# Get all todo items
curl -X GET "http://127.0.0.1:8000/todos/"

# Get a specific todo item by ID (e.g., ID 1)
curl -X GET "http://127.0.0.1:8000/todos/1"

# Update a todo item by ID (e.g., ID 1)
curl -X PUT "http://127.0.0.1:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Master FastAPI", "description": "Build a complete project", "completed": true}'

# Delete a todo item by ID (e.g., ID 1)
curl -X DELETE "http://127.00.1:8000/todos/1"
```

---

## 🤝 **Contributing**
1.  **Fork** the repo 🍴
2.  **Create** a new branch 🌱
3.  **Commit** your changes 💡
4.  **Push** to the branch 🚀
5.  **Open** a Pull Request 🎯

👉 See issues here: https://github.com/pavitar-rana/todo-fastapi/issues

---

## 📜 **License**
**MIT**

---

## 🔗 **Links**
*   🌐 **GitHub:** https://github.com/pavitar-rana/todo-fastapi
*   🏠 **Homepage:** Not provided