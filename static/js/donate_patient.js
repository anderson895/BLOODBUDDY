$(document).ready(function() {
    const bloodCompatibility = {
        "A+": { receive: "A+, A-, O+, O-", donate: "A+, AB+" },
        "A-": { receive: "A-, O-", donate: "A+, A-, AB+, AB-" },
        "B+": { receive: "B+, B-, O+, O-", donate: "B+, AB+" },
        "B-": { receive: "B-, O-", donate: "B+, B-, AB+, AB-" },
        "AB+": { receive: "A+, A-, B+, B-, AB+, AB-, O+, O-", donate: "AB+" },
        "AB-": { receive: "A-, B-, AB-, O-", donate: "AB+, AB-" },
        "O+": { receive: "O+, O-", donate: "O+, A+, B+, AB+" },
        "O-": { receive: "O-", donate: "O+, O-, A+, A-, B+, B-, AB+, AB-" }
    };

    // Enable/disable button based on selection
    $("#blood-type").change(function() {
        let bloodType = $(this).val();
        $("#check-compatibility").prop("disabled", bloodType === "");
        
    });

    // Check blood compatibility
    $("#check-compatibility").click(function() {
        let bloodType = $("#blood-type").val();
        if (bloodType && bloodCompatibility[bloodType]) {
            $("#result-title").text(`YOU ARE BLOOD TYPE ${bloodType} !`);
            $("#receive-list").text(bloodCompatibility[bloodType].receive);
            $("#donate-list").text(bloodCompatibility[bloodType].donate);
            $("#form-container").fadeOut(300, function() {
                $("#result-container").fadeIn(300);
            });
        } 
    });

    // Reset form
    $("#reset").click(function() {
        $("#result-container").fadeOut(300, function() {
            $("#form-container").fadeIn(300);
            $("#blood-type").val("");
            $("#check-compatibility").prop("disabled", true);
        });
    });



// Show Donor Form when Donate is clicked
    $("#donate-button").click(function() {
        let bloodType = $("#blood-type").val();
        if (bloodType && bloodCompatibility[bloodType]) {
            let donateOptions = bloodCompatibility[bloodType].donate.split(", ");

            let donorSelect = $("#donor-bloodtype");
            donorSelect.empty(); // Clear previous options
            donorSelect.append('<option value="">Donate blood type</option>');

            donateOptions.forEach(type => {
                donorSelect.append(`<option value="${type}">${type}</option>`);
            });

            $("#result-container").fadeOut(300, function() {
                $("#donor-form").fadeIn(300);
            });
        }
    });
    // Hide Donor Form and go back
    $("#go-back").click(function() {
        $("#donor-form").fadeOut(300, function() {
            $("#result-container").fadeIn(300);
        });
    });


// Show recipient list when "RECEIVE" is clicked
$("#receive-button").click(function () {
let bloodType = $("#blood-type").val().trim().toUpperCase();

console.log("📌 Selected Blood Type:", bloodType);
if (!bloodType || !bloodCompatibility[bloodType]) {
    alert("Please select a valid blood type.");
    return;
}

let receiveOptions = bloodCompatibility[bloodType].receive.split(", ").map(bt => bt.trim().toUpperCase());
console.log("📌 Can Receive From:", receiveOptions);

// AJAX request to fetch donors from the server
$.ajax({
    url: "/get-donors?patient_id={{ session['patient_id'] }}",
    type: "GET",
    dataType: "json",
    success: function (response) {
        console.log("✅ Full Server Response:", JSON.stringify(response, null, 2));

        // Ensure the response is an array
        let donors = Array.isArray(response) ? response : [];

        if (!donors.length) {
            console.error("❌ No donors found in response.");
            alert("Error: No donor data received.");
            return;
        }

        // Extract donor blood types
        let bloodTypesList = donors.map(donor => donor.donor_bloodtype ? donor.donor_bloodtype.trim().toUpperCase() : null);
        console.log("📌 Available Donors Blood Types:", bloodTypesList);

        // Filtering donors based on blood type compatibility
        let filteredDonors = donors.filter(donor => {
            if (!donor.donor_bloodtype) return false;
            let donorBloodType = donor.donor_bloodtype.trim().toUpperCase();
            console.log(`🩸 Checking Donor: ${donor.donor_name} | Type: ${donorBloodType}`);

            return receiveOptions.includes(donorBloodType);
        });

        console.log("✅ Matching Donors:", filteredDonors);

        let donorContainer = $(".grid-cols-1");
        donorContainer.empty();

        if (filteredDonors.length > 0) {
            let donorHTML = filteredDonors.map(donor => `
                <div class="border border-red-500 p-4 rounded-lg text-red-700 text-center italic">
                    <span class="font-bold">${donor.donor_name}</span><br>
                    Blood Type: ${donor.donor_bloodtype} <br>
                    Age: ${donor.donor_age} <br>
                    City: ${donor.donor_city} <br>
                    Contact: ${donor.donor_contact} <br>
                    Email: ${donor.donor_email}
                </div>
            `).join("");

            donorContainer.append(donorHTML);
        } else {
            donorContainer.append(`<p class="text-red-700 italic">No matching donors found.</p>`);
        }

        $("#result-container").fadeOut(300, function () {
            $(".w-full.max-w-4xl").fadeIn(300);
        });
    },
    error: function (xhr, status, error) {
        console.error("❌ AJAX Error:", status, error);
        alert("Failed to fetch donor data. Please try again.");
    }
});
});




$("#frmDonate").submit(function(e) {
    e.preventDefault();
  
    const donor_name = $('#donor-name').val().trim();
    const donor_age = $('#donor-age').val().trim();
    const donor_city = $('#donor-city').val().trim();
    const donor_contact = $('#donor-contact').val().trim();
    const donor_email = $('#donor-email').val().trim();
    const donor_bloodtype = $('#donor-bloodtype').val().trim();
    const donor_id = $('#donor-id').val().trim();

    if (!donor_name) {
        alertify.error("Please Enter Name.");
        return;
    }
    if (!donor_age) {
        alertify.error("Please Enter Age");
        return;
    }

    if (!donor_city) {
        alertify.error("Please Enter City");
        return;
    }

    if (!donor_contact) {
        alertify.error("Please Enter Contact Number");
        return;
    }
    if (!donor_email) {
        alertify.error("Please Enter Email");
        return;
    }

    if (!donor_bloodtype) {
        alertify.error("Please Select Bloodtype");
        return;
    }

    $('.spinner').show();
    $('#confirm-donation').prop('disabled', true);

    // Create JSON object from form data
    var formData = {
        donor_id: donor_id,
        donor_name: donor_name,
        donor_age: donor_age,
        donor_city: donor_city,
        donor_contact: donor_contact,
        donor_email: donor_email,
        donor_bloodtype: donor_bloodtype
    };

    // Send data to the server
    $.ajax({
        type: "POST",
        url: "/post_patient_donate",
        contentType: "application/json",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function(response) {

            console.log(response);
            
            if (response.status == "success") {
                console.log(response);
                alertify.success(response.message);
                setTimeout(function() {
                    window.location.href = "/patient/donation_success";
                }, 1000);
            } else if (response.status === "error") {
                alertify.error(response.message);
                $('.spinner').hide();
                $('#btnSignup').prop('disabled', false);
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", status, error);
            alertify.error("An error occurred while logging in. Please try again.");
        }
    });
});

});