from flask_login import login_user, login_required, logout_user, current_user
from database import Device, db
from flask import Flask, redirect, url_for, render_template, Blueprint, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash

def create_device(name, ip, os, device_user, device_pass, filepath, cert):
        new_device = Device(name=name,ip_address=ip,os=os,device_user=device_user,device_password=device_pass,filepath=filepath,ssl_cert=cert)
        db.session.add(new_device)
        db.session.commit()
     

views = Blueprint("views", __name__, url_prefix='/views')

@views.route("/")
@login_required
def home():
        return render_template("home.html", user=current_user)

@views.route("/devices", methods=["POST", "GET"])
@login_required
def devices():

        if request.method == "POST":
                test = request.form
                print(test)
                device_name = request.form.get("device_name")
                device_ip = request.form.get("device_ip")
                device_os = request.form["flexRadioDefault"]
                server_user = request.form.get("server_user")
                server_pass  = request.form.get("server_password")
                filepath = request.form.get("filepath")
                
                device_cert = request.files["crt"]
                if device_cert.filename != "":
                        device_cert.save(f"lookerr/certs/{device_cert.filename}")
                
                create_device(device_name, device_ip, device_os, server_user, server_pass, filepath, device_cert.filename)
               
                        
                        

        
                
                

                return redirect("/devices")

        
        device_list = db.session.query(Device).all()
        
        
                

        return render_template("devices.html", user=current_user, device_list=device_list)


@views.route("/devices-update", methods=["POST"])
@login_required
def devices_update():
        if request.method == "POST":
               device_json = json.loads(request.data)
               device_id = device_json["id"]
               device_name = device_json["name"]
               device_ip = device_json["ip"]
               device_os = device_json["os"]
               device_user = device_json["server_user"]
               device_pass = device_json["server_pass"]
               filepath = device_json["file_path"]
               device = Device.query.get(device_id)
               

               device.name = device_name
               device.ip_address = device_ip
               device.os = device_os
               device.device_user = device_user
               device.device_password = device_pass
               device.filepath = filepath
               db.session.commit()
        return redirect("/devices")