from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker

#Base Class Generated
Base = declarative_base()



class User(Base):
	__tablename__ = "Users"

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __repr__(self):
		return "<User(name="+self.name+")>"

class Project(Base):
	__tablename__ = "Projects"
	id = Column(Integer, primary_key=True)
	dateAddedUTC = Column(DateTime)
	projectOpen = Column(Boolean)
	projectHidden = Column(Boolean)

	shortName = Column(String)
	longName = Column(String)

class Task(Base):
	__tablename__ = "Tasks"
	id = Column(Integer, primary_key=True)
	parentProject = Column(Integer, ForeignKey('Projects.id'))
	dateAddedUTC = Column(DateTime)
	priority = Column(Integer)
	shortName = Column(String)
	createdBy = Column(Integer, ForeignKey('Users.id'))
	assignedTo = Column(Integer, ForeignKey('Users.id'))
	isCompleted = Column(Boolean)
	dateCompleted = Column(DateTime)


class DB():
	def __init__(self):
		self.engine = None
		self.Session = None
	def Ignition(self):
		engine = create_engine('sqlite:///tempdb.sql', echo=True)	
		Base.metadata.create_all(engine)  # Create all tables...
		self.Session = sessionmaker(bind=engine)
	def GetSession(self):
		return self.Session()

if __name__ == "__main__":
	print User.__table__

	one_user = User(name="one")
	print one_user
	#The engine
	db = DB()

	db.Ignition()


	ses = db.GetSession()

	ses.add(one_user)

	#ses.close()

	our_user = ses.query(User).filter_by(name="one").first() 

	print "is equal", one_user is our_user

