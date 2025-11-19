async function loadSelection() {
  // Get current date
  const today = new Date();
  const currentMonth = today.getMonth() + 1; // months are 0-based
  const currentDay = today.getDate();

  // == Session ==
  const response1 = await fetch(`/helper/get_sessions`);
  const session_data = await response1.json();

  const sessionSelect = document.getElementById("Session");
  sessionSelect.innerHTML = '<option value="">-- Select Session --</option>';
  session_data.sessions.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    sessionSelect.appendChild(option);
  });

  // Auto-select the current session (assuming session like 2025)
  const currentYear = today.getFullYear();
  const foundSession = session_data.sessions.find(s => s.name.includes(currentYear));
  if (foundSession) {
    sessionSelect.value = foundSession.id;
  }

  // == Month ==
  const response2 = await fetch(`/helper/get_months`);
  const month_data = await response2.json();

  const monthSelect = document.getElementById("Month");
  monthSelect.innerHTML = '<option value="">-- Select Month --</option>';
  month_data.months.forEach(m => {
    const option = document.createElement("option");
    option.value = m.id;
    option.textContent = m.name;
    monthSelect.appendChild(option);
  });

  // Auto-select current month
  monthSelect.value = currentMonth;

  // == Day ==
  const response3 = await fetch(`/helper/get_days`);
  const day_data = await response3.json();

  const daySelect = document.getElementById("Day");
  daySelect.innerHTML = '<option value="">-- Select Day --</option>';
  day_data.days.forEach(d => {
    const option = document.createElement("option");
    option.value = d.id;
    option.textContent = d.name;
    daySelect.appendChild(option);
  });

  // Auto-select current day
  daySelect.value = currentDay;


  // == shift ==
  const response5 = await fetch(`/helper/get_shift`);
  const shiftData = await response5.json();

  const shiftSelect = document.getElementById("shift");
  shiftSelect.innerHTML = '<option value="">-- Select Shift --</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });
}

window.onload = loadSelection;
