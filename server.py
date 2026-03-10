"""
Prompteering MVP — Lean AI Prompt Analyzer
Built-in http.server + tiktoken + NLTK (no frameworks, no torch)
Run: python server.py → http://localhost:8000
"""

import json
import re
import mimetypes
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

import tiktoken
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag


# ── NLTK SETUP ─────────────────────────────────────────────────────
NLTK_DIR = Path(__file__).parent / ".nltk_data"
nltk.data.path.insert(0, str(NLTK_DIR))


def _ensure_nltk():
    """Auto-download required NLTK data on first run (~5MB)."""
    needed = {
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "taggers/averaged_perceptron_tagger_eng": "averaged_perceptron_tagger_eng",
    }
    for resource_path, pkg_name in needed.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            print(f"  ↓ Downloading NLTK: {pkg_name}...")
            nltk.download(pkg_name, download_dir=str(NLTK_DIR), quiet=True)


_ensure_nltk()


# ── TIKTOKEN ──────────────────────────────────────────────────────
ENC = {
    "o200k_base": tiktoken.get_encoding("o200k_base"),
    "cl100k_base": tiktoken.get_encoding("cl100k_base"),
}

STOP = set(stopwords.words("english"))


# ── MODEL CONFIGS (pricing per 1M tokens, USD) ───────────────────
MODELS = {
    "gpt-4o": {
        "label": "GPT-4o",
        "encoding": "o200k_base",
        "multiplier": 1.0,
        "input_cost": 2.50,
        "output_cost": 10.00,
        "context_window": 128_000,
    },
    "claude-sonnet-4": {
        "label": "Claude Sonnet 4",
        "encoding": "cl100k_base",
        "multiplier": 1.05,
        "input_cost": 3.00,
        "output_cost": 15.00,
        "context_window": 200_000,
    },
    "gemini-2.0-flash": {
        "label": "Gemini 2.0 Flash",
        "encoding": "cl100k_base",
        "multiplier": 0.95,
        "input_cost": 0.10,
        "output_cost": 0.40,
        "context_window": 1_000_000,
    },
}


# ── WEIGHT SCORING ───────────────────────────────────────────────
ACTION_VERBS = {
    "write", "create", "make", "build", "generate", "explain", "analyze",
    "describe", "list", "show", "give", "find", "help", "design", "code",
    "implement", "train", "develop", "compare", "summarize", "detail",
    "produce", "optimize", "debug", "refactor", "deploy", "test",
    "translate", "convert", "calculate", "evaluate", "plan", "fix",
    "configure", "setup", "install", "migrate", "integrate", "solve",
}

TECH_TERMS = {
    "python", "javascript", "typescript", "react", "vue", "angular",
    "api", "rest", "graphql", "neural", "network", "model", "data",
    "algorithm", "database", "function", "class", "pytorch", "tensorflow",
    "sql", "nosql", "html", "css", "json", "yaml", "xml",
    "llm", "gpt", "bert", "transformer", "vector", "embedding",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "server",
    "machine", "learning", "deep", "regression", "classification",
    "clustering", "backend", "frontend", "fullstack", "microservice",
    "token", "prompt", "inference", "training", "dataset", "feature",
    "component", "module", "package", "library", "framework",
}

QUALITY_MODIFIERS = {
    "step", "guide", "tutorial", "detailed", "complete", "full",
    "comprehensive", "advanced", "optimized", "efficient", "structured",
    "professional", "simple", "basic", "complex", "minimal", "robust",
    "scalable", "production", "enterprise", "beginner", "expert",
    "modern", "lightweight", "secure", "performant", "reliable",
}

POS_WEIGHTS = {
    "VB": 0.70, "VBP": 0.70, "VBZ": 0.70,
    "VBG": 0.65, "VBD": 0.65, "VBN": 0.60,
    "NN": 0.60, "NNS": 0.60,
    "NNP": 0.80, "NNPS": 0.80,
    "JJ": 0.55, "JJR": 0.55, "JJS": 0.55,
    "RB": 0.35, "RBR": 0.35, "RBS": 0.35,
    "CD": 0.45,
}


