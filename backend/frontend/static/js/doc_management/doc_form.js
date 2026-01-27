
async function loadSelection() {
  // == Doc Type ==
  const response1 = await fetch(`/helper/get_doc_types`);
  const docTypeData = await response1.json();

  const docTypeSelect = document.getElementById("doc_type");
  docTypeSelect.innerHTML = '<option value="">-- Select Doc Type --</option>';
  docTypeData.doc_types.forEach(dt => {
    const option = document.createElement("option");
    option.value = dt.id;
    option.textContent = dt.name;
    docTypeSelect.appendChild(option);
  });

}


window.onload = function() {
  loadSelection();
};


document.getElementById("studentDocsForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    clearValidation();

    let isValid = true;

    /* ===== Student ID (required + existence check) ===== */
    const studentIdInput = document.querySelector("input[name='student_id']");
    const studentId = studentIdInput.value.trim();

    if (studentId === "") {
        showFieldError(studentIdInput, "Student ID is required");
        return;
    }

    try {
        const response = await fetch("/student/check_student", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ student_id: studentId })
        });

        const result = await response.json();

        if (!result.exists) {
            showFieldError(studentIdInput, "Student not found. Please add student first.");
            return;
        } else {
            studentIdInput.classList.add("input-success");
        }
    } catch (err) {
        alert("Server error while checking student.");
        return;
    }

    /* ===== Doc Type (required) ===== */
    isValid &= validateField(
        document.querySelector("select[name='doc_type_id']"),
        val => val !== "",
        "Please select document type"
    );

    /* ===== Received By (required) ===== */
    isValid &= validateField(
        document.querySelector("input[name='recived_by']"),
        val => val !== "",
        "Received by is required"
    );

    /* ===== Receiver Phone (required) ===== */
    isValid &= validateField(
        document.querySelector("input[name='reciver_phone']"),
        val => {
            const mobilePatternHyphen = /^03\d{2}-\d{7}$/;
            const mobilePatternNoHyphen = /^03\d{9}$/;
            return mobilePatternHyphen.test(val) || mobilePatternNoHyphen.test(val);
        },
        "Receiver number must be 03xx-xxxxxxx or 03xxxxxxxxx"
    );

    /* ===== Note (optional) ===== */
    validateFieldOptional(
        document.querySelector("input[name='note']"),
        () => true,
        ""
    );

    /* ===== Submit ===== */
    if (isValid) this.submit();
});

/* ===== Helper Functions (same idea as example) ===== */

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

function showFieldError(element, message) {
    element.classList.add("input-error");
    showError(element, message);
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
