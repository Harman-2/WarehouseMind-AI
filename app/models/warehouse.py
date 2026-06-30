from sqlalchemy import Column, Integer, String, Boolean


from app.database.database import Base


class Worker(Base):

    __tablename__ = "workers"


    id = Column(Integer, primary_key=True)

    name = Column(String)

    role = Column(String)

    active = Column(Boolean, default=True)



class Robot(Base):

    __tablename__ = "robots"


    id = Column(Integer, primary_key=True)

    name = Column(String)

    status = Column(String)



class Inventory(Base):

    __tablename__ = "inventory"


    id = Column(Integer, primary_key=True)

    product_name = Column(String)

    quantity = Column(Integer)

    threshold = Column(Integer)



class Order(Base):

    __tablename__ = "orders"


    id = Column(Integer, primary_key=True)

    product = Column(String)

    priority = Column(String)

    status = Column(String)