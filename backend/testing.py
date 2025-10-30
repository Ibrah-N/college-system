from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


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



## create declared tables
Base.metadata.create_all(bind=engine)


## get db
db = SessionLocal()



# add entry
n = "Khan"

new_entry = Test(name=n)
db.add(new_entry)
db.commit()
db.refresh(new_entry)



# read entry
all_entries = db.query(Test).all()
print("Entries")
for e in all_entries:
    print(e.id, e.name)



# update 
db.query(Test).filter(Test.id==3).update(
    {"name": "Ali"})
db.commit()

# read entry
all_entries = db.query(Test).all()
print("Entries")
for e in all_entries:
    print(e.id, e.name)



# delete ali
db.query(Test).filter(Test.name=="Ali").delete()
db.commit()


# read entry
all_entries = db.query(Test).all()
print("Entries")
for e in all_entries:
    print(e.id, e.name)