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

# 4. 顯示「活動報名」頁面
@app.get("/register/{event_id}", response_class=HTMLResponse)
def register_form(request: Request, event_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, description, event_date, location, max_participants, status
        FROM events
        WHERE id = %s
        """,
        (event_id,)
    )
    event = cur.fetchone()
    cur.close()
    conn.close()
    return templates.TemplateResponse("register.html", {"request": request, "event": event})

# 5. 處理「送出報名」表單
@app.post("/register/{event_id}")
def submit_registration(
    event_id: int,
    name: str = Form(...),
    phone: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO registrations (event_id, name, phone)
        VALUES (%s, %s, %s)
        """,
        (event_id, name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url=f"/registrations/{event_id}", status_code=303)

# 6. 查看某活動的報名名單
@app.get("/registrations/{event_id}", response_class=HTMLResponse)
def registration_list(request: Request, event_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, description, event_date, location, max_participants, status
        FROM events
        WHERE id = %s
        """,
        (event_id,)
    )
    event = cur.fetchone()

    cur.execute(
        """
        SELECT id, event_id, name, phone
        FROM registrations
        WHERE event_id = %s
        ORDER BY id ASC
        """,
        (event_id,)
    )
    registrations = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "registrations.html",
        {
            "request": request,
            "event": event,
            "registrations": registrations
        }
    )