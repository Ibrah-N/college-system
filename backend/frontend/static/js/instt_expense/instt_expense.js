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


document.getElementById("insttExpenseForm").addEventListener("submit", function (e) {
    e.preventDefault();

    clearValidation();

    let isValid = true;

    isValid &= validateField(
        document.querySelector("input[name='amount']"),
        val => val !== "" && !isNaN(val) && Number(val) > 0,
        "Enter a valid amount"
    );

    isValid &= validateField(
        document.querySelector("select[name='shift_id']"),
        val => val !== "",
        "Please select a shift"
    );

    isValid &= validateField(
        document.querySelector("input[name='expense_by']"),
        val => val !== "",
        "Expense By is required"
    );

    isValid &= validateField(
        document.querySelector("input[name='item_details']"),
        val => val !== "",
        "Item details are required"
    );

    isValid &= validateField(
        document.querySelector("input[name='expense_for']"),
        val => val !== "",
        "Expense For is required"
    );

    if (isValid) {
        this.submit();
    }
});

/* ===== Helper functions ===== */

function validateField(element, conditionFn, message) {
    const value = element.value.trim();

    if (!conditionFn(value)) {
        element.classList.add("input-error");
        showError(element, message);
        return false;
    } else {
        element.classList.add("input-success");
        return true;
    }
}

function showError(element, message) {
    const error = document.createElement("div");
    error.className = "error-message";
    error.innerText = message;

    element.insertAdjacentElement("afterend", error);
}

function clearValidation() {
    document.querySelectorAll(".input-error, .input-success")
        .forEach(el => el.classList.remove("input-error", "input-success"));

    document.querySelectorAll(".error-message")
        .forEach(el => el.remove());
}
