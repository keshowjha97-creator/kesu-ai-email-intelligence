# 🚀 Kesu AI Email Intelligence

**Your AI Chief of Staff for Gmail - Save 2+ Hours Daily**

Built with Bhindi AI assistance | Powered by GPT-4

---

## 🎯 What is Kesu AI?

Kesu AI is an intelligent email management system that automatically:
- ✅ Analyzes and classifies your Gmail inbox
- ✅ Extracts tasks, deadlines, and action items
- ✅ Exports daily reports to Google Sheets & Docs
- ✅ Syncs meetings to Google Calendar
- ✅ Sends priority email reminders
- ✅ Detects phishing and security threats

**Result:** Save 2+ hours daily on email management.

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** (Python 3.11+)
- **OpenAI GPT-4** for email analysis
- **Google Workspace APIs** (Gmail, Sheets, Docs, Calendar)
- **MongoDB** for data storage
- **Celery** for background tasks

### Frontend
- **Next.js 14** (React 18)
- **Tailwind CSS** for styling
- **Recharts** for analytics
- **NextAuth.js** for authentication

### Infrastructure
- **Vercel** (Frontend hosting)
- **Railway/Render** (Backend hosting)
- **MongoDB Atlas** (Database)
- **GitHub Actions** (CI/CD)

---

## 📦 Project Structure

```
kesu-ai-email-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── gmail.py          # Gmail API integration
│   │   │   ├── analysis.py       # GPT-4 email analysis
│   │   │   ├── sheets.py         # Google Sheets export
│   │   │   ├── calendar.py       # Calendar sync
│   │   │   └── reminders.py      # Notification system
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── email.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── gmail_service.py
│   │   │   ├── openai_service.py
│   │   │   └── google_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── calendar/
│   │   ├── analytics/
│   │   └── settings/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── next.config.js
├── docs/
│   ├── SETUP.md
│   ├── API.md
│   └── DEPLOYMENT.md
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB Atlas account
- Google Cloud project with APIs enabled
- OpenAI API key

### 1. Clone Repository
```bash
git clone https://github.com/keshowjha97-creator/kesu-ai-email-intelligence.git
cd kesu-ai-email-intelligence
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your API endpoints
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔑 Environment Variables

### Backend (.env)
```env
# Google Cloud
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# OpenAI
OPENAI_API_KEY=your_openai_key

# MongoDB
MONGODB_URI=your_mongodb_connection_string

# App Config
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your_nextauth_secret
NEXTAUTH_URL=http://localhost:3000
```

---

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [API Documentation](docs/API.md) - API endpoints and usage
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

---

## 🎯 Features

### ✅ Phase 1 (Current)
- [x] Gmail OAuth integration
- [x] Email fetching and parsing
- [x] GPT-4 classification
- [x] Basic dashboard

### 🚧 Phase 2 (In Progress)
- [ ] Google Sheets export
- [ ] Google Docs reports
- [ ] Calendar sync
- [ ] Priority reminders

### 📋 Phase 3 (Planned)
- [ ] Mobile app
- [ ] Team collaboration
- [ ] Advanced analytics
- [ ] API access

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1 Gmail account, 50 emails/day |
| Pro | $5/month | 3 accounts, unlimited emails, full features |
| Team | $20/month | 10 accounts, shared dashboard |
| Enterprise | Custom | Unlimited, white-label, API access |

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👨‍💻 Built By

**Keshow Jha**  
AI Engineer & Founder  
🔗 [LinkedIn](https://www.linkedin.com/in/keshow-jha-a71b41370)

**Built with Bhindi AI assistance**  
🌐 [bhindi.io](https://bhindi.io)

---

## 📞 Support

- Email: keshowjha97@gmail.com
- Issues: [GitHub Issues](https://github.com/keshowjha97-creator/kesu-ai-email-intelligence/issues)

---

**⭐ Star this repo if you find it useful!**
