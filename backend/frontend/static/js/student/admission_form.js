document.getElementById("admissionForm").addEventListener("submit", function(e) {
    e.preventDefault();
    clearValidation();

    let isValid = true;

    // ===== General text fields =====
    isValid &= validateField(
        document.querySelector("input[name='student_name']"),
        val => val !== "",
        "Student name is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='father_name']"),
        val => val !== "",
        "Father/Guardian name is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='date_of_birth']"),
        val => val !== "",
        "Date of birth is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='nationality']"),
        val => val !== "",
        "Nationality is required"
    );

    isValid &= validateField(
        document.querySelector("select[name='gender']"),
        val => val !== "",
        "Please select gender"
    );

    // ===== CNIC (optional) =====
    isValid &= validateFieldOptional(
        document.querySelector("input[name='cnic']"),
        val => {
            if (val === "") return true; // optional
            const cnicPatternHyphen = /^\d{5}-\d{7}-\d{1}$/;
            const cnicPatternNoHyphen = /^\d{13}$/;
            return cnicPatternHyphen.test(val) || cnicPatternNoHyphen.test(val);
        },
        "CNIC must be 00000-0000000-0 or 13 digits"
    );

    // ===== Mobile (mandatory) =====
    isValid &= validateField(
        document.querySelector("input[name='mobile']"),
        val => {
            const mobilePatternHyphen = /^03\d{2}-\d{7}$/;
            const mobilePatternNoHyphen = /^03\d{9}$/;
            return mobilePatternHyphen.test(val) || mobilePatternNoHyphen.test(val);
        },
        "Mobile must be 03xx-xxxxxxx or 03xxxxxxxxx"
    );

    // ===== Emergency Contact (mandatory) =====
    isValid &= validateField(
        document.querySelector("input[name='emergency_no']"),
        val => {
            const mobilePatternHyphen = /^03\d{2}-\d{7}$/;
            const mobilePatternNoHyphen = /^03\d{9}$/;
            return mobilePatternHyphen.test(val) || mobilePatternNoHyphen.test(val);
        },
        "Emergency contact must be 03xx-xxxxxxx or 03xxxxxxxxx"
    );

    // ===== Address fields =====
    isValid &= validateField(
        document.querySelector("input[name='temp_address']"),
        val => val !== "",
        "Temporary address is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='perm_address']"),
        val => val !== "",
        "Permanent address is required"
    );

    // ===== Academic Qualification =====
    isValid &= validateField(
        document.querySelector("input[name='degree']"),
        val => val !== "",
        "Degree is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='name_of_institute']"),
        val => val !== "",
        "Name of institute is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='academic-year']"),
        val => val !== "" && !isNaN(val),
        "Year is required and must be a number"
    );

    isValid &= validateField(
        document.querySelector("input[name='grade']"),
        val => val !== "",
        "Grade is required"
    );

    if (isValid) this.submit();
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

// Optional field validation
function validateFieldOptional(element, conditionFn, message) {
    const value = element.value.trim();
    if (value === "") return true; // optional
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
