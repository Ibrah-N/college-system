async function loadDepartment() {

  const response = await fetch("/helper/get_department");
  const data = await response.json();

  const select = document.getElementById("department");
  select.innerHTML = '<option value="">-- Select Dept --</option>';


  data.departments.forEach(dep => {
    const option = document.createElement("option");
    option.value = dep.id;
    option.textContent = dep.department;
    select.appendChild(option)
  });

  select.addEventListener("change", loadCourses);
}


async function loadCourses() {
  const dept_id = this.value;
  const courseSelect = document.getElementById("course");
  courseSelect.innerHTML = '<option value="">-- Select Course --</option>';

  if (!dept_id) return; // no department selected

  const response = await fetch(`/helper/get_courses?department_id=${dept_id}`);
  const courseData = await response.json();

  courseData.courses.forEach(course => {
    const option = document.createElement("option");
    option.value = course.id;
    option.textContent = course.name;
    courseSelect.appendChild(option);
  });
}


async function loadSelection() {
  // == shift ==
  const response1 = await fetch(`/helper/get_shift`);
  const shiftData = await response1.json();

  const shiftSelect = document.getElementById("shift");
  shiftSelect.innerHTML = '<option value="">-- Select Shift --</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });

  // == class code ==
  const response2 = await fetch(`/helper/get_class_code`);
  const classCode_data = await response2.json();

  const classcodeSelect = document.getElementById("class_code");
  classcodeSelect.innerHTML = '<option value="">-- Select Code --</option>';
  classCode_data.class_codes.forEach(cls_codes => {
    const option = document.createElement("option");
    option.value = cls_codes.id;
    option.textContent = cls_codes.name;
    classcodeSelect.appendChild(option);
  });

  // == admission type ==
  const response3 = await fetch(`/helper/get_admission_type`);
  const admissionType_data = await response3.json();

  const admissiontypeSelect = document.getElementById("admission_type");
  admissiontypeSelect.innerHTML = '<option value="">-- Select Type --</option>';
  admissionType_data.admission_type.forEach(adm_type => {
    const option = document.createElement("option");
    option.value = adm_type.id;
    option.textContent = adm_type.name;
    admissiontypeSelect.appendChild(option);
  });

  // == semester ==
  const response4 = await fetch(`/helper/get_semester`);
  const semester_data = await response4.json();

  const semesterSelect = document.getElementById("semester");
  semesterSelect.innerHTML = '<option value="">-- Select Semester --</option>';
  semester_data.semesters.forEach(semes => {
    const option = document.createElement("option");
    option.value = semes.id;
    option.textContent = semes.name;
    semesterSelect.appendChild(option);
  });

}


window.onload = function() {
  loadDepartment();
  loadSelection();
};



document.getElementById("studentEnrollmentForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    clearValidation();

    const studentIdInput = document.querySelector("input[name='student_id']");
    const studentId = studentIdInput.value.trim();

    // ===== 1️⃣ Check student existence =====
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
        }

    } catch (err) {
        alert("Server error. Try again.");
        return;
    }

    // ===== 2️⃣ Validate rest of fields =====
    let isValid = true;

    isValid &= validateSelect("department_id", "Please select department");
    isValid &= validateSelect("course_id", "Please select course");
    isValid &= validateSelect("shift_id", "Please select shift");
    isValid &= validateSelect("class_code_id", "Please select class code");
    isValid &= validateSelect("admission_type_id", "Please select admission type");
    isValid &= validateSelect("semester_id", "Please select semester");

    isValid &= validateInput(
        document.querySelector("input[name='fee']"),
        val => /^\d+$/.test(val),
        "Fee must be numeric"
    );

    // ===== 3️⃣ Submit =====
    if (isValid) {
        this.submit();
    }
});


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

function validateInput(el, condition, message) {
    if (!condition(el.value.trim())) {
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

function showError(el, msg) {
    if (el.nextElementSibling?.classList.contains("error-message")) return;
    const d = document.createElement("div");
    d.className = "error-message";
    d.innerText = msg;
    el.insertAdjacentElement("afterend", d);
}

function clearValidation() {
    document.querySelectorAll(".input-error, .input-success")
        .forEach(el => el.classList.remove("input-error", "input-success"));

    document.querySelectorAll(".error-message").forEach(e => e.remove());
}
