# Quick Start Guide -    Financial Health Platform

## Prerequisites Check
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ⚠️ PostgreSQL (optional - will use SQLite if not configured)

## Step-by-Step Setup

### 1. Backend Setup

#### A. Create `.env` file
```bash
cd backend
copy .env.example .env
```

#### B. Edit `backend/.env` with these values:

**REQUIRED CHANGES:**
```env
# Option 1: Use SQLite (easiest for testing)
DATABASE_URL=sqlite:///./  _finhealth.db

# Option 2: Use PostgreSQL (for production)
# DATABASE_URL=postgresql://username:password@localhost:5432/  _finhealth

# Generate SECRET_KEY (run in PowerShell):
# -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
SECRET_KEY=change-this-to-a-random-32-character-string

# Generate ENCRYPTION_KEY (must be exactly 32 characters):
ENCRYPTION_KEY=12345678901234567890123456789012

# OPTIONAL - OpenAI API Key (platform works without it using rule-based fallback)
OPENAI_API_KEY=

# Keep these as-is for development
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### C. Install Python dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### D. Start backend server
```bash
# Make sure you're in the backend directory with venv activated
uvicorn main:app --reload
```

**Backend should now be running on:** `http://localhost:8000`
**API docs available at:** `http://localhost:8000/docs`

---

### 2. Frontend Setup

#### A. Install dependencies
```bash
# Open a NEW terminal
cd frontend
npm install
```

#### B. Start frontend
```bash
npm start
```

**Frontend should now be running on:** `http://localhost:3000`

---

## Common Issues & Solutions

### Issue 1: "npm start" fails in backend directory
**Problem:** You ran `npm start` in the backend folder
**Solution:** Backend uses Python, not npm. Run `uvicorn main:app --reload` instead

### Issue 2: Database connection error
**Problem:** PostgreSQL not configured
**Solution:** Use SQLite instead:
```env
DATABASE_URL=sqlite:///./  _finhealth.db
```

### Issue 3: OpenAI API errors
**Problem:** No API key or invalid key
**Solution:** Leave `OPENAI_API_KEY` empty - the platform will use rule-based fallback automatically

### Issue 4: CORS errors
**Problem:** Frontend can't connect to backend
**Solution:** Ensure both servers are running and `ALLOWED_ORIGINS` includes `http://localhost:3000`

### Issue 5: Module not found errors
**Problem:** Dependencies not installed
**Solution:** 
- Backend: Activate venv and run `pip install -r requirements.txt`
- Frontend: Run `npm install`

---

## Testing the Application

### 1. Open browser to `http://localhost:3000`

### 2. Fill in Business Profile:
- Business Name: "Test Manufacturing Co"
- Business Type: Private Limited
- Industry: Manufacturing
- Size: Medium
- Click "Continue"

### 3. Enter Financial Data (or use pre-filled sample):
- Revenue: 10,000,000
- COGS: 6,000,000
- Operating Expenses: 2,000,000
- Net Income: 2,000,000
- Total Assets: 8,000,000
- Current Assets: 4,000,000
- Total Liabilities: 3,000,000
- Current Liabilities: 1,500,000
- Inventory: 1,000,000
- Receivables: 1,500,000
- Payables: 800,000
- Cash: 1,500,000

### 4. Click "Analyze Finances"

### 5. Explore the 6 dashboard tabs:
- Overview
- Detailed Metrics
- Cash Flow Forecast
- Industry Benchmarking
- Product Recommendations
- Tax & Compliance

---

## What You Can Customize

### 1. **OpenAI Integration** (Optional)
- Get API key from https://platform.openai.com/api-keys
- Add to `OPENAI_API_KEY` in `.env`
- Provides more contextual AI insights
- Costs: ~$5-20/month for moderate usage

### 2. **Database** (Optional for production)
- Install PostgreSQL
- Create database: `CREATE DATABASE   _finhealth;`
- Update `DATABASE_URL` in `.env`

### 3. **Security Keys** (REQUIRED for production)
- Generate strong `SECRET_KEY` (32+ characters)
- Generate `ENCRYPTION_KEY` (exactly 32 characters)
- Never commit these to version control

### 4. **Languages**
Currently supports:
- English (full)
- Hindi (full)
- Tamil (basic)
- Telugu (basic)

To add more languages, edit `backend/services/translation_service.py`

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Change `ENVIRONMENT=production` in `.env`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Generate strong random keys for `SECRET_KEY` and `ENCRYPTION_KEY`
- [ ] Set up HTTPS/TLS
- [ ] Configure proper CORS origins
- [ ] Set up database backups
- [ ] Enable audit logging
- [ ] Review rate limiting settings
- [ ] Conduct security audit

---

## Need Help?

1. **Backend not starting?**
   - Check Python version: `python --version` (need 3.9+)
   - Check if venv is activated (you should see `(venv)` in terminal)
   - Check for error messages in terminal

2. **Frontend not starting?**
   - Check Node version: `node --version` (need 16+)
   - Delete `node_modules` and `package-lock.json`, then run `npm install` again

3. **Analysis not working?**
   - Check backend is running on port 8000
   - Check browser console for errors (F12)
   - Verify `.env` file is configured correctly

---

**You're all set! 🚀**
