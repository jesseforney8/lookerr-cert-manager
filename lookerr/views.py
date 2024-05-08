from flask_login import login_user, login_required, logout_user, current_user
from database import Device, db
from flask import Flask, redirect, url_for, render_template, Blueprint, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash

def create_device(name, ip, os, device_user, device_pass, filepath, cert):
        new_device = Device(name=name,ip_address=ip,os=os,device_user=device_user,device_paassword=device_pass,filepath=filepath,ssl_cert=cert)
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
                device = json.loads(request.data)
                device_name = device["name"]
                device_ip = device["ip"]
                device_os = device["os"]
                server_user = device["server_user"]
                server_pass = device["server_pass"]
                filepath = device["file_path"]
                device_cert = device["device_cert"]
                
                create_device(device_name, device_ip, device_os, server_user, server_pass, filepath, device_cert)

                

        return render_template("devices.html", user=current_user)