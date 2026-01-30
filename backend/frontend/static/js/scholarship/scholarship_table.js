async function deleteScholarship(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this scholarship record?");
  if (!confirmed) return;

  const response = await fetch(`/scholarship/delete/${id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Scholarship record deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Scholarship record"}`);
  }
}


async function loadSelection() {
  // == Course ==
  const response1 = await fetch(`/helper/get_courses_only`);
  const courseData = await response1.json();

  const courseSelect = document.getElementById("course_apply_for_id");
  courseSelect.innerHTML = '<option value="">-- Course --</option>';
  courseData.courses.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    courseSelect.appendChild(option);
  });
}


window.onload = function() {
  loadSelection();
};


async function exportScholarship() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/scholarship/export", {
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
  a.download = "scholarship_export.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
