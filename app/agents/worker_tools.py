from app.database.database import SessionLocal
from app.models.warehouse import Worker

def check_worker_status():
    db = SessionLocal()
    workers = db.query(Worker).all()
    result = []

    for worker in workers:
        result.append({
            "name": worker.name,
            "role": worker.role,
            "status": "Active" if worker.active else "Inactive",
            "shift_start": worker.shift_start,
            "shift_end": worker.shift_end,
            "zone": worker.zone            
        })

    db.close()
    return result