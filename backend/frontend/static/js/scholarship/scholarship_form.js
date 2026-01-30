async function loadSelection() {
  // == Course ==
  const response1 = await fetch(`/helper/get_courses_only`);
  const courseData = await response1.json();

  const courseSelect = document.getElementById("course_apply_for_id");
  courseSelect.innerHTML = '<option value="">-- Select Course --</option>';
  courseData.courses.forEach(sh => {
    const option = document.createElement("option");
    option.value = sh.id;
    option.textContent = sh.name;
    courseSelect.appendChild(option);
  });


  // == Tests Info ==
  const response2 = await fetch(`/helper/tests_info`);
  const testData = await response2.json();

  const testSelect = document.getElementById("test_info");
  testSelect.innerHTML = '<option value="">-- Select Test --</option>';
  testData.tests_info.forEach(ti => {
    const option = document.createElement("option");
    option.value = ti.id;
    option.textContent = ti.name;
    testSelect.appendChild(option);
  });

  // == Syllabus Info ==
  const response3 = await fetch(`/helper/syllabus_info`);
  const syllabus_infoData = await response3.json();

  const syllabusSelected = document.getElementById("syllabus");
  syllabusSelected.innerHTML = '<option value="">-- Select Syllabus --</option>';
  syllabus_infoData.syllabus_info.forEach(si => {
    const option = document.createElement("option");
    option.value = si.id;
    option.textContent = si.name;
    syllabusSelected.appendChild(option);
  });

}


window.onload = function() {
  loadSelection();
};



document.getElementById("scholarshipForm").addEventListener("submit", function(e) {
    // 1. Stop the form from sending immediately
    e.preventDefault();
    
    // 2. Clear previous error red lines/messages
    clearValidation();

    let isValid = true;

    // ==========================================
    // 1. SIMPLE TEXT FIELDS (Required)
    // ==========================================

    // Name
    isValid &= validateField(
        document.querySelector("input[name='name']"),
        val => val !== "",
        "Name is required"
    );

    // Father Name
    isValid &= validateField(
        document.querySelector("input[name='father_name']"),
        val => val !== "",
        "Father name is required"
    );

    // Qualification
    isValid &= validateField(
        document.querySelector("input[name='qualification']"),
        val => val !== "",
        "Qualification is required"
    );

    // Current Institute
    isValid &= validateField(
        document.querySelector("input[name='current_institute']"),
        val => val !== "",
        "Current Institute is required"
    );

    // Address
    isValid &= validateField(
        document.querySelector("input[name='address']"),
        val => val !== "",
        "Address is required"
    );

    // Course Applying For
    isValid &= validateField(
        document.querySelector("select[name='course_apply_for']"),
        val => val !== "",
        "Course name is required"
    );

    // Date
    isValid &= validateField(
        document.querySelector("input[name='registration_date']"),
        val => val !== "",
        "Registration Date is required"
    );


    // ==========================================
    // 2. COMPLEX PATTERN FIELDS
    // ==========================================

    // WhatsApp: 03xx-xxxxxxx (Dashes) OR 03xxxxxxxxx (No Dashes)
    isValid &= validateField(
        document.querySelector("input[name='whatsapp']"),
        val => {
            // Regex Breakdown:
            // ^03\d{2}-\d{7}$  -> Starts with 03, 2 digits, hyphen, 7 digits (Total 12)
            // ^03\d{9}$        -> Starts with 03, followed by 9 digits (Total 11)
            const withDash = /^03\d{2}-\d{7}$/; 
            const noDash   = /^03\d{9}$/;
            return withDash.test(val) || noDash.test(val);
        },
        "Invalid format. Use 03xx-xxxxxxx or 03xxxxxxxxx"
    );

    // CNIC: xxxxx-xxxxxxx-x (Dashes) OR xxxxxxxxxxxxx (No Dashes)
    isValid &= validateField(
        document.querySelector("input[name='cnic_formb']"),
        val => {
            // Regex Breakdown:
            // ^\d{5}-\d{7}-\d{1}$ -> Standard CNIC format (15 chars)
            // ^\d{13}$            -> Pure numbers (13 chars)
            const withDash = /^\d{5}-\d{7}-\d{1}$/;
            const noDash   = /^\d{13}$/;
            return withDash.test(val) || noDash.test(val);
        },
        "Invalid CNIC. Use xxxxx-xxxxxxx-x or 13 digits"
    );


    // ==========================================
    // 3. FILE & DROPDOWNS
    // ==========================================

    // Photo Upload (Check if file is selected)
    const photoInput = document.querySelector("input[name='photo']");
    isValid &= validateField(
        photoInput,
        () => photoInput.files.length > 0, // specific check for files
        "Please upload a photo"
    );

    // Select Test
    isValid &= validateField(
        document.querySelector("select[name='select_test']"),
        val => val !== "",
        "Please select a test"
    );

    // Select Syllabus
    isValid &= validateField(
        document.querySelector("select[name='select_syllabus']"),
        val => val !== "",
        "Please select a syllabus"
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