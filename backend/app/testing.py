from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Float, ForeignKey, Computed, PrimaryKeyConstraint






DATABASE_URL = "postgresql://ibrahim@localhost/college_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




## declare a table
from sqlalchemy import Column, Integer, String
class Test(Base):
    __tablename__ = "test"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Account(Base):
    __tablename__ = "account"
    x = Column(Integer, primary_key=True)
    total_fee = Column(Float)
    paid_salary = Column(Float)
    instt_income = Column(Float)
    instt_expense = Column(Float)
    total_income = Column(Float)
    total_expenses = Column(Float)

    # Automatically calculated by DB:
    account = Column(Float, Computed("total_income - total_expenses"))


## create declared tables
Base.metadata.create_all(bind=engine)

# ## get db
db = SessionLocal()
new_acc  = Account(total_fee=0, paid_salary=0, instt_income=0, instt_expense=0, total_income=200, total_expenses=100)
db.add(new_acc)
db.commit()
db.refresh(new_acc)


# # add entry
# n = "Khan"


# new_entry = Test(name=n)
# db.add(new_entry)
# db.commit()
# db.refresh(new_entry)



# # read entry
# all_entries = db.query(Test).all()
# print("Entries")
# for e in all_entries:
#     print(e.id, e.name)



# # update 
# db.query(Test).filter(Test.id==3).update(
#     {"name": "Ali"})
# db.commit()

# # read entry
# all_entries = db.query(Test).all()
# print("Entries")
# for e in all_entries:
#     print(e.id, e.name)



# # delete ali
# db.query(Test).filter(Test.name=="Ali").delete()
# db.commit()


# # read entry
# all_entries = db.query(Test).all()
# print("Entries")
# for e in all_entries:
#     print(e.id, e.name)