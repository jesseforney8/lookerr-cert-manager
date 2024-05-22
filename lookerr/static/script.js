function add_devices(){
    let device_name = document.getElementById("device_name").value;
    let device_ip = document.getElementById("device_ip").value;
    let server_user = document.getElementById("server_user").value;
    let server_pass = document.getElementById("server_password").value;
    let filepath = document.getElementById("filepath").value;

    if (document.getElementById("Windows").checked) {
        var os = document.getElementById("Windows").value;


    } else {
        var os = document.getElementById("Linux").value;


    };
    
    
    console.log(os)

    fetch("/devices", {
              method: "POST",
              body: JSON.stringify({name: device_name, ip: device_ip, os: os, server_user: server_user, server_pass: server_pass, file_path: filepath, device_cert: "dummy"}),
            }).then((_res) => {
                window.location.href = "/devices";
            });
          
  }