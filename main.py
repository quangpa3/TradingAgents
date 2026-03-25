import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

app = FastAPI(title="TradingAgents API")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "trading123")

class AnalyzeRequest(BaseModel):
    ticker: str
    date: str
    llm_provider: str = "openai"
    deep_think_llm: str = "gpt-4o"
    quick_think_llm: str = "gpt-4o-mini"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradingAgents - Phan Tich Co Phieu</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .container { background: white; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); max-width: 600px; width: 100%; overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .content { padding: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; }
        .form-group input, .form-group select { width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 16px; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #667eea; }
        .btn { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; }
        .btn:disabled { opacity: 0.6; }
        .result { margin-top: 25px; padding: 20px; background: #f9fafb; border-radius: 12px; display: none; }
        .result.show { display: block; }
        .result-content { white-space: pre-wrap; font-size: 14px; }
        .loading { text-align: center; padding: 20px; display: none; }
        .loading.show { display: block; }
        .spinner { width: 40px; height: 40px; border: 4px solid #e5e7eb; border-top-color: #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>TradingAgents</h1>
            <p>AI-powered Stock Analysis</p>
        </div>
        <div class="content">
            <form id="analyzeForm">
                <div class="form-group">
                    <label>Ma Co Phieu (Ticker)</label>
                    <input type="text" id="ticker" placeholder="VD: AAPL, NVDA, MSFT" required>
                </div>
                <div class="form-group">
                    <label>Ngay Phan Tich</label>
                    <input type="date" id="date" required>
                </div>
                <div class="form-group">
                    <label>LLM Provider</label>
                    <select id="llm_provider">
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic (Claude)</option>
                        <option value="google">Google (Gemini)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Deep Think Model</label>
                    <select id="deep_think_llm">
                        <option value="gpt-4o">GPT-4o</option>
                        <option value="gpt-4o-mini">GPT-4o-mini</option>
                        <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                        <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                    </select>
                </div>
                <button type="submit" class="btn" id="submitBtn">Phan Tich</button>
            </form>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Dang phan tich...</p>
            </div>
            <div class="result" id="result">
                <h3>Ket Qua Phan Tich</h3>
                <div class="result-content" id="resultContent"></div>
            </div>
        </div>
    </div>
    <script>
        document.getElementById('date').valueAsDate = new Date();
        document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            btn.disabled = true;
            loading.classList.add('show');
            result.classList.remove('show');
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        ticker: document.getElementById('ticker').value.toUpperCase(),
                        date: document.getElementById('date').value,
                        llm_provider: document.getElementById('llm_provider').value,
                        deep_think_llm: document.getElementById('deep_think_llm').value,
                        quick_think_llm: document.getElementById('deep_think_llm').value.replace('-mini', '') + '-mini'
                    })
                });
                const data = await response.json();
                resultContent.textContent = JSON.stringify(data, null, 2);
                result.classList.add('show');
            } catch (error) {
                resultContent.textContent = 'Loi: ' + error.message;
                result.classList.add('show');
            } finally {
                btn.disabled = false;
                loading.classList.remove('show');
            }
        });
    </script>
</body>
</html>'''

LOGIN_HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dang Nhap - TradingAgents</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .login-box { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); width: 100%; max-width: 400px; }
        h1 { text-align: center; color: #1a1a2e; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; }
        .form-group input { width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 16px; }
        .btn { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; }
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; display: none; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>TradingAgents</h1>
        <p class="error" id="error">Sai thong tin dang nhap</p>
        <form id="loginForm">
            <div class="form-group">
                <label>Ten dang nhap</label>
                <input type="text" id="username" required>
            </div>
            <div class="form-group">
                <label>Mat khau</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn">Dang nhap</button>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const response = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                })
            });
            if (response.ok) { window.location.href = '/'; }
            else { document.getElementById('error').style.display = 'block'; }
        });
    </script>
</body>
</html>'''

sessions = {}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return HTMLResponse(LOGIN_HTML)
    return HTMLResponse(HTML_TEMPLATE)

@app.post("/login")
async def login(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        import uuid
        session_id = str(uuid.uuid4())
        sessions[session_id] = username
        from fastapi.responses import JSONResponse
        response = JSONResponse({"status": "ok"})
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        return response
    return JSONResponse({"error": "Invalid credentials"}, status_code=401)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: Request, analyze_request: AnalyzeRequest):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = analyze_request.llm_provider
        config["deep_think_llm"] = analyze_request.deep_think_llm
        config["quick_think_llm"] = analyze_request.quick_think_llm

        ta = TradingAgentsGraph(debug=False, config=config)
        _, decision = ta.propagate(analyze_request.ticker, analyze_request.date)
        return {"ticker": analyze_request.ticker, "date": analyze_request.date, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
