# FinHealth AI - SME Financial Intelligence Platform

FinHealth AI is an advanced, AI-powered financial health assessment platform which provides comprehensive analysis, cash flow forecasting, industry benchmarking, and personalized strategic recommendations in multiple languages for Small and Medium Enterprises (SMEs).

## 🚀 Key Features

*   **Multi-Language Support**: Complete interface and reporting in English, Hindi (हिंदी), and Tamil (தமிழ்).
*   **Financial Health Scoring**: Real-time assessment of business stability and creditworthiness.
*   **AI-Powered Insights**: Smart analysis of financial data using Large Language Models.
*   **Cash Flow Forecasting**: 12-month projections of revenue, net income, and cash flow.
*   **Industry Benchmarking**: Compare your performance against industry standards.
*   **Professional PDF Reporting**: Generate understandable, executive-ready reports for stakeholders.
*   **Tax & Compliance**: Estimated tax liabilities and GST compliance tracking.

## 🛠️ Technology Stack

### Frontend
*   **React.js**: Modern component-based UI.
*   **Framer Motion**: Smooth animations and transitions.
*   **Recharts**: Dynamic visualization of financial trends.
*   **Lucide React**: Premium iconography.
*   **CSS3**: Custom custom-designed responsive layouts with glassmorphism.

### Backend
*   **FastAPI**: High-performance Python web framework.
*   **OpenAI GPT-5.2**: Advanced financial reasoning and natural language processing.
*   **Neon**: PostgreSQL Database Server (For deployment).
*   **Pandas**: Robust data processing and metric calculation.

---

## 🏃 How to Run Locally

### Prerequisites
*   **Python 3.8+**
*   **Node.js 14+**
*   **OpenAI API Key**

### Step 1: Clone and Setup Backend
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venvname
    source venvname/bin/activate  # On Windows: venvname\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables:
    *   Create a `.env` file in the `backend` folder.
    *   Add your OpenAI API Key: `OPENAI_API_KEY=your_key_here`

### Step 2: Start the Backend Server
```bash
uvicorn main:app --reload --port 8000
```
The API will be available at `https://finhealthai.onrender.com`.

### Step 3: Setup and Start Frontend
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install packages:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```
The application will open automatically at `http://localhost:3000`.

---

## 📂 Project Structure

*   `backend/main.py`: Main API entry point.
*   `backend/services/`: Core logic for analysis, benchmarking, and forecasting.
*   `frontend/src/components/`: Modular UI components.
*   `frontend/src/translations.js`: Centralized internationalization system.

---
## 🏃 Check the live demo here

`https://financial-health-ai.netlify.app`


**Last Updated**: February 2026
