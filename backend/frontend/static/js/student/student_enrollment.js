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


  // == class code ==
  const response2 = await fetch(`/helper/get_class_code`);
  const classCode_data = await response2.json();

  const classcodeSelect = document.getElementById("class_code_id");
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

  const admissiontypeSelect = document.getElementById("admission_type_id");
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

  const semesterSelect = document.getElementById("semester_id");
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