# ── INTENT PATTERNS ──────────────────────────────────────────────
INTENTS = [
    {"name": "Step-by-step Guide", "icon": "list-ordered", "patterns": [
        r"step.by.step", r"how to", r"\bguide\b", r"tutorial",
        r"procedure", r"walk.?through", r"instructions"]},
    {"name": "Code Generation", "icon": "code", "patterns": [
        r"\bcode\b", r"\bprogram\b", r"\bfunction\b", r"\bscript\b",
        r"\bimplement\b", r"\bbuild\b", r"\bdevelop\b",
        r"\bpython\b", r"\bjavascript\b", r"\bapi\b"]},
    {"name": "Creative Writing", "icon": "pen", "patterns": [
        r"\bwrite\b", r"\bstory\b", r"\bessay\b", r"\bblog\b",
        r"\barticle\b", r"\bpoem\b", r"\bnarrative\b", r"\bcreative\b"]},
    {"name": "Explanation / ELI5", "icon": "info", "patterns": [
        r"\bexplain\b", r"what is", r"\bdescribe\b", r"\bdefine\b",
        r"\bmeaning\b", r"\bunderstand\b", r"tell me about"]},
    {"name": "List / Enumeration", "icon": "list", "patterns": [
        r"\blist\b", r"\benumerate\b", r"examples of",
        r"top \d", r"best \d", r"give me.*example"]},
    {"name": "Analysis / Research", "icon": "chart", "patterns": [
        r"\banalyze\b", r"\banalyse\b", r"\bcompare\b", r"\bevaluate\b",
        r"\bassess\b", r"pros and cons", r"\bdifference\b", r"\bversus\b"]},
    {"name": "Q&A / Factual", "icon": "help", "patterns": [
        r"\bwho\b", r"\bwhat\b", r"\bwhen\b", r"\bwhere\b",
        r"\bwhy\b", r"how many", r"how much"]},
]


# ── FLOWCHART TEMPLATES ──────────────────────────────────────────
FLOWCHARTS = {
    "Step-by-step Guide": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Instruction Decode", "type": "step"},
        {"label": "Context Window Scan", "type": "step"},
        {"label": "RAG Retrieval", "type": "rag"},
        {"label": "Enumerate Steps", "type": "step"},
        {"label": "Draft Each Step Body", "type": "step"},
        {"label": "Conclusion Block", "type": "output"},
    ],
    "Code Generation": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Language Detection", "type": "step"},
        {"label": "Pattern Recall", "type": "step"},
        {"label": "RAG: Codebase Docs", "type": "rag"},
        {"label": "Core Logic Draft", "type": "step"},
        {"label": "Error Handling", "type": "step"},
        {"label": "Comments + Docs", "type": "step"},
        {"label": "Usage Example", "type": "output"},
    ],
    "Creative Writing": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Tone + Style Detect", "type": "step"},
        {"label": "Setting Build", "type": "step"},
        {"label": "Narrative Arc Plan", "type": "step"},
        {"label": "Draft Content", "type": "step"},
        {"label": "Polish + Voice Refine", "type": "output"},
    ],
    "Explanation / ELI5": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Concept Identification", "type": "step"},
        {"label": "RAG: Context Fetch", "type": "rag"},
        {"label": "Sub-concept Breakdown", "type": "step"},
        {"label": "Analogy Generation", "type": "step"},
        {"label": "Summary Block", "type": "output"},
    ],
    "Analysis / Research": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Scope Definition", "type": "step"},
        {"label": "RAG: Source Fetch", "type": "rag"},
        {"label": "Dimension Compare", "type": "step"},
        {"label": "Structure Findings", "type": "step"},
        {"label": "Verdict Block", "type": "output"},
    ],
    "List / Enumeration": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Category Detection", "type": "step"},
        {"label": "RAG: Item Retrieval", "type": "rag"},
        {"label": "Sort by Relevance", "type": "step"},
        {"label": "Format Each Item", "type": "step"},
        {"label": "Final List Output", "type": "output"},
    ],
    "Q&A / Factual": [
        {"label": "USER PROMPT", "type": "start"},
        {"label": "Intent Parse", "type": "intent"},
        {"label": "Question Parsing", "type": "step"},
        {"label": "RAG: Fact Fetch", "type": "rag"},
        {"label": "Answer Construction", "type": "step"},
        {"label": "Direct Response", "type": "output"},
    ],
}


# ═══════════════════════════════════════════════════════════════════
#  API LOGIC
# ═══════════════════════════════════════════════════════════════════

