# Cup_Streaming
# FastAPI Project with GitHub Actions CI/CD

This repository contains a **FastAPI project** integrated with **GitHub Actions** for CI/CD.

---

## 🚀 CI/CD Pipeline

- The project uses **GitHub Actions** workflows located in `.github/workflows/`.
- On every push to the **main** branch:
  - The pipeline prepares a clean package of the app.
  - Excludes unnecessary files (e.g., `.git`, `.venv`, `__pycache__`, logs, etc.).
  - Uploads the clean package as an **artifact** (`prod-drop`).

---

## ▶️ How to Trigger Pipeline

- Make any change in the repo (for example edit this README file) and push it to the **main branch**:

```bash
git add .
git commit -m "Trigger pipeline"
git push origin main
