"""High School Management System API with SQLite persistence

This updates the simple example to use SQLModel + SQLite for persistence.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import os

from sqlmodel import select

from . import db
from .models import Activity, Student, ActivityStudent


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent, "static")), name="static")


@app.on_event("startup")
def on_startup():
    db.init_db()
    # Seed default activities if none exist
    with db.get_session() as session:
        count = session.exec(select(Activity)).first()
        if not session.exec(select(Activity)).first():
            seed = [
                Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
                Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
                Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
            ]
            session.add_all(seed)
            session.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(session: db.Session = Depends(db.get_session)):
    activities = session.exec(select(Activity)).all()
    result = {}
    for a in activities:
        participants = [s.email for s in a.participants]
        result[a.name] = {
            "description": a.description,
            "schedule": a.schedule,
            "max_participants": a.max_participants,
            "participants": participants,
        }
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, session: db.Session = Depends(db.get_session)):
    activity = session.get(Activity, activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check existing participants count
    if len(activity.participants) >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Ensure student exists
    student = session.get(Student, email)
    if not student:
        student = Student(email=email)
        session.add(student)
        session.commit()
        session.refresh(student)

    # Check already registered
    link = session.exec(select(ActivityStudent).where(ActivityStudent.activity_name == activity_name, ActivityStudent.student_email == email)).first()
    if link:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    assoc = ActivityStudent(activity_name=activity_name, student_email=email)
    session.add(assoc)
    session.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, session: db.Session = Depends(db.get_session)):
    activity = session.get(Activity, activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    link = session.exec(select(ActivityStudent).where(ActivityStudent.activity_name == activity_name, ActivityStudent.student_email == email)).first()
    if not link:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    session.delete(link)
    session.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}

