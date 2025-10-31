async function deleteStudent(student_id) {
    const confirmed = confirm("Are you sure you want to delete this student?");
    if (!confirmed) return;

    const response = await fetch(`/student/delete/${student_id}`, {
        method: "DELETE",
    });

    if (response.ok) {
        alert("Student Deleted Successfully");
        window.location.reload();
    } else {
        const err = await response.json();
        alert(`Error: ${err.message || "Failed to delete student"}`);
    }
}

async function updateStudent(student_id) {
    const response = await fetch(`/student/update_stage_1/${student_id}`, {
        method: "POST",
    });
}