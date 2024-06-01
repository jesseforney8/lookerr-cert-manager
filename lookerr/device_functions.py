from database import Device, User, db
from werkzeug.security import generate_password_hash, check_password_hash

def create_device(name, ip, os, device_user, device_pass, filepath, cert):
        new_device = Device(name=name,ip_address=ip,os=os,device_user=device_user,device_password=device_pass,filepath=filepath,ssl_cert=cert, sync_status=False)
        db.session.add(new_device)
        db.session.commit()

def create_user(email, password):
     user = User(email=email, password=generate_password_hash(password, method="scrypt"))
     db.session.add(user)
     db.session.commit()