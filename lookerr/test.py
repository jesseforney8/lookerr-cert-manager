from database import db, User


user = User(id=1,username="bobby14",email="bobbydoggy@gmail.com")

db.session.add(user)
db.session.commit()
print("Done")