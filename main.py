import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

app = FastAPI(title="TradingAgents API")

class AnalyzeRequest(BaseModel):
    ticker: str
    date: str
    llm_provider: str = "gpt-5"
    deep_think_llm: str = "gpt-5"
    quick_think_llm: str = "gpt-5-mini"

@app.get("/")
def root():
    return {"message": "TradingAgents API", "endpoints": ["/health", "/analyze"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = request.llm_provider
        config["deep_think_llm"] = request.deep_think_llm
        config["quick_think_llm"] = request.quick_think_llm

        ta = TradingAgentsGraph(debug=False, config=config)
        _, decision = ta.propagate(request.ticker, request.date)
        return {"ticker": request.ticker, "date": request.date, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
