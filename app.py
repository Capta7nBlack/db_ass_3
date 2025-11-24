import uvicorn
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text

# 1. Database Connection (Cloud or Local)
url = "postgresql://caregivers_db_7dm8_user:pKjPqCvuTRFyjTPDEc9noF94yNRb7ZmD@dpg-d4i4i5buibrs73dvgfp0-a/caregivers_db_7dm8"
engine = create_engine(url)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 2. Main Page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with engine.connect() as conn:
        users = conn.execute(text('SELECT * FROM "USER" ORDER BY user_id')).mappings().all()
        caregivers = conn.execute(text('SELECT * FROM CAREGIVER ORDER BY caregiver_user_id')).mappings().all()
        members = conn.execute(text('SELECT * FROM MEMBER ORDER BY member_user_id')).mappings().all()
        addresses = conn.execute(text('SELECT * FROM ADDRESS ORDER BY member_user_id')).mappings().all()
        jobs = conn.execute(text('SELECT * FROM JOB ORDER BY job_id')).mappings().all()
        apps = conn.execute(text('SELECT * FROM JOB_APPLICATION ORDER BY date_applied DESC')).mappings().all()
        appts = conn.execute(text('SELECT * FROM APPOINTMENT ORDER BY appointment_id')).mappings().all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users, "caregivers": caregivers, "members": members,
        "addresses": addresses, "jobs": jobs, "apps": apps, "appts": appts
    })

# 3. CRUD Operations
@app.post("/user/create")
async def create_user(
    email: str = Form(...), given_name: str = Form(...), surname: str = Form(...), 
    city: str = Form(""), phone_number: str = Form(""), profile_description: str = Form(""), 
    password: str = Form(...)
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) 
            VALUES (:e, :n, :s, :c, :ph, :d, :p)
        """), {"e": email, "n": given_name, "s": surname, "c": city, "ph": phone_number, "d": profile_description, "p": password})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/user/update_any")
async def update_user_any(uid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["email", "given_name", "surname", "city", "phone_number", "profile_description", "password"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE "USER" SET {field_name} = :v WHERE user_id = :id'), {"v": new_value, "id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/user/delete/{user_id}")
async def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM "USER" WHERE user_id = :id'), {"id": user_id})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/caregiver/create")
async def create_cg(
    uid: int = Form(...), type: str = Form(...), rate: float = Form(...),
    photo: str = Form(""), gender: str = Form("")
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO CAREGIVER (caregiver_user_id, caregiving_type, hourly_rate, photo, gender) 
            VALUES (:id, :t, :r, :p, :g)
        """), {"id": uid, "t": type, "r": rate, "p": photo, "g": gender})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/caregiver/update_any")
async def update_cg_any(uid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["caregiving_type", "hourly_rate", "photo", "gender"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE CAREGIVER SET {field_name} = :v WHERE caregiver_user_id = :id'), {"v": new_value, "id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/caregiver/delete/{uid}")
async def delete_cg(uid: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM CAREGIVER WHERE caregiver_user_id = :id'), {"id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/member/create")
async def create_mem(uid: int = Form(...), rules: str = Form(...), desc: str = Form("")):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) 
            VALUES (:id, :r, :d)
        """), {"id": uid, "r": rules, "d": desc})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/member/update_any")
async def update_mem_any(uid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["house_rules", "dependent_description"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE MEMBER SET {field_name} = :v WHERE member_user_id = :id'), {"v": new_value, "id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/member/delete/{uid}")
async def delete_mem(uid: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM MEMBER WHERE member_user_id = :id'), {"id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/address/create")
async def create_addr(uid: int = Form(...), town: str = Form(...), street: str = Form(...), num: str = Form(...)):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO ADDRESS (member_user_id, town, street, house_number) 
            VALUES (:id, :t, :s, :n)
        """), {"id": uid, "t": town, "s": street, "n": num})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/address/update_any")
async def update_addr_any(uid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["town", "street", "house_number"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE ADDRESS SET {field_name} = :v WHERE member_user_id = :id'), {"v": new_value, "id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/address/delete/{uid}")
async def delete_addr(uid: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM ADDRESS WHERE member_user_id = :id'), {"id": uid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/job/create")
async def create_job(mid: int = Form(...), type: str = Form(...), req: str = Form(...)):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements) 
            VALUES (:m, :t, :r)
        """), {"m": mid, "t": type, "r": req})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/job/update_any")
async def update_job_any(jid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["required_caregiving_type", "other_requirements", "date_posted"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE JOB SET {field_name} = :v WHERE job_id = :id'), {"v": new_value, "id": jid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/job/delete/{jid}")
async def delete_job(jid: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM JOB WHERE job_id = :id'), {"id": jid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/app/create")
async def create_app(jid: int = Form(...), cid: int = Form(...)):
    with engine.connect() as conn:
        conn.execute(text('INSERT INTO JOB_APPLICATION (job_id, caregiver_user_id) VALUES (:j, :c)'),
                     {"j": jid, "c": cid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/app/update_any")
async def update_app_any(jid: int = Form(...), cid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["date_applied"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE JOB_APPLICATION SET {field_name} = :v WHERE job_id = :j AND caregiver_user_id = :c'),
                     {"v": new_value, "j": jid, "c": cid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/app/delete")
async def delete_app(jid: int = Form(...), cid: int = Form(...)):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM JOB_APPLICATION WHERE job_id = :j AND caregiver_user_id = :c'),
                     {"j": jid, "c": cid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/appt/create")
async def create_appt(
    cid: int = Form(...), mid: int = Form(...), date: str = Form(...), 
    time: str = Form(...), hours: int = Form(...)
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours) 
            VALUES (:c, :m, :d, :t, :h)
        """), {"c": cid, "m": mid, "d": date, "t": time, "h": hours})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/appt/update_any")
async def update_appt_any(aid: int = Form(...), field_name: str = Form(...), new_value: str = Form(...)):
    if field_name not in ["appointment_date", "appointment_time", "work_hours", "status"]:
        return RedirectResponse("/", status_code=303)
    with engine.connect() as conn:
        conn.execute(text(f'UPDATE APPOINTMENT SET {field_name} = :v WHERE appointment_id = :id'), 
                     {"v": new_value, "id": aid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/appt/delete/{aid}")
async def delete_appt(aid: int):
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM APPOINTMENT WHERE appointment_id = :id'), {"id": aid})
        conn.commit()
    return RedirectResponse("/", status_code=303)

# 4. Server Start Logic
if __name__ == "__main__":

    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
