# 🤖 AI Interview System

An AI-driven interactive interview platform built with **Streamlit**, **Gemini AI**, and **SQLite**.  
It asks adaptive questions, evaluates responses, records transcriptions, and provides admin reporting.

---

## ✅ Features

✅ Dynamic question generation based on role & experience  
✅ Voice & typed answers supported  
✅ AI-based evaluation & follow-up questions  
✅ Real-time scoring  
✅ Admin dashboard  
✅ Local database storage (SQLite)  
✅ Streamlit UI  
✅ Secure secret key handling  

---

## 📦 Tech Stack

| Component | Tech |
|----------|------|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Google Gemini |
| DB | SQLite |
| Authentication | Admin login |
| Speech Input | streamlit-mic-recorder |

---

## 🚀 Run Locally

### 1️⃣ Clone repository

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

shell
Copy code

### 2️⃣ Create Virtual Env

python -m venv .venv
source .venv/bin/activate # Mac/Linux
.venv\Scripts\activate # Windows

shell
Copy code

### 3️⃣ Install Dependencies

pip install -r requirements.txt

makefile
Copy code

### 4️⃣ Add `.env` file

Create:

GEMINI_API_KEY=YOUR_KEY
ADMIN_USER=admin
ADMIN_PASS=admin123

shell
Copy code

### 5️⃣ Run

streamlit run app.py

yaml
Copy code

---

## 🔐 Environment Variables

| Key | Required | Description |
|-----|----------|-------------|
| GEMINI_API_KEY | ✅ | Gemini AI API Key |
| ADMIN_USER | ✅ | Admin login |
| ADMIN_PASS | ✅ | Admin password |

---

## 🗄️ Local Database

SQLite DB is auto-created at:

instance/interview.db

yaml
Copy code

---

# 🌐 Deploying on Streamlit Cloud

### ✅ Step-by-step

1️⃣ Push to GitHub  
2️⃣ Go to: https://share.streamlit.io  
3️⃣ Click "New app" → choose your repo  
4️⃣ In **Advanced Settings → Secrets**, paste:

GEMINI_API_KEY="YOUR_KEY"
ADMIN_USER="admin"
ADMIN_PASS="admin123"

yaml
Copy code

✅ Deploy → done 🎉

---

## ✅ Folder Structure

📂 project
│── app.py
│── config.py
│── requirements.txt
│── README.md
│── .gitignore
│── utils/
│ ├── db_ops.py
│ ├── ai_utils.py
│── instance/
│ └── interview.db (AUTO-CREATED)
│── .env (NOT INCLUDED IN GIT)

yaml
Copy code

---

## ✅ Security

❌ DO NOT commit `.env`  
✅ Use Streamlit Secrets for deployment  

---

## ✨ Future Enhancements

✅ Result PDF export  
✅ Email notifications  
✅ ML-based scoring model  
✅ Multi-language support  

---

## ✅ Credits

Built with ❤️ using  
**Streamlit + Gemini + SQLite**

---
