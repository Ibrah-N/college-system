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



async function deleteExpenses(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this Expense?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    id
  });

  const response = await fetch(`/account/delete_expense?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Expense deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Expense"}`);
  }
}


async function exportExpenses() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/account/export_expenses", {
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
  a.download = "exported_expenses.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}




async function updateExpense(expense_id) {
    window.location.href = `/account/update_expense_stage_1/${expense_id}`;
}