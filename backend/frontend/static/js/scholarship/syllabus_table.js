async function deleteSyllabus(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this syllabus record?");
  if (!confirmed) return;

  const response = await fetch(`/scholarship/delete_syllabus/${id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Syllabus record deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Syllabus record"}`);
  }
}