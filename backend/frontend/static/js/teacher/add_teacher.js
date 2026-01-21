

document.getElementById("teacherForm").addEventListener("submit", function (e) {
    e.preventDefault();
    clearValidation();

    let isValid = true;

    // ===== Teacher Name =====
    isValid &= validateField(
        document.querySelector("input[name='teacher_name']"),
        val => val !== "",
        "Teacher name is required"
    );

    // ===== Father Name =====
    isValid &= validateField(
        document.querySelector("input[name='father_name']"),
        val => val !== "",
        "Father name is required"
    );

    // ===== Qualification =====
    isValid &= validateField(
        document.querySelector("input[name='qualification']"),
        val => val !== "",
        "Qualification is required"
    );

    // ===== Contact (Mobile) =====
    isValid &= validateField(
        document.querySelector("input[name='contact']"),
        val => {
            const p1 = /^03\d{2}-\d{7}$/;
            const p2 = /^03\d{9}$/;
            return p1.test(val) || p2.test(val);
        },
        "Contact must be 03xx-xxxxxxx or 03xxxxxxxxx"
    );

    // ===== Gender =====
    isValid &= validateField(
        document.querySelector("select[name='gender']"),
        val => val !== "",
        "Please select gender"
    );

    // ===== Address =====
    isValid &= validateField(
        document.querySelector("input[name='address']"),
        val => val !== "",
        "Address is required"
    );

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

