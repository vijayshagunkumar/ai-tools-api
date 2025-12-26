from fastapi import FastAPI
from typing import List, Dict
import json
import os

app = FastAPI(title="AI Tools API", version="1.0")

DATA_FILE = os.path.join("data", "tools.json")


def load_tools() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def root():
    return {"status": "AI Tools API running"}


@app.get("/api/tools")
def get_tools():
    return load_tools()


@app.get("/api/tools/top")
def get_top(limit: int = 5):
    tools = load_tools()
    tools = sorted(tools, key=lambda x: x.get("score", 0), reverse=True)
    return tools[:limit]


@app.get("/api/tools/search")
def search_tools(q: str):
    tools = load_tools()
    q = q.lower()
    return [t for t in tools if q in t["name"].lower()]
