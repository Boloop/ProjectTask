from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

#Base Class Generated
Base = declarative_base()



class User(Base):
	__tablename__ = "Users"

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __repr__(self):
		return "<User(name="+self.name+")>"

if __name__ == "__main__":
	print User.__table__

	one_user = User(name="one")
	print one_user
	#The engine
	engine = create_engine('sqlite:///:memory:', echo=True)
	Base.metadata.create_all(engine)  # Create all tables...
	Session = sessionmaker(bind=engine)

	ses = Session()

	ses.add(one_user)

	#ses.close()

	our_user = ses.query(User).filter_by(name="one").first() 

	print "is equal", one_user is our_user

