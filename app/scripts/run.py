from app.services.weekly_summary import compute_weekly_summary
from app.db import SessionLocal

def main():
    db = SessionLocal()
    try:
        summary = compute_weekly_summary(db, user_id = 2)
        print(summary)
    finally:
      db.close()

if __name__ == '__main__':
   main()
