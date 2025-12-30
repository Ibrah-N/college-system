async function loadDepartment() {

  const response = await fetch("/helper/get_department");
  const data = await response.json();

  const select = document.getElementById("department");
  select.innerHTML = '<option value="">-Department-</option>';


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
  courseSelect.innerHTML = '<option value="">-Course-</option>';

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

  const shiftSelect = document.getElementById("shift_id");
  shiftSelect.innerHTML = '<option value="">-Shift-</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });
}


window.onload = function() {
  loadDepartment();
  loadSelection();
};


async function deleteRegistration(
  teacher_id,
  department_id,
  course_id,
  shift_id
) {
  const confirmed = confirm("Are you sure you want to delete this registration?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    teacher_id,
    department_id,
    course_id,
    shift_id
  });

  const response = await fetch(`/teacher/delete_registration?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Registration deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Registration"}`);
  }
}


async function exportRegistration() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/teacher/export_registration", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    alert("Export failed");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "registration_export.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
