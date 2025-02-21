$(document).ready(function() {
    $("#frmCreateAccount").submit(function (e) {
        e.preventDefault();
        console.log('click');
      

        // Validate form fields
        const fullname = $('#fullname').val().trim();
        const email = $('#email').val().trim();
        const password = $('#password').val().trim();

        // Basic validation
        if (!fullname) {
            alertify.error("Please Enter Fullname.");
            return;
        }
        // Basic validation
        if (!email) {
            alertify.error("Please Enter Email.");
            return;
        }
        // Basic validation
        if (!password) {
            alertify.error("Please Enter Password");
            return;
        }

        // Validate email format
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
            alertify.error("Please enter a valid email address.");
            $('#email').addClass('is-invalid');
            return;
        }

   
        // Prepare data to send
        const data = {
            full_name: fullname,
            email: email,
            password: password
        };

        // Send data to the server
        $.ajax({
            type: "POST",
            url: "/createPatientAccount",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(response) {
               console.log(response);
               if(response.status=="success"){
                    alertify.success(response.message);
                    setTimeout(function () {
                        window.location.href = "/login"; 
                      }, 1000);
               }else if(response.status=="error"){
                    alertify.error(response.message);
               }
            },
        });
    });
});
