$(document).ready(function() {
    $("#frmLogin_patient").submit(function(e) {
        e.preventDefault();
        console.log('login');

        const email = $('#login_patient_email').val().trim();
        const password = $('#login_patient_password').val().trim();

        if (!email) {
            alertify.error("Please Enter Email.");
            return;
        }
        if (!password) {
            alertify.error("Please Enter Password");
            return;
        }

        // Create JSON object from form data
        var formData = {
            email: email,
            password: password
        };

        // Send data to the server
        $.ajax({
            type: "POST",
            url: "/post_login_patient",
            contentType: "application/json",
            data: JSON.stringify(formData),
            dataType: "json",
            success: function(response) {
                
                if (response.status == "success") {
                    console.log(response);
                    alertify.success(response.message);
                    setTimeout(function() {
                        window.location.href = "/patient/home_patient";
                    }, 1000);
                } else if (response.status === "error") {
                    alertify.error(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
                alertify.error("An error occurred while logging in. Please try again.");
            }
        });
    });
});
