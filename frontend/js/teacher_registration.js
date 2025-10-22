// -- define course --
const courses = {
  m: ["Anatomy", "Physiology", "Pharmacology", "Nursing"],
  it: ["Web Development", "Data Science", "Cyber Security", "AI & ML"],
  s_c: ["Marketing", "Finance", "Accounting", "Entrepreneurship"]
};

// -- extract the ids --
const departmentSelect = document.getElementById("department");
const courseSelect = document.getElementById("course");

// -- listener function for department --
departmentSelect.addEventListener("change", function() {
  const selectDept = this.value;
  courseSelect.innerHTML = "<option value=''>-- Select Course --</option>";

  // -- check selected dept & course list --
  if (selectDept && courses[selectDept]) {
    courses[selectDept].forEach(course => {
      const htmlElement = document.createElement("option");
      htmlElement.value = course.toLowerCase().replace(/\s+/g, "_");
      htmlElement.textContent = course;
      courseSelect.appendChild(htmlElement);
    });
  }
});
