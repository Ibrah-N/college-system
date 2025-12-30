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

  const shiftSelect = document.getElementById("shift_id");
  shiftSelect.innerHTML = '<option value="">-- Select Shift --</option>';
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