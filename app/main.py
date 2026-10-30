from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import get_connection

app = FastAPI(title="廢墟版活動報名平台")
templates = Jinja2Templates(directory="app/templates")

# 1. 首頁：列出所有活動
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, event_date, location, max_participants, status FROM events ORDER BY event_date ASC")
    events = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "events": events})

# 2. 顯示「新增活動」頁面
@app.get("/add-event", response_class=HTMLResponse)
def add_event_form(request: Request):
    return templates.TemplateResponse("add_event.html", {"request": request})

# 3. 處理「新增活動」表單送出
@app.post("/add-event")
def add_event(
    title: str = Form(...),
    description: str = Form(""),
    event_date: str = Form(...),
    location: str = Form("線上"),
    max_participants: int = Form(50)
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (title, description, event_date, location, max_participants)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (title, description, event_date, location, max_participants)
    )
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)