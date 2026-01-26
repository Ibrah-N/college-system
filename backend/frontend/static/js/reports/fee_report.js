async function loadSelection() {

  // == session ==
  const response1 = await fetch(`/helper/get_sessions`);
  const sessionData = await response1.json();

  const sessionSelect = document.getElementById("session_id");
  sessionSelect.innerHTML = '<option value="">Select Session</option>';
  sessionData.sessions.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    sessionSelect.appendChild(option);
  });


  // == month ==
  const response2 = await fetch(`/helper/get_months`);
  const monthData = await response2.json();

  const monthSelect = document.getElementById("month_id");
  monthSelect.innerHTML = '<option value="">Select Month</option>';
  monthData.months.forEach(mon => {
    const option = document.createElement("option");
    option.value = mon.id;
    option.textContent = mon.name;
    monthSelect.appendChild(option);
  });



  // == day ==
  const response3 = await fetch(`/helper/get_days`);
  const days_data = await response3.json();

  const daysSelect = document.getElementById("day_id");
  daysSelect.innerHTML = '<option value="">Select Day</option>';
  days_data.days.forEach(da => {
    const option = document.createElement("option");
    option.value = da.id;
    option.textContent = da.name;
    daysSelect.appendChild(option);
  });
}
window.onload = function() {
  loadSelection();
};


async function exportRegistration() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/reports/fee_report", {
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
  a.download = "fee_report_.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
