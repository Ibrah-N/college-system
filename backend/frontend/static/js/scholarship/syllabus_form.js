

document.getElementById("scholarshipForm").addEventListener("submit", function(e) {
    // 1. Stop the form from sending immediately
    e.preventDefault();
    
    // 2. Clear previous error red lines/messages
    clearValidation();

    let isValid = true;

    // ==========================================
    // 1. SIMPLE TEXT FIELDS (Required)
    // ==========================================

    // Chemistry MCQs
    isValid &= validateField(
        document.querySelector("input[name='chemistry_mcqs']"),
        val => val !== "",
        "ChSubject & MCQs is required; format: Sub - #mcqs"
    );

    // Physics MCQs
    isValid &= validateField(
        document.querySelector("input[name='physics_mcqs']"),
        val => val !== "",
        "Subject & MCQs is required; format: Sub - #mcqs"
    );

    // English MCQs
    isValid &= validateField(
        document.querySelector("input[name='english_mcqs']"),
        val => val !== "",
        "Subject & MCQs is required; format: Sub - #mcqs"
    );

    // General MCQs
    isValid &= validateField(
        document.querySelector("input[name='general_mcqs']"),
        val => val !== "",
        "Subject & MCQs is required; format: Sub - #mcqs"
    );


    // ==========================================
    // 4. FINAL DECISION
    // ==========================================
    if (isValid) {
        this.submit(); // Send data to Python/FastAPI
    } else {
        // Optional: Scroll to top if errors exist
        document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
    }
});


/* ==========================================
   HELPER FUNCTIONS (Reusable)
   ========================================== */

function validateField(element, conditionFn, message) {
    if (!element) return true; // Safety check if element doesn't exist

    // Handle file input value differently than text
    let value = element.value ? element.value.trim() : "";
    
    // If it's a file input, we don't trim the value, logic is handled in the conditionFn above
    
    // Check the condition
    if (!conditionFn(value)) {
        element.classList.add("input-error");
        showError(element, message);
        return false; // Invalid
    } else {
        element.classList.add("input-success");
        return true; // Valid
    }
}

function showError(element, message) {
    // Create the error text divf
    const error = document.createElement("div");
    error.className = "error-message";
    error.innerText = message;
    
    // Find the parent .form-row to append the message correctly
    // This ensures the error appears Under the input, not inside it
    const parentRow = element.closest('.form-row');
    if (parentRow) {
        // Insert after the whole row or inside it? 
        // Based on your CSS, inside the .form-row might break flex layout.
        // Let's append it specifically after the INPUT inside the parent
        element.insertAdjacentElement("afterend", error);
    }
}

function clearValidation() {
    // Remove red/green borders
    document.querySelectorAll(".input-error, .input-success")
        .forEach(el => el.classList.remove("input-error", "input-success"));

    // Remove text messages
    document.querySelectorAll(".error-message")
        .forEach(el => el.remove());
}