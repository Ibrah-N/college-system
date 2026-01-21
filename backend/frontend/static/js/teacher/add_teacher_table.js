async function deleteTeacher(teacher_id) {
    const confirmed = confirm("Are you sure you want to delete this teacher?");
    if (!confirmed) return;

    const response = await fetch(`/teacher/delete/${teacher_id}`, {
        method: "DELETE",
    });

    if (response.ok) {
        alert("Teacher Deleted Successfully");
        window.location.reload();
    } else {
        const err = await response.json();
        alert(`Error: ${err.message || "Failed To Delete Teacher"}`);
    }
}


async function updateTeacher(teacher_id) {
    window.location.href = `/teacher/update_stage_1/${teacher_id}`;
}
