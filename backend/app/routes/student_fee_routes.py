from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse, Response,
                                RedirectResponse, StreamingResponse)


from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal
from sqlalchemy import func, and_

from app.models.admission_orm import Student
from app.models.student_enrollment_orm import StudentEnrollment
from app.models.student_fee_orm import StudentFee
from app.models.student_fee_recipt_orm import StudentFeeRecipt
from app.models.helper_orm import (Shift, ClassCode, AdmissionType,
                                    Semester, Department, Course,
                                    PaymentType)
from weasyprint import HTML
from datetime import datetime
import base64


student_fee_router = APIRouter(prefix="/student_fee", tags=["Fee"])
templates = Jinja2Templates("frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================================#
#  L O A D - S T U D E N T S - F E E - F O R M   #
# ===============================================#
@student_fee_router.get("/pay_fee")
def fee_form(student_id: int, class_code_id: int,
        department_id: int, course_id: int, admission_type_id: int,
        semester_id: int, shift_id: int, request: Request, 
        db: Session = Depends(get_db)
    ):


    # === Extract Data From Form ===
    form_data = db.query(
    Student, StudentEnrollment, ClassCode,
    Department, Course, AdmissionType, Semester, Shift
    ).join(
        StudentEnrollment, Student.student_id == StudentEnrollment.student_id
    ).join(
        ClassCode, StudentEnrollment.class_code_id == ClassCode.class_code_id
    ).join(
        Department, StudentEnrollment.department_id == Department.department_id
    ).join(
        Course, StudentEnrollment.course_id == Course.course_id
    ).join(
        AdmissionType, StudentEnrollment.admission_type_id == AdmissionType.admission_type_id
    ).join(
        Semester, StudentEnrollment.semester_id == Semester.semester_id
    ).join(
        Shift, StudentEnrollment.shift_id == Shift.shift_id
    ).filter(
        StudentEnrollment.student_id == student_id,
        StudentEnrollment.class_code_id == class_code_id,
        StudentEnrollment.department_id == department_id,
        StudentEnrollment.course_id == course_id,
        StudentEnrollment.admission_type_id == admission_type_id,
        StudentEnrollment.semester_id == semester_id,
        StudentEnrollment.shift_id == shift_id
    ).first()
    form_info = {
        "student_id": form_data.StudentEnrollment.student_id,
        "student_name": form_data.Student.name,
        "father_name": form_data.Student.father_name,
        "department": form_data.Department.department_name,
        "department_id": form_data.Department.department_id,
        "course": form_data.Course.name,
        "course_id": form_data.Course.course_id,
        "shift": form_data.Shift.shift_name,
        "shift_id": form_data.Shift.shift_id,
        "class_code": form_data.ClassCode.class_code_name,
        "class_code_id": form_data.ClassCode.class_code_id,
        "admission_type": form_data.AdmissionType.admission_type,
        "admission_type_id": form_data.AdmissionType.admission_type_id,
        "semester": form_data.Semester.semester,
        "semester_id": form_data.Semester.semester_id,
        "fee": form_data.StudentEnrollment.fee
    }
    query_data = (
        db.query(
            Student, StudentFee, 
            Department, Course, Shift, ClassCode,
            AdmissionType, Semester, PaymentType
        )
        .select_from(StudentFee)
        .join(Student, Student.student_id == StudentFee.student_id)
        .join(Department, Department.department_id == StudentFee.department_id)
        .join(Course, Course.course_id == StudentFee.course_id)
        .join(Shift, Shift.shift_id == StudentFee.shift_id)
        .join(ClassCode, ClassCode.class_code_id == StudentFee.class_code_id)
        .join(AdmissionType, AdmissionType.admission_type_id == StudentFee.admission_type_id)
        .join(Semester, Semester.semester_id == StudentFee.semester_id)
        .join(PaymentType, PaymentType.payment_type_id == StudentFee.fee_type_id)
    )
    fee_list = query_data.filter(
        StudentFee.student_id == student_id,
        StudentFee.class_code_id == class_code_id,
        StudentFee.department_id == department_id,
        StudentFee.course_id == course_id,
        StudentFee.admission_type_id == admission_type_id,
        StudentFee.semester_id == semester_id,
        StudentFee.shift_id == shift_id
    ).order_by(StudentFee.payment_id).all()


    # -- if paid fee record found --
    fee_list_record = []
    if fee_list:
        for student, student_fee, department, course, shift, classcode, admissiontype, semester, payment_type in fee_list:
            fee_list_record.append({
                "payment_id": student_fee.payment_id,
                "student_name": student.name,
                "father_name": student.father_name,
                "department": department.department_name,
                "department_id": department.department_id,
                "course": course.name,
                "course_id": course.course_id,
                "shift": shift.shift_name,
                "shift_id": shift.shift_id,
                "class_code": classcode.class_code_name,
                "class_code_id": classcode.class_code_id,
                "admission_type": admissiontype.admission_type,
                "admission_type_id": admissiontype.admission_type_id,
                "semester": semester.semester,
                "semester_id": semester.semester_id,
                "fee_type": payment_type.payment_type_name,
                "paid": student_fee.paid,
                "discount": student_fee.discount,
                "date": student_fee.date
            })


    # -- if no record found --
    return templates.TemplateResponse(
        "pages/student_fee/student_fee_form.html",
        {
            "request": request, 
            "form_info": form_info,
            "fee_list_record": fee_list_record
        }
    )




# ============================================================
#       R E A D  -  S T U D E N T S - F E E                  #
# ============================================================
@student_fee_router.get("/list_fee")
def list_fee(request: Request, db: Session = Depends(get_db)):

    # -- extract record using joins --
    result = (
    db.query(
        StudentEnrollment.student_id,

        Student.name.label("student_name"),
        Student.father_name,

        Department.department_id,
        Department.department_name,

        Course.course_id,
        Course.name.label("course_name"),

        Shift.shift_id,
        Shift.shift_name,

        ClassCode.class_code_id,
        ClassCode.class_code_name,

        AdmissionType.admission_type_id,
        AdmissionType.admission_type,

        Semester.semester_id,
        Semester.semester,

        StudentEnrollment.fee,

        func.coalesce(func.sum(StudentFee.paid), 0).label("total_paid"),
        func.coalesce(func.sum(StudentFee.discount), 0).label("total_discount"),
    )
    .select_from(StudentEnrollment)   # BASE TABLE

    .join(Student, Student.student_id == StudentEnrollment.student_id)
    .join(Department, Department.department_id == StudentEnrollment.department_id)
    .join(Course, Course.course_id == StudentEnrollment.course_id)
    .join(Shift, Shift.shift_id == StudentEnrollment.shift_id)
    .join(ClassCode, ClassCode.class_code_id == StudentEnrollment.class_code_id)
    .join(AdmissionType, AdmissionType.admission_type_id == StudentEnrollment.admission_type_id)
    .join(Semester, Semester.semester_id == StudentEnrollment.semester_id)

    #  CORRECT LEFT JOIN (IMPORTANT)
    .outerjoin(
        StudentFee,
        and_(
            StudentFee.student_id == StudentEnrollment.student_id,
            StudentFee.department_id == StudentEnrollment.department_id,
            StudentFee.course_id == StudentEnrollment.course_id,
            StudentFee.class_code_id == StudentEnrollment.class_code_id,
            StudentFee.admission_type_id == StudentEnrollment.admission_type_id,
            StudentFee.semester_id == StudentEnrollment.semester_id,
            StudentFee.shift_id == StudentEnrollment.shift_id,
        )
    )
    .group_by(
        StudentEnrollment.student_id,
        Student.name,
        Student.father_name,
        Department.department_id,
        Department.department_name,
        Course.course_id,
        Course.name,
        Shift.shift_id,
        Shift.shift_name,
        ClassCode.class_code_id,
        ClassCode.class_code_name,
        AdmissionType.admission_type_id,
        AdmissionType.admission_type,
        Semester.semester_id,
        Semester.semester,
        StudentEnrollment.fee,
    )
    .order_by(StudentEnrollment.student_id)
    .all()
    )

    # -- jsonify record for fastapi responses --
    student_fee_records = []
    for student_id, student_name, father_name, \
        department_id, department_name, course_id, course_name, \
        shift_id, shift_name, class_code_id, class_code_name, admission_type_id, admission_type, semester_id, semester_name, \
        fee, total_paid, total_discount in result:

        student_fee_records.append({
            "student_id": student_id,
            "student_name": student_name,
            "father_name": father_name,
            "department_id": department_id,
            "department": department_name,
            "course_id": course_id,
            "course": course_name,
            "shift_id": shift_id,
            "shift": shift_name,
            "class_code_id": class_code_id,
            "class_code": class_code_name,
            "admission_type_id": admission_type_id,
            "admission_type": admission_type,
            "semester_id": semester_id,
            "fee": fee,
            "semester": semester_name,
            "paid_fee": total_paid,
            "discount": total_discount
        })


    # -- return response -- 
    return templates.TemplateResponse(
        "pages/student_fee/student_fee_table.html", 
        {
            "request": request,
            "studend_fee_records": student_fee_records
        }
    )




# ============================================================
#                A D D  -  S T U D E N T - F E E             #
# ============================================================
@student_fee_router.post("/add")
async def add_student_fee(
    request: Request,
    db: Session = Depends(get_db)
    ):

    form_data = await request.form()

    student_id = int(form_data.get("student_id"))
    department_id = int(form_data.get("department_id"))
    course_id = int(form_data.get("course_id"))
    class_code_id = int(form_data.get("class_code_id"))
    admission_type_id = int(form_data.get("admission_type_id"))
    semester_id = int(form_data.get("semester_id"))
    shift_id = int(form_data.get("shift_id"))
    course_fee = float(form_data.get("course_fee"))
    course_name = form_data.get("course")
    student_name = form_data.get("student_name")
    father_name = form_data.get("father_name")

    fee_types = form_data.getlist("fee_type[]")
    paid_fees = form_data.getlist("paid_fee[]")
    discounts = form_data.getlist("discount[]")
    fee_type_names = [db.query(PaymentType.payment_type_name).filter(PaymentType.payment_type_id == ft_id).scalar() for ft_id in fee_types]


    running_fee = 0.0 # summing the tution fee 
    running_discount = 0 # summing the tution discount
    for fee_type, paid_fee, discount in zip(fee_types, paid_fees, discounts):
        
        if int(fee_type) == 1: # Tuition Fee
            running_fee  += float(paid_fee)
            if discount != "":
                running_discount = running_discount + float(discount)
        
        # check negative fee
        if float(paid_fee) < 0:
            return JSONResponse(
                content = {
                    "message": f"Fee can't be negative; Entered Value {paid_fee}"
                }
            )

        # check negative discount
        if not discount == "":
            if float(discount) < 0:
                return JSONResponse(
                    content = {
                        "message": f"Discount can't be negative; Entered Value {discount}"
                    }
                )

    # check wheather fee entered exceeds the actuall fee 
    # for that particluer student enrollment of course
    # -- simple check --
    if (running_discount + running_fee) > course_fee:
        return JSONResponse(
            content = {
                "message": f"Total Fee and Discount Exceeds the Actual Fee of {course_fee}"
            }
        )
    # -- complex check --
    # - check whether this guy eneted anything before -
    total_paid_discount = (
        db.query(
            func.coalesce(func.sum(StudentFee.paid), 0).label("total_paid"),
            func.coalesce(func.sum(StudentFee.discount), 0).label("total_discount")
        )
        .filter(
            StudentFee.student_id == student_id,
            StudentFee.department_id == department_id,
            StudentFee.course_id == course_id,
            StudentFee.class_code_id == class_code_id,
            StudentFee.admission_type_id == admission_type_id,
            StudentFee.semester_id == semester_id,
            StudentFee.shift_id == shift_id, 
            StudentFee.fee_type_id == 1 # Tuition Fee Only
        )
        .all()
    )

    total_paid_fee = (total_paid_discount[0].total_paid + running_discount + 
                        running_fee + total_paid_discount[0].total_discount)
    if (total_paid_fee) > course_fee:
        return JSONResponse(
            content = {
                "message": f"Total Fee and Discount Exceeds the Actual Fee of {course_fee}. The Previously Paid Amount of Fee: {total_paid_discount[0].total_paid}; New Entered Amount: {running_fee + running_discount} which is greater then the actual fee: {total_paid_discount[0].total_paid + running_discount + running_fee + total_paid_discount[0].total_discount} > {course_fee}"
            }
        )

     # ====== FEE COMMIT ===========
    for fee_type_n, fee_type_id, paid_fee, discount in zip(fee_type_names, fee_types, paid_fees, discounts):
        student_fee = StudentFee(
            student_id=student_id,
            department_id=department_id,
            course_id=course_id,
            class_code_id=class_code_id,
            admission_type_id=admission_type_id,
            semester_id=semester_id,
            shift_id=shift_id,
            fee_type_id=fee_type_id,
            paid=float(paid_fee),
            discount=float(discount) if discount != "" else 0.0
        )
        db.add(student_fee)
    db.commit()
    # ====== RECIEPT COMMIT ===========
    recipt_id = db.query(func.coalesce(func.max(StudentFeeRecipt.recipt_id), 0) + 1).scalar()
    student_fee_recipt = StudentFeeRecipt(
        recipt_id = recipt_id,
        student_id = student_id,
        total_paid = total_paid_fee,
    )
    db.add(student_fee_recipt)
    db.commit()

    total_paid_fee = (total_paid_discount[0].total_paid + running_discount + 
                        running_fee + total_paid_discount[0].total_discount)
    # -- fee variables for recipt --
    prev_paid_fee = 0 # only tution fee
    prev_discount_on_fee = 0  # only tution fee
    current_amount = 0 # tution fee + extra fees
    current_discount = 0 # tution fee + extra fees 
    # (Prev.paid + Prev.Discount + Curr_tution_paid + Curr_tution_discount)
    total_course_fee_paid = 0 # only tution fees 
    remain_balance = 0 # simple (course_fee - total_course_fee_paid)

    # -- filling information
    prev_paid_fee = total_paid_discount[0].total_paid if total_paid_discount[0].total_paid >=0 else 0
    prev_discount_on_fee = total_paid_discount[0].total_discount if total_paid_discount[0].total_discount >=0 else 0
    current_amount = sum(float(pf) for pf in paid_fees)
    current_discount = sum(float(d) if d != "" else 0 for d in discounts)
    total_course_fee_paid = prev_paid_fee + prev_discount_on_fee + running_fee + running_discount
    remain_balance = course_fee - total_course_fee_paid


    # -- json for recipt --
    context = {
        "student_id": student_id,
        "reciept_id": recipt_id,
        "student_name": student_name,
        "father_name": father_name,
        "course": course_name,
        "current_date": datetime.now().strftime("%d %b %Y %I:%M %p"),
        "fee_rows": [
            {"fee_type": ft, "paid": pf, "discount": d or 0}
            for ft, pf, d in zip(fee_type_names, paid_fees, discounts)
        ],
        "prev_paid_fee": prev_paid_fee,
        "prev_discount_on_fee": prev_discount_on_fee,
        "current_amount": current_amount,
        "current_discount": current_discount,
        "course_fee": course_fee,
        "total_course_fee_paid": total_course_fee_paid,
        "remain_balance": remain_balance
    }


    html = templates.get_template("pages/student_fee/fee_recipt.html").render(context)
    pdf = HTML(string=html).write_pdf()
    link = f"/student_fee/pay_fee?payment_id=&student_id={student_id}&department_id={department_id}&course_id={course_id}&class_code_id={class_code_id}&semester_id={semester_id}&admission_type_id={admission_type_id}&shift_id={shift_id}"
    pdf_base64 = base64.b64encode(pdf).decode()
    html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0">
        <iframe src="data:application/pdf;base64,{pdf_base64}"
                style="width:100vw;height:100vh;border:none">
        </iframe>

        <script>
            setTimeout(() => {{
                window.location.href = "{link}";
            }}, 2000000);
        </script>
        </body>
        </html>
        """
    # return RedirectResponse(
    #     url = link,
    #     status_code=303
    # )
    return HTMLResponse(html)



# ===============================================
#      U P D A T E -  S T U D E N T - F E E     #
# ===============================================
@student_fee_router.get("/update_stage_1/{payment_id}", response_class=HTMLResponse)
async def update_stage_1_fee(request: Request, payment_id: int, db: Session = Depends(get_db)):
    payment_old = db.query(StudentFee).filter(StudentFee.payment_id == payment_id).first()

    if not payment_old:
        return JSONResponse(content={"message": f"Student Payment with ID {payment_id} not found !!!"}, status_code=404)

    # -- load the data to update form --
    return templates.TemplateResponse(
        "pages/student_fee/update_student_fee.html",
        {
            "request": request, 
            "payment_old": payment_old
        }
    )


@student_fee_router.post("/update_student_fee")
async def update_student_fee(request: Request, db: Session = Depends(get_db)):
    
    # -- recieve form data --
    form_data = await request.form()
    payment_id = int(form_data.get("payment_id"))
    paid_fee = float(form_data.get("fee")) if form_data.get("fee") != '' else 0.0
    discount = float(form_data.get("discount")) if form_data.get("discount") != '' else 0.0
    print("from_data", form_data)

    # # # -- find existing student --
    payment = db.query(StudentFee).filter(StudentFee.payment_id == payment_id).first()
    if not payment:
        return JSONResponse(content={"message": "Payment not found"}, status_code=404)


    # check nothing when entered
    if form_data.get("fee") == '':
        return JSONResponse(
            content = {
                "message": f"Fee can't be zero; Entered Value {paid_fee}"
            }
        )

    # check negative fee
    if paid_fee < 0:
        return JSONResponse(
            content = {
                "message": f"Fee can't be negative; Entered Value {paid_fee}"
            }
        )

    # # check negative discount
    if float(discount) < 0:
        return JSONResponse(
            content = {
                "message": f"Discount can't be negative; Entered Value {discount}"
            }
        )
    
    # check wheather fee entered exceeds the actuall fee 
    # for that particluer student enrollment of course
    # -- simple check --
    # if (paid_fee + discount) > course_fee:
    #     return JSONResponse(
    #         content = {
    #             "message": f"Total Fee and Discount Exceeds the Actual Fee of {course_fee}"
    #         }
    #     )
    # # -- complex check --
    # # - check whether this guy eneted anything before -
    # total_paid_discount = (
    #     db.query(
    #         func.coalesce(func.sum(StudentFee.paid), 0).label("total_paid"),
    #         func.coalesce(func.sum(StudentFee.discount), 0).label("total_discount")
    #     )
    #     .filter(
    #         StudentFee.student_id == student_id,
    #         StudentFee.department_id == department_id,
    #         StudentFee.course_id == course_id,
    #         StudentFee.class_code_id == class_code_id,
    #         StudentFee.admission_type_id == admission_type_id,
    #         StudentFee.semester_id == semester_id,
    #         StudentFee.shift_id == shift_id, 
    #         StudentFee.fee_type_id == 1 # Tuition Fee Only
    #     )
    #     .all()
    # )
    # print("running fee", running_fee)
    # print("total", total_paid_discount[0].total_paid + running_discount + 
    #     running_fee + total_paid_discount[0].total_discount)

    # if (total_paid_discount[0].total_paid + running_discount + 
    #     running_fee + total_paid_discount[0].total_discount) > course_fee:
    #     return JSONResponse(
    #         content = {
    #             "message": f"Total Fee and Discount Exceeds the Actual Fee of {course_fee}. The Previously Paid Amount of Fee: {total_paid_discount[0].total_paid}; New Entered Amount: {running_fee + running_discount} which is greater then the actual fee: {total_paid_discount[0].total_paid + running_discount + running_fee + total_paid_discount[0].total_discount} > {course_fee}"
    #         }
    #     )

    # -- update student --
    payment.paid = paid_fee
    payment.discount = discount
    db.commit()


    link = f'/student_fee/pay_fee?payment_id=&student_id={form_data.get("student_id")}&department_id={form_data.get("department_id")}&course_id={form_data.get("course_id")}&class_code_id={form_data.get("class_code_id")}&semester_id={form_data.get("semester_id")}&admission_type_id={form_data.get("admission_type_id")}&shift_id={form_data.get("shift_id")}'
    return RedirectResponse(
        url = link,
        status_code=303
    )




# ============================================================
#          D E L E T E  -  S T U D E N T - F E E             #
# ============================================================
@student_fee_router.delete("/delete_fee/")
async def delete_student_fee(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(StudentFee).filter(StudentFee.payment_id == payment_id).first()

    print()
    if not payment:
        return JSONResponse(content={"message": "Payment not found"}, status_code=404)

    db.delete(payment)
    db.commit()
    return RedirectResponse(url="/student_fee/list_fee", status_code=303)



# ============================================================
#     S E A R C H -  S T U D E N T - F E E - R E C O R D     #
# ============================================================
@student_fee_router.post("/search_student_fee")
async def search_student_fee(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    if not form_data.get("id_search") and not form_data.get("name_search"):
        return RedirectResponse(
            "/student_fee/list_fee", 
            status_code=303
        )


    student_fee_data = []
    query_ = (
    db.query(
        StudentEnrollment.student_id,

        Student.name.label("student_name"),
        Student.father_name,

        Department.department_id,
        Department.department_name,

        Course.course_id,
        Course.name.label("course_name"),

        Shift.shift_id,
        Shift.shift_name,

        ClassCode.class_code_id,
        ClassCode.class_code_name,

        AdmissionType.admission_type_id,
        AdmissionType.admission_type,

        Semester.semester_id,
        Semester.semester,

        StudentEnrollment.fee,

        func.coalesce(func.sum(StudentFee.paid), 0).label("total_paid"),
        func.coalesce(func.sum(StudentFee.discount), 0).label("total_discount"),
    )
    .select_from(StudentEnrollment)   # BASE TABLE
    .join(Student, Student.student_id == StudentEnrollment.student_id)
    .join(Department, Department.department_id == StudentEnrollment.department_id)
    .join(Course, Course.course_id == StudentEnrollment.course_id)
    .join(Shift, Shift.shift_id == StudentEnrollment.shift_id)
    .join(ClassCode, ClassCode.class_code_id == StudentEnrollment.class_code_id)
    .join(AdmissionType, AdmissionType.admission_type_id == StudentEnrollment.admission_type_id)
    .join(Semester, Semester.semester_id == StudentEnrollment.semester_id)

    #  CORRECT LEFT JOIN (IMPORTANT)
    .outerjoin(
        StudentFee,
        and_(
            StudentFee.student_id == StudentEnrollment.student_id,
            StudentFee.department_id == StudentEnrollment.department_id,
            StudentFee.course_id == StudentEnrollment.course_id,
            StudentFee.class_code_id == StudentEnrollment.class_code_id,
            StudentFee.admission_type_id == StudentEnrollment.admission_type_id,
            StudentFee.semester_id == StudentEnrollment.semester_id,
            StudentFee.shift_id == StudentEnrollment.shift_id,
        )
    )
    .group_by(
        StudentEnrollment.student_id,
        Student.name,
        Student.father_name,
        Department.department_id,
        Department.department_name,
        Course.course_id,
        Course.name,
        Shift.shift_id,
        Shift.shift_name,
        ClassCode.class_code_id,
        ClassCode.class_code_name,
        AdmissionType.admission_type_id,
        AdmissionType.admission_type,
        Semester.semester_id,
        Semester.semester,
        StudentEnrollment.fee,
    )
    )
    # -- search filters --
    # if id-search enabled it will only search
    # on the basis of id else it will look for 
    # all other filter combinaly
    if form_data.get("id_search"):
        result = query_.filter(
            StudentEnrollment.student_id == int(form_data.get("id_search")),
        ).order_by(StudentEnrollment.student_id).all()

        # -- jsonify record for fastapi responses --
        student_fee_records = []
        for student_id, student_name, father_name, \
            department_id, department_name, course_id, course_name, \
            shift_id, shift_name, class_code_id, class_code_name, admission_type_id, admission_type, semester_id, semester_name, \
            fee, total_paid, total_discount in result:

            student_fee_records.append({
                "student_id": student_id,
                "student_name": student_name,
                "father_name": father_name,
                "department_id": department_id,
                "department": department_name,
                "course_id": course_id,
                "course": course_name,
                "shift_id": shift_id,
                "shift": shift_name,
                "class_code_id": class_code_id,
                "class_code": class_code_name,
                "admission_type_id": admission_type_id,
                "admission_type": admission_type,
                "semester_id": semester_id,
                "fee": fee,
                "semester": semester_name,
                "paid_fee": total_paid,
                "discount": total_discount
            })


        # -- return response -- 
        return templates.TemplateResponse(
            "pages/student_fee/student_fee_table.html", 
            {
                "request": request,
                "studend_fee_records": student_fee_records
            }
        )


    # -- ofther fileters --
    if form_data.get("name_search"):
        query = query_.filter(Student.name.ilike(f"%{form_data.get('name_search')}%"))
    # if form_data.get("class_code_id"):
    #     query = query.filter(StudentEnrollment.class_code_id==int(form_data.get("class_code_id")))
    # if form_data.get("department_id"):
    #     query = query.filter(StudentEnrollment.department_id==int(form_data.get("department_id")))
    # if form_data.get(("course_id")):
    #     query = query.filter(StudentEnrollment.course_id==int(form_data.get("course_id")))
    # if form_data.get("admission_type_id"):
    #     query = query.filter(StudentEnrollment.admission_type_id==int(form_data.get("admission_type_id")))
    # if form_data.get("semester_id"):
    #     query = query.filter(StudentEnrollment.semester_id==int(form_data.get("semester_id")))
    # if form_data.get("shift_id"):
    #     query = query.filter(StudentEnrollment.shift_id==int(form_data.get("shift_id")))
    query = query.order_by(StudentEnrollment.student_id)
    result = query.all()

    
    # -- jsonify record for fastapi responses --
    student_fee_records = []
    for student_id, student_name, father_name, \
        department_id, department_name, course_id, course_name, \
        shift_id, shift_name, class_code_id, class_code_name, admission_type_id, admission_type, semester_id, semester_name, \
        fee, total_paid, total_discount in result:

        student_fee_records.append({
            "student_id": student_id,
            "student_name": student_name,
            "father_name": father_name,
            "department_id": department_id,
            "department": department_name,
            "course_id": course_id,
            "course": course_name,
            "shift_id": shift_id,
            "shift": shift_name,
            "class_code_id": class_code_id,
            "class_code": class_code_name,
            "admission_type_id": admission_type_id,
            "admission_type": admission_type,
            "semester_id": semester_id,
            "fee": fee,
            "semester": semester_name,
            "paid_fee": total_paid,
            "discount": total_discount
        })


    # -- return response -- 
    return templates.TemplateResponse(
        "pages/student_fee/student_fee_table.html", 
        {
            "request": request,
            "studend_fee_records": student_fee_records
        }
    )



# ============================================================
#            L I S T - F E E - R E C I P T                   #
# ============================================================
@student_fee_router.get("/fee_recipt_list", response_class=HTMLResponse)
async def fee_recipt_list(request: Request, db: Session = Depends(get_db)):
    recipt_list = (
        db.query(StudentFeeRecipt, Student.name, Student.father_name)
        .join(Student, Student.student_id == StudentFeeRecipt.student_id)
        .order_by(StudentFeeRecipt.recipt_id)
        .all()
    )

    recipt_records = []
    for recipt, student_name, father_name in recipt_list:
        recipt_records.append({
            "recipt_id": recipt.recipt_id,
            "student_name": student_name,
            "father_name": father_name,
            "date": recipt.date.strftime("%d %b %Y %I:%M %p"),
            "total_paid": recipt.total_paid
        })

    return templates.TemplateResponse(
        "pages/student_fee/fee_recipt_table.html",
        {
            "request": request,
            "recipt_records": recipt_records
        }
    )


# ============================================================
#      S E A R C H  -  F E E - R E C I P T                   #
# ============================================================
@student_fee_router.post("/search_fee_recipt", response_class=HTMLResponse)
async def fee_recipt(request: Request, 
                    db: Session = Depends(get_db)
                    ):
    form_data = await request.form()
    recipt_id = form_data.get("id_search")

    if recipt_id == "":
        return RedirectResponse(
            "/student_fee/fee_recipt_list",
            status_code=303
        )
    rrecipt_list = (
        db.query(StudentFeeRecipt, Student.name, Student.father_name)
        .join(Student, Student.student_id == StudentFeeRecipt.student_id)
        .filter(StudentFeeRecipt.recipt_id == recipt_id)
        .order_by(StudentFeeRecipt.recipt_id)
        .all()
    )

    recipt_records = []
    for recipt, student_name, father_name in rrecipt_list:
        recipt_records.append({
            "recipt_id": recipt.recipt_id,
            "student_name": student_name,
            "father_name": father_name,
            "date": recipt.date.strftime("%d %b %Y %I:%M %p"),
            "total_paid": recipt.total_paid
        })

    return templates.TemplateResponse(
        "pages/student_fee/fee_recipt_table.html",
        {
            "request": request,
            "recipt_records": recipt_records
        }
    )