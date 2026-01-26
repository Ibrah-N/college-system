async function loadSelection() {

  // == shift ==
  const response1 = await fetch(`/helper/get_shift`);
  const shiftData = await response1.json();

  const shiftSelect = document.getElementById("shift_id");
  shiftSelect.innerHTML = '<option value="">-- Select Shift --</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });


      // == department ==
  const response = await fetch(`/helper/get_department`);
  const departmentData = await response.json();

  const departmentSelected = document.getElementById("department_id");
  departmentSelected.innerHTML = '<option value="">-- Select Dept --</option>';
  departmentData.departments.forEach(dp => {
    const option = document.createElement("option");
    option.value = dp.id;
    option.textContent = dp.department;
    departmentSelected.appendChild(option);
  });


  // == Contract type ==
  const response3 = await fetch(`/helper/get_admission_type`);
  const contractData = await response3.json();

  const contractSelected = document.getElementById("contract_type_id");
  contractSelected.innerHTML = '<option value="">-- Select Contract --</option>';
  contractData.admission_type.forEach(adm_type => {
    const option = document.createElement("option");
    option.value = adm_type.id;
    option.textContent = adm_type.name;
    contractSelected.appendChild(option);
  });

}


window.onload = function() {
  loadSelection();
};



document.getElementById("teacherRegistractionForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // stop default submission
    clearValidation();

    const teacherIdInput = document.querySelector("input[name='teacher_id']");
    const teacherId = teacherIdInput.value.trim();

    // ===== 1️⃣ Check teacher existence (must exist first) =====
    if (teacherId === "") {
        showFieldError(teacherIdInput, "Teacher ID is required");
        return;
    }

    try {
        const response = await fetch("/teacher/check_teacher", { // POST endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ teacher_id: teacherId })
        });

        if (!response.ok) throw new Error("Network error");

        const result = await response.json();

        if (!result.exists) { // teacher must exist
            showFieldError(teacherIdInput, "Teacher not found. Please add teacher first.");
            return;
        }

    } catch (err) {
        console.error(err);
        alert("Server error. Try again.");
        return;
    }

    // ===== 2️⃣ Validate rest of fields =====
    let isValid = true;

    isValid &= validateSelect("department_id", "Please select department");
    isValid &= validateSelect("contract_type_id", "Please select contract type");
    isValid &= validateSelect("shift_id", "Please select shift");

    isValid &= validateInput(
        document.querySelector("input[name='salary']"),
        val => /^\d+$/.test(val),
        "Salary must be numeric"
    );

    // ===== 3️⃣ Submit form if all valid =====
    if (isValid) {
        this.submit();
    }
});

/* ===== Helper functions ===== */
function validateSelect(name, message) {
    const el = document.querySelector(`select[name='${name}']`);
    if (!el.value) {
        el.classList.add("input-error");
        showError(el, message);
        return false;
    }
    el.classList.add("input-success");
    return true;
}

function validateInput(el, conditionFn, message) {
    const value = el.value.trim();
    if (!conditionFn(value)) {
        el.classList.add("input-error");
        showError(el, message);
        return false;
    }
    el.classList.add("input-success");
    return true;
}

function showFieldError(el, message) {
    el.classList.add("input-error");
    showError(el, message);
}

function showError(el, message) {
    if (el.nextElementSibling?.classList.contains("error-message")) return;
    const div = document.createElement("div");
    div.className = "error-message";
    div.innerText = message;
    el.insertAdjacentElement("afterend", div);
}

function clearValidation() {
    document.querySelectorAll(".input-error, .input-success").forEach(el => el.classList.remove("input-error", "input-success"));
    document.querySelectorAll(".error-message").forEach(e => e.remove());
}
