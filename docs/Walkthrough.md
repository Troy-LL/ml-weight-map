# Prompteering MVP — Walkthrough

## What Was Built

A **local AI prompt analyzer** that accepts any prompt and visually reports on NLP statistics and API pricing.

| Panel | Purpose | Tech |
|---|---|---|
| **Word Weight Map** | Color-coded word importance scores | NLTK POS tagging + keyword dictionaries |
| **Token Calculator** | Token counts + API cost for 3 models | tiktoken (exact GPT) + calibrated estimates |
| **Intent Classifier** | Predicts response type with confidence bars | Regex pattern engine |
| **Response Roadmap** | Flowchart of predicted processing steps | Template-based on top intent |

## How to Run

There are two primary ways to start the application:

```bash
# Option 1: Double-click the one-click launcher shell script
start.bat

# Option 2: Manual execution via the terminal
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python server.py

# → The server spins up at http://localhost:8000 and the browser automatically opens to this tab.
```

## Project Architecture & Structure

```text
├── server.py              # Zero-framework backend API using built-in `http.server`
├── requirements.txt       # The only two Python dependencies: `tiktoken` + `nltk`
├── start.bat              # One-click launcher wrapper script
├── templates/
│   └── index.html         # Main UI Interface
├── static/
│   ├── css/style.css      # Dark theme UI Styling + Component designs
│   └── js/app.js          # Main client controller + DOM manipulation + API communication
└── prompteering.html      # Original conceptual prototype (reference)
```

## Multi-Model Context Engine 

Switching between models allows you to instantly see how their prices scale against the length of your prompt. 

All this data is fetched locally instantly because all 3 variations are compiled into the payload under the `/api/tokens` endpoint!

| Model Profile | Tokenizer Approach | Model Accuracy | Max Context Limits |
|---|---|---|---|
| GPT-4o | tiktoken `o200k_base` | Exact 1:1 Match | 128k |
| Claude Sonnet 3.5/4 | tiktoken proxy × 1.05 modifier | ~95% Margin | 200k |
| Gemini 2.0 Flash | tiktoken proxy × 0.95 modifier | ~90% Margin | 1M Context Window |

---

*This lean MVP tool provides a zero-framework (no FastAPI, no massive Torch/DistilBERT footprints) interface for rapid prompt inspection, now fully compatible with **Netlify Functions** for cloud deployment.*

---

## 🚀 Netlify Deployment

This project is configured for one-click deployment to Netlify.

1.  **Connect to GitHub**: Push your code to a GitHub repository.
2.  **Configure Netlify**: 
    - **Build Command**: (Leave empty)
    - **Publish Directory**: `.` (Root)
    - **Functions Directory**: `netlify/functions` (Auto-detected via `netlify.toml`)
3.  **Deploy**: Netlify will automatically build the site and deploy the API as serverless functions.

The `netlify.toml` file handles the routing from `/api/*` to the serverless function.

