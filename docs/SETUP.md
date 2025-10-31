# 🚀 Kesu AI Setup Guide

Complete step-by-step instructions to get Kesu AI Email Intelligence running.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Git** installed
- **Google Account** (for Gmail API)
- **OpenAI API Key** (get from platform.openai.com)
- **MongoDB Atlas Account** (free tier available)

---

## 🔧 Part 1: Google Cloud Setup (10 minutes)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Name it "Kesu AI" → Click "Create"
4. Wait for project creation (30 seconds)

### Step 2: Enable Required APIs

1. In the search bar, type "Gmail API" → Click it
2. Click "Enable" button
3. Repeat for:
   - Google Sheets API
   - Google Docs API
   - Google Calendar API

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: Kesu AI
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue" through all steps
4. Back to "Create OAuth client ID":
   - Application type: Web application
   - Name: Kesu AI Backend
   - Authorized redirect URIs: `http://localhost:8000/auth/google/callback`
   - Click "Create"
5. **SAVE YOUR CLIENT ID AND CLIENT SECRET** - you'll need these!

### Step 4: Add Test Users (Important!)

1. Go to "OAuth consent screen"
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your Gmail address
5. Click "Save"

---

## 💾 Part 2: MongoDB Setup (5 minutes)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up / Log in
3. Create a free cluster:
   - Choose "Shared" (Free)
   - Select region closest to you
   - Click "Create Cluster"
4. Create database user:
   - Security → Database Access
   - Add New Database User
   - Username: kesuai
   - Password: (generate strong password)
   - **SAVE THIS PASSWORD!**
5. Whitelist your IP:
   - Security → Network Access
   - Add IP Address → "Allow Access from Anywhere" (0.0.0.0/0)
6. Get connection string:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password

---

## 🔑 Part 3: OpenAI API Key (2 minutes)

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up / Log in
3. Go to API Keys section
4. Click "Create new secret key"
5. Name it "Kesu AI"
6. **COPY AND SAVE THE KEY** (you can't see it again!)

---

## 💻 Part 4: Backend Setup

### Clone Repository

```bash
git clone https://github.com/keshowjha97-creator/kesu-ai-email-intelligence.git
cd kesu-ai-email-intelligence
```

### Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Configure .env File

Open `backend/.env` and fill in:

```env
# Google Cloud (from Step 3)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# OpenAI (from Part 3)
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# MongoDB (from Part 2)
MONGODB_URI=your_mongodb_connection_string_here
MONGODB_DB_NAME=kesu_ai

# Generate a random secret key
SECRET_KEY=your_super_secret_key_change_this_in_production

# Keep these as is for development
ENVIRONMENT=development
DEBUG=True
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Visit http://localhost:8000/docs to see API documentation!

---

## 🎨 Part 5: Frontend Setup

Open a **new terminal** (keep backend running):

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
```

### Configure .env.local

Open `frontend/.env.local` and fill in:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=generate_random_string_here
NEXTAUTH_URL=http://localhost:3000

# Same Google credentials as backend
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### Run Frontend

```bash
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000
```

Visit http://localhost:3000 to see your app!

---

## ✅ Part 6: Test the Application

1. Open http://localhost:3000
2. Click "Sign in with Google"
3. Authorize Kesu AI to access your Gmail
4. You should see your dashboard!

---

## 🎯 Next Steps

Now that it's running:

1. **Test Email Fetching**: Check if emails are being fetched
2. **Test Analysis**: Verify GPT-4 is analyzing emails
3. **Test Sheets Export**: Create a Google Sheet and test export
4. **Test Calendar Sync**: Check if meetings are being added

---

## 🐛 Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added yourself as a test user in Google Cloud Console
- Check that redirect URI matches exactly

### "OpenAI API Error"
- Verify your API key is correct
- Check you have credits in your OpenAI account

### "MongoDB Connection Error"
- Verify connection string is correct
- Check password doesn't have special characters (or URL encode them)
- Ensure IP whitelist includes your IP

### "Module not found" errors
- Make sure you ran `pip install -r requirements.txt`
- Verify virtual environment is activated

---

## 📞 Need Help?

- Email: keshowjha97@gmail.com
- GitHub Issues: [Create an issue](https://github.com/keshowjha97-creator/kesu-ai-email-intelligence/issues)

---

**🎉 Congratulations! Your Kesu AI Email Intelligence is now running!**
