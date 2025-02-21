function togglePasswordVisibility() {
    const passwordInput = document.getElementById('login_patient_password');
    const button = document.getElementById('button-addon2');

    if (passwordInput && button) { // Ensure elements exist
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            button.textContent = 'visibility'; // Show password
        } else {
            passwordInput.type = 'password';
            button.textContent = 'visibility_off'; // Hide password
        }
    }
}

// jQuery version (if needed)
$(document).ready(function () {
    $('#button-addon3').on('click', function () {
        const passwordInput = $('#login_patient_password'); // Match the correct ID
        const isPasswordVisible = passwordInput.attr('type') === 'text';

        // Toggle password visibility
        passwordInput.attr('type', isPasswordVisible ? 'password' : 'text');

        // Toggle icon
        $(this).text(isPasswordVisible ? 'visibility_off' : 'visibility');
    });
});
