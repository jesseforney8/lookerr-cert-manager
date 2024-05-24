function update_devices(device_id){
        
    let device_name = document.getElementById("device_name_update" + device_id).value;
    let device_ip = document.getElementById("device_ip_update"+ device_id).value;
    let server_user = document.getElementById("server_user_update"+ device_id).value;
    let server_pass = document.getElementById("server_password_update"+ device_id).value;
    let filepath = document.getElementById("filepath_update"+ device_id).value;
    


    if (document.getElementById("Windows_update"+ device_id).checked) {
        var os = document.getElementById("Windows_update"+ device_id).value;


    } else {
        var os = document.getElementById("Linux_update"+ device_id).value;


    };
    
    
    

    fetch("/devices-update", {
              method: "POST",
              body: JSON.stringify({id: device_id, name: device_name, ip: device_ip, os: os, server_user: server_user, server_pass: server_pass, file_path: filepath}),
            }).then((_res) => {
                window.location.href = "/devices";
            });
          
  };

function new_cert() {
    document.getElementById("upload_div").style.display = "block";
    
    


};