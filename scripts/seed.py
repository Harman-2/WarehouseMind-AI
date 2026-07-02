import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.database.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.warehouse import Worker, Robot, Inventory, Order
from app.rag.ingest import ingest_text

db_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "warehouse.db",
)
if os.path.exists(db_path) and os.getenv("KEEP_DB") != "1":
    os.remove(db_path)
    print("Existing database deleted for reset.")

Base.metadata.create_all(bind=engine)
print("Database tables created.")

db = SessionLocal()

if db.query(Worker).count() > 0:
    print("Database already seeded. Skipping.")
    db.close()
    sys.exit(0)

workers = [
    Worker(
        name="Alex",
        role="Picker",
        active=True,
        shift_start="08:00 AM",
        shift_end="04:00 PM",
        zone="Zone A (Picking)",
    ),
    Worker(
        name="Maria",
        role="Packer",
        active=True,
        shift_start="08:00 AM",
        shift_end="04:00 PM",
        zone="Zone B (Packing)",
    ),
    Worker(
        name="John",
        role="Forklift Driver",
        active=False,
        shift_start="06:00 AM",
        shift_end="02:00 PM",
        zone="Zone C (Loading)",
    ),
    Worker(
        name="Sarah",
        role="Receiver",
        active=True,
        shift_start="08:00 AM",
        shift_end="04:00 PM",
        zone="Zone C (Loading)",
    ),
]

robots = [
    Robot(name="Robot-101", status="Working", battery_level=85),
    Robot(name="Robot-102", status="Charging", battery_level=22),
    Robot(name="Robot-103", status="Maintenance", battery_level=5),
    Robot(name="Robot-104", status="Working", battery_level=98),
]

items = [
    Inventory(product_name="Laptop", quantity=100, threshold=20),
    Inventory(product_name="Keyboard", quantity=15, threshold=30),
    Inventory(product_name="Mouse", quantity=120, threshold=15),
    Inventory(product_name="Monitor", quantity=8, threshold=10),
]

orders = [
    Order(product="Laptop", priority="High", status="Processing"),
    Order(product="Keyboard", priority="Medium", status="Pending"),
]

users = [
    User(
        email="admin@warehousemind.ai",
        hashed_password=hash_password("admin123"),
        full_name="Warehouse Admin",
        role="admin",
    ),
    User(
        email="manager@warehousemind.ai",
        hashed_password=hash_password("manager123"),
        full_name="Shift Manager",
        role="manager",
    ),
]

db.add_all(workers)
db.add_all(robots)
db.add_all(items)
db.add_all(orders)
db.add_all(users)
db.commit()

ingest_text(
    db,
    title="Warehouse Safety Manual",
    doc_type="safety",
    filename="safety_manual.txt",
    content="""
    All forklift operators must complete a pre-shift safety inspection.
    Workers must wear high-visibility vests in active loading zones.
    Report spills, blocked aisles, or equipment faults immediately to the shift supervisor.
    Robots below 20 percent battery must be routed to charging before peak order windows.
    """,
)

ingest_text(
    db,
    title="Inventory Reorder Policy",
    doc_type="policy",
    filename="inventory_policy.txt",
    content="""
    Reorder any SKU when quantity falls below threshold for two consecutive checks.
    Critical items such as monitors and keyboards require same-day escalation to the inventory manager.
    High-priority orders must not be allocated from stock reserved below threshold.
    Restock requests above 200 units require manager approval.
    """,
)

print("Warehouse data, users, and knowledge base seeded")
print("Demo logins: admin@warehousemind.ai / admin123, manager@warehousemind.ai / manager123")

db.close()
