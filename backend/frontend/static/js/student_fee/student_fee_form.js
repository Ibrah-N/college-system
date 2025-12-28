let payment_type_data_global = []; // store globally

window.onload = async function() {
    await loadSelection();
};

async function loadSelection() {
    const response = await fetch(`/helper/get_payment_type`);
    const data = await response.json();
    payment_type_data_global = data.payment_type;

    // Populate all existing selects on page load
    document.querySelectorAll('.payment_type').forEach(select => {
        populatePaymentType(select);
    });
}

function populatePaymentType(select) {
    select.innerHTML = ''; // clear previous options
    payment_type_data_global.forEach(p_type => {
        const option = document.createElement('option');
        option.value = p_type.id;
        option.textContent = p_type.name;
        select.appendChild(option);
    });
}

function addEntry() {
    const container = document.getElementById('fee-entries-container');

    const div = document.createElement('div');
    div.className = 'fee-entry';
    div.innerHTML = `
        <select name="fee_type[]" class="payment_type" required></select>
        <input type="number" name="paid_fee[]" placeholder="Paid Fee" required>
        <input type="number" name="discount[]" placeholder="Discount">
        <button type="button" class="remove-entry" onclick="removeEntry(this)">x</button>
    `;
    container.appendChild(div);

    // Populate the new select immediately
    populatePaymentType(div.querySelector('.payment_type'));
}

function removeEntry(button) {
    const container = document.getElementById('fee-entries-container');
    if (container.children.length > 1) {
        button.parentElement.remove();
    }
}


async function closeForm() {
    window.location.href = `/student_fee/list_fee`;
}

async function updateFee(payment_id) {
    window.location.href = `/student_fee/update_stage_1/${payment_id}`;
}


async function deleteFee(
  payment_id,
) {
  const confirmed = confirm("Are you sure you want to delete this fee record?");
  if (!confirmed) return;

  const params = new URLSearchParams({
    payment_id
  });

  const response = await fetch(`/student_fee/delete_fee?${params.toString()}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Fee Record deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete Fee record"}`);
  }
}