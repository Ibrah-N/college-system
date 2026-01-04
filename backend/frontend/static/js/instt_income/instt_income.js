async function loadSelection() {

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
