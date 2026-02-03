async function deleteTestInfo(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this testinfo record?");
  if (!confirmed) return;

  const response = await fetch(`/scholarship/delete_testinfo/${id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Testinfo record deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Testinfo record"}`);
  }
}