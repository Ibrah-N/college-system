async function deleteEnrollment(
  student_id,
  class_code_id,
  department_id,
  course_id,
  admission_type_id,
  semester_id,
  shift_id
) {
  const confirmed = confirm("Are you sure you want to delete this enrollment?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    student_id,
    class_code_id,
    department_id,
    course_id,
    admission_type_id,
    semester_id,
    shift_id
  });

  const response = await fetch(`/student/delete_enrollment?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Enrollment deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete enrollment"}`);
  }
}
