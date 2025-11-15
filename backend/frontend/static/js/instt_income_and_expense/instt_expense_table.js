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

  
  // == session ==
  const response3 = await fetch(`/helper/get_sessions`);
  const sessionData = await response3.json();

  const sessionSelect = document.getElementById("session");
  sessionSelect.innerHTML = '<option value="">-Session-</option>';
  sessionData.sessions.forEach(s => {
    const option = document.createElement("option");
    option.value = s.id;
    option.textContent = s.name;
    sessionSelect.appendChild(option);
  });


  // == month ==
  const response4 = await fetch(`/helper/get_months`);
  const month_data = await response4.json();

  const monthSelect = document.getElementById("month");
  monthSelect.innerHTML = '<option value="">-Month-</option>';
  month_data.months.forEach(m => {
    const option = document.createElement("option");
    option.value = m.id;
    option.textContent = m.name;
    monthSelect.appendChild(option);
  });


  // == day ==
  const response5 = await fetch(`/helper/get_days`);
  const day_data = await response5.json();

  const daySelect = document.getElementById("day");
  daySelect.innerHTML = '<option value="">-Day-</option>';
  day_data.days.forEach(d => {
    const option = document.createElement("option");
    option.value = d.id;
    option.textContent = d.name;
    daySelect.appendChild(option);
  });
}
loadSelection();



async function deleteExpenses(
  id,
  session_id,
  month_id,
  day_id,
) {
  const confirmed = confirm("Are you sure you want to delete this Expense?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    id,
    session_id,
    month_id,
    day_id,
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
