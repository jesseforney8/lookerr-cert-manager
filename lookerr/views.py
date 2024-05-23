from flask_login import login_user, login_required, logout_user, current_user
from database import Device, db
from flask import Flask, redirect, url_for, render_template, Blueprint, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
                device_cert.save(f"lookerr/certs/{device_cert.filename}")
        
                
                create_device(device_name, device_ip, device_os, server_user, server_pass, filepath, device_cert.filename)

                return redirect("/devices")

        
        device_list = db.session.query(Device).all()
        
                

        return render_template("devices.html", user=current_user, device_list=device_list)