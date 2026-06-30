import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from app.database.database import SessionLocal

from app.models.warehouse import (
    Worker,
    Robot,
    Inventory,
    Order
)



db = SessionLocal()



workers = [

    Worker(
        name="Alex",
        role="Picker",
        active=True
    ),

    Worker(
        name="Maria",
        role="Packer",
        active=True
    )

]



robots = [

    Robot(
        name="Robot-101",
        status="Working"
    ),

    Robot(
        name="Robot-102",
        status="Charging"
    )

]



items = [

    Inventory(
        product_name="Laptop",
        quantity=100,
        threshold=20
    ),

    Inventory(
        product_name="Keyboard",
        quantity=15,
        threshold=30
    )

]



orders = [

    Order(
        product="Laptop",
        priority="High",
        status="Processing"
    )

]



db.add_all(workers)

db.add_all(robots)

db.add_all(items)

db.add_all(orders)



db.commit()


print("Warehouse data inserted")