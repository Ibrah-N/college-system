async function loadSelection() {

  // == shift ==
  const response1 = await fetch(`/helper/get_shift`);
  const shiftData = await response1.json();

  const shiftSelect = document.getElementById("shift_id");
  shiftSelect.innerHTML = '<option value="">-- Select Shift --</option>';
  shiftData.shift.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    shiftSelect.appendChild(option);
  });


      // == department ==
  const response = await fetch(`/helper/get_department`);
  const departmentData = await response.json();

  const departmentSelected = document.getElementById("department_id");
  departmentSelected.innerHTML = '<option value="">-- Select Dept --</option>';
  departmentData.departments.forEach(dp => {
    const option = document.createElement("option");
    option.value = dp.id;
    option.textContent = dp.department;
    departmentSelected.appendChild(option);
  });


  // == Contract type ==
  const response2 = await fetch(`/helper/get_contract_type`);
  const contractData = await response2.json();

  const contractSelected = document.getElementById("contract_type_id");
  contractSelected.innerHTML = '<option value="">-- Select Contract --</option>';
  contractData.contract_type.forEach(ct => {
    const option = document.createElement("option");
    option.value = ct.id;
    option.textContent = ct.name;
    contractSelected.appendChild(option);
  });

}


window.onload = function() {
  loadSelection();
};