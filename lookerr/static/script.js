function add_devices(){
    let device_name = document.getElementById("device_name").value;
    let device_ip = document.getElementById("device_ip").value;
    let server_user = document.getElementById("server_user").value;
    let server_pass = document.getElementById("server_password").value;
    let filepath = document.getElementById("filepath").value;
    

    fetch("/devices", {
              method: "POST",
              body: JSON.stringify({name: device_name, ip: device_ip, os: "dummy", server_user: server_user, server_pass: server_pass, file_path: filepath, device_cert: "dummy"}),
            }).then((_res) => {
                window.location.href = "/devices";
            });
          
  }