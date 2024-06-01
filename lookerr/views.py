from flask_login import login_user, login_required, logout_user, current_user
from database import Device, db
from flask import Flask, redirect, url_for, render_template, Blueprint, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
import os
from ssh_functions import show_dir, check_remote_cert
from device_functions import create_device


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
                device_cert = request.files["upload_cert1"]
                        
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


@views.route("/cert_check", methods=["POST"])
@login_required
def cert_check():
        if request.method == "POST":

                device_id_json = json.loads(request.data)
                device_id = device_id_json['id']

                filepath = r"C:\Users\Administrator\Documents\test1.cer"

                device = Device.query.get(device_id)

                device.sync_status = check_remote_cert(device.device_user, device.device_password, device.ip_address, filepath)

                db.session.commit()


        return redirect("/devices")
