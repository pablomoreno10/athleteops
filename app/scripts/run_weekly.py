from app.db import SessionLocal
from app.services.weekly_summary import compute_weekly_summary, save_weekly_summary

def main():
    db = SessionLocal()
    try:
        user_id = 2
        summary = compute_weekly_summary(db, user_id=user_id)
        saved = save_weekly_summary(db, summary)
        print("COMPUTED:", summary)
        print("SAVED SUMMARY ID:", saved.id, "PERIOD:", saved.period_start, "->", saved.period_end)
    finally:
        db.close()

if __name__ == "__main__":
    main()
