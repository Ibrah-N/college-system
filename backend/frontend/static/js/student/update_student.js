document.getElementById("admissionForm").addEventListener("submit", function(e) {
    e.preventDefault();
    clearValidation();

    let isValid = true;

    // General fields
    isValid = validateField(document.querySelector("input[name='student_name']"), val => val !== "", "Student name is required") && isValid;
    isValid = validateField(document.querySelector("input[name='father_name']"), val => val !== "", "Father/Guardian name is required") && isValid;
    isValid = validateField(document.querySelector("input[name='date_of_birth']"), val => val !== "", "Date of birth is required") && isValid;
    isValid = validateField(document.querySelector("input[name='nationality']"), val => val !== "", "Nationality is required") && isValid;
    isValid = validateField(document.querySelector("select[name='gender']"), val => val !== "", "Please select gender") && isValid;

    // CNIC (optional)
    isValid = validateFieldOptional(document.querySelector("input[name='cnic']"), val => {
        if (val === "") return true;
        const cnicPatternHyphen = /^\d{5}-\d{7}-\d{1}$/;
        const cnicPatternNoHyphen = /^\d{13}$/;
        return cnicPatternHyphen.test(val) || cnicPatternNoHyphen.test(val);
    }, "CNIC must be 00000-0000000-0 or 13 digits") && isValid;

    // Mobile & Emergency
    isValid = validateField(document.querySelector("input[name='mobile']"), val => {
        const pattern1 = /^03\d{2}-\d{7}$/;
        const pattern2 = /^03\d{9}$/;
        return pattern1.test(val) || pattern2.test(val);
    }, "Mobile must be 03xx-xxxxxxx or 03xxxxxxxxx") && isValid;

    isValid = validateField(document.querySelector("input[name='emergency_no']"), val => {
        const pattern1 = /^03\d{2}-\d{7}$/;
        const pattern2 = /^03\d{9}$/;
        return pattern1.test(val) || pattern2.test(val);
    }, "Emergency contact must be 03xx-xxxxxxx or 03xxxxxxxxx") && isValid;

    // Addresses
    isValid = validateField(document.querySelector("input[name='temp_address']"), val => val !== "", "Temporary address is required") && isValid;
    isValid = validateField(document.querySelector("input[name='perm_address']"), val => val !== "", "Permanent address is required") && isValid;

    // Academic
    isValid = validateField(document.querySelector("input[name='degree']"), val => val !== "", "Degree is required") && isValid;
    isValid = validateField(document.querySelector("input[name='name_of_institute']"), val => val !== "", "Name of institute is required") && isValid;
    isValid = validateField(document.querySelector("input[name='academic-year']"), val => val !== "" && !isNaN(val), "Year is required and must be a number") && isValid;
    isValid = validateField(document.querySelector("input[name='grade']"), val => val !== "", "Grade is required") && isValid;

    if (isValid) {
        setTimeout(() => this.submit(), 150);
        this.submit();
    } 
});

/* ===== Helper functions ===== */
function validateField(element, conditionFn, message) {
    const value = element.value.trim();

    if (!conditionFn(value)) {
        element.classList.add("input-error");
        showError(element, message);
        return false;
    } else {
        element.classList.add("input-success");
        return true;
    }
}

function showError(element, message) {
    const error = document.createElement("div");
    error.className = "error-message";
    error.innerText = message;
    element.insertAdjacentElement("afterend", error);
}

function clearValidation() {
    document.querySelectorAll(".input-error, .input-success")
        .forEach(el => el.classList.remove("input-error", "input-success"));

    document.querySelectorAll(".error-message")
        .forEach(el => el.remove());
}


function validateFieldOptional(element, conditionFn, message) {
    const value = element.value.trim();
    if (value === "") return true;

    if (!conditionFn(value)) {
        element.classList.add("input-error");
        showError(element, message);
        return false;
    } else {
        element.classList.add("input-success");
        return true;
    }
}
