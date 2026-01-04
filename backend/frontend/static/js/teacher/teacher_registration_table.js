


async function loadSelection() {

  // == shift ==
  const response1 = await fetch(`/helper/get_shift`);
  const shiftData = await response1.json();

  const shiftSelect = document.getElementById("shift_id");
  shiftSelect.innerHTML = '<option value="">-Shift-</option>';
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
  departmentSelected.innerHTML = '<option value="">-Department-</option>';
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


async function deleteRegistration(
  teacher_id,
  department_id,
  contract_type_id,
  shift_id
) {
  const confirmed = confirm("Are you sure you want to delete this registration?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    teacher_id,
    department_id,
    contract_type_id,
    shift_id
  });

  const response = await fetch(`/teacher/delete_registration?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Registration deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Registration"}`);
  }
}


async function exportRegistration() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/teacher/export_registration", {
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
  a.download = "registration_export.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
