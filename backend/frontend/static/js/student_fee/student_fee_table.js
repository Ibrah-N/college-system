async function payFee(
  payment_id,
  student_id,
  department_id,
  course_id,
  class_code_id,
  semester_id,
  admission_type_id,
  shift_id
) {

    const params = new URLSearchParams({
    payment_id,
    student_id,
    department_id,
    course_id,
    class_code_id,
    semester_id,
    admission_type_id,
    shift_id
    });

    window.location.href = `/student_fee/pay_fee?${params.toString()}`;
}



