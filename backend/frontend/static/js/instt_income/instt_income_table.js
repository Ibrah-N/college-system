async function loadSelection() {

  // == shift ==
  const response1 = await fetch(`/helper/get_shift`);
  const shiftData = await response1.json();

  const shiftSelect = document.getElementById("shift");
  shiftSelect.innerHTML = '<option value="">-Shift-</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });

  
}
loadSelection();



async function deleteIncome(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this Income?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    id
  });

  const response = await fetch(`/account/delete_income?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Income deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Income"}`);
  }
}


async function exportIncomes() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/account/export_incomes", {
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
  a.download = "exported_incomes.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}




async function updateIncome(income_id) {
    window.location.href = `/account/update_income_stage_1/${income_id}`;
}