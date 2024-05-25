from flask_login import login_user, login_required, logout_user, current_user
from database import Device, db
from flask import Flask, redirect, url_for, render_template, Blueprint, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress
import os

class NamerForm(FlaskForm):
        name = StringField("What's your name?", validators=[DataRequired()])
        submit = SubmitField("Submit")







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
        
        
                

        return render_template("devices.html", user=current_user, device_list=device_list, cert_list = os.listdir(os.getcwd() + "/lookerr/certs"))


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


@views.route("/upload_cert", methods=["POST"])
@login_required
def upload_cert():
        if request.method == "POST":
                device_id = request.form.get("cert_id")
                device_cert = request.files["new_crt"]
                
                device = Device.query.get(device_id)
              
                device.ssl_cert = device_cert.filename
                db.session.commit()
                        
                if device_cert.filename != "":
                        device_cert.save(f"lookerr/certs/{device_cert.filename}")





        return redirect("/devices")


@views.route("/select_cert", methods=["POST"])
@login_required
def select_cert():
        if request.method == "POST":
                device_id = request.form.get("cert_id")
                cert_selection = request.form.get("cert_select")
                device = Device.query.get(device_id)
                device.ssl_cert = cert_selection
                db.session.commit()

        return redirect("/devices")



@views.route("/delete_cert", methods=["POST"])
@login_required
def delete_cert():
        if request.method == "POST":
                cert_selection = request.form.get("cert_select")
        
                if os.path.exists(os.getcwd() + f"/lookerr/certs/{cert_selection}"):
                        device_list = Device.query.filter_by(ssl_cert=cert_selection)
                        for device in device_list:
                                device.ssl_cert = ""
                        db.session.commit()
                        os.remove(os.getcwd() + f"/lookerr/certs/{cert_selection}")
                
                
                

        return redirect("/devices")