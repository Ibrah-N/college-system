document.getElementById("teacherForm").addEventListener("submit", function (e) {
    e.preventDefault();
    clearValidation();

    let isValid = true;

    // ===== Teacher Name =====
    if (!validateField(
        document.querySelector("input[name='teacher_name']"),
        val => val !== "",
        "Teacher name is required"
    )) isValid = false;

    // ===== Father Name =====
    if (!validateField(
        document.querySelector("input[name='father_name']"),
        val => val !== "",
        "Father name is required"
    )) isValid = false;

    // ===== Qualification =====
    if (!validateField(
        document.querySelector("input[name='qualification']"),
        val => val !== "",
        "Qualification is required"
    )) isValid = false;

    // ===== Contact =====
    if (!validateField(
        document.querySelector("input[name='contact']"),
        val => {
            const p1 = /^03\d{2}-\d{7}$/;
            const p2 = /^03\d{9}$/;
            return p1.test(val) || p2.test(val);
        },
        "Contact must be 03xx-xxxxxxx or 03xxxxxxxxx"
    )) isValid = false;

    // ===== Gender =====
    if (!validateField(
        document.querySelector("select[name='gender']"),
        val => val !== "",
        "Please select gender"
    )) isValid = false;

    // ===== Address =====
    if (!validateField(
        document.querySelector("input[name='address']"),
        val => val !== "",
        "Address is required"
    )) isValid = false;

    // ===== Submit =====
    if (isValid) {
        setTimeout(() => this.submit(), 200);
    }
});

/* ===== Helper functions ===== */

function validateField(element, conditionFn, message) {
    const value = element.value.trim();

    if (!conditionFn(value)) {
        element.classList.add("input-error");
        element.classList.remove("input-success");
        showError(element, message);
        return false;
    } else {
        element.classList.add("input-success");
        element.classList.remove("input-error");
        return true;
    }
}

function showError(element, message) {
    if (element.nextElementSibling?.classList.contains("error-message")) return;

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