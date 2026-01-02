async function paySalary(
  teacher_id,
  department_id,
  course_id,
  shift_id
) {

    const params = new URLSearchParams({
    teacher_id,
    department_id,
    course_id,
    shift_id
    });

    window.location.href = `/salary/pay_salary?${params.toString()}`;
}