def handle_tokens(prompt: str) -> dict:
    """Count tokens for all models + cost estimates."""
    text = prompt.strip()
    if not text:
        return {}

    words = text.split()
    word_count, char_count = len(words), len(text)
    results = {}

    for mid, cfg in MODELS.items():
        enc = ENC[cfg["encoding"]]
        raw = len(enc.encode(text))
        pt = max(1, round(raw * cfg["multiplier"]))
        o_min = round(pt * 1.8)
        o_max = round(pt * 7.5)
        o_mid = (o_min + o_max) // 2

        results[mid] = {
            "label": cfg["label"],
            "promptTokens": pt,
            "wordCount": word_count,
            "charCount": char_count,
            "outputMin": o_min,
            "outputMax": o_max,
            "outputMid": o_mid,
            "total": pt + o_max,
            "cost": round((pt / 1e6) * cfg["input_cost"] + (o_mid / 1e6) * cfg["output_cost"], 6),
            "contextWindow": cfg["context_window"],
            "inputCostPer1M": cfg["input_cost"],
            "outputCostPer1M": cfg["output_cost"],
        }

    return results


def handle_weights(prompt: str) -> dict:
    """Score word importance via POS tagging + keyword dictionaries."""
    text = prompt.strip()
    if not text:
        return {"words": []}

    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    # Frequency map (non-stop words)
    freq = {}
    for tok in tokens:
        c = re.sub(r"[^a-z]", "", tok.lower())
        if c and c not in STOP:
            freq[c] = freq.get(c, 0) + 1
    max_freq = max(freq.values()) if freq else 1

    words = []
    for word, pos in tagged:
        clean = re.sub(r"[^a-zA-Z0-9]", "", word).lower()
        if not clean:
            words.append({"word": word, "score": 0.05})
            continue

        base = POS_WEIGHTS.get(pos, 0.15)

        if clean in STOP:
            base = 0.08
        else:
            if clean in ACTION_VERBS:
                base = max(base, 0.92)
            elif clean in TECH_TERMS:
                base = max(base, 0.85)
            elif clean in QUALITY_MODIFIERS:
                base = max(base, 0.72)
            f = freq.get(clean, 0) / max_freq
            base = min(1.0, base + f * 0.08)

        words.append({"word": word, "score": round(base, 3)})

    return {"words": words}


def handle_intent(prompt: str) -> dict:
    """Classify prompt intent via regex pattern matching."""
    text = prompt.strip().lower()
    results = []

    for i, intent in enumerate(INTENTS):
        matches = sum(1 for p in intent["patterns"] if re.search(p, text))
        n = len(intent["patterns"])
        if matches > 0:
            score = min(0.98, 0.45 + (matches / n) * 0.50)
        else:
            score = max(0.02, 0.12 - i * 0.014)

        results.append({
            "name": intent["name"],
            "score": round(score, 2),
            "icon": intent["icon"],
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"intents": results}


def handle_flowchart(prompt: str) -> dict:
    """Generate response roadmap based on top intent."""
    intent_data = handle_intent(prompt)
    top = intent_data["intents"][0]["name"]
    nodes = FLOWCHARTS.get(top, FLOWCHARTS["Q&A / Factual"])
    return {"intent": top, "nodes": nodes}


# ═══════════════════════════════════════════════════════════════════
#  HTTP SERVER
# ═══════════════════════════════════════════════════════════════════

BASE = Path(__file__).parent

API_ROUTES = {
    "/api/tokens": handle_tokens,
    "/api/weights": handle_weights,
    "/api/intent": handle_intent,
    "/api/flowchart": handle_flowchart,
}


class Handler(BaseHTTPRequestHandler):
    """Zero-framework request handler for Prompteering."""

    def do_GET(self):
        path = urlparse(self.path).path

        # Root → serve index.html
        if path in ("/", "/index.html"):
            self._serve_file(BASE / "public" / "index.html", "text/html")
            return

        # Static files
        if path.startswith("/static/"):
            file_path = BASE / "public" / path.lstrip("/")
            if file_path.is_file():
                content_type, _ = mimetypes.guess_type(str(file_path))
                self._serve_file(file_path, content_type or "application/octet-stream")
                return

        self._json_response(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        handler = API_ROUTES.get(path)

        if not handler:
            self._json_response(404, {"error": "Unknown endpoint"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            prompt = body.get("prompt", "")
            result = handler(prompt)
            self._json_response(200, result)
        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _serve_file(self, filepath: Path, content_type: str):
        try:
            data = filepath.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self._json_response(404, {"error": "File not found"})

    def _json_response(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Clean log format
        print(f"  {args[0]}")


# ── MAIN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8000

    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║  Prompteering MVP                        ║")
    print(f"  ║  http://{HOST}:{PORT}                    ║")
    print("  ║  Press Ctrl+C to stop                    ║")
    print("  ╚══════════════════════════════════════════╝")
    print()

    webbrowser.open(f"http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), Handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()
