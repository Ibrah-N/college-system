from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse, JSONResponse, Response,
                                RedirectResponse, StreamingResponse)

from sqlalchemy.orm import Session 
from app.config.db_connect import SessionLocal
from sqlalchemy import func, and_




from app.models.teacher_payment_orm import TeacherPayment
from app.models.add_teacher_orm import AddTeacher
from app.models.teacher_registration_orm import TeacherRegesitration
from app.models.helper_orm import (Department, ContractType, Shift,
                                    Semester, SalaryType)

from weasyprint import HTML
from datetime import datetime
import base64

teacher_salary_router = APIRouter(prefix="/salary", tags=["SALARY"])
templates = Jinja2Templates("frontend")


# -- connect db --
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# =================================================== =#
#  L O A D - T E A C H E R - S A L A R Y - F O R M     #
# =====================================================#
@teacher_salary_router.get("/pay_salary")
def fee_form(teacher_id: int, department_id: int, 
            contract_type_id: int, shift_id: int,
            request: Request, db: Session = Depends(get_db)
    ):


    # === Extract Data For Form ===
    form_data = db.query(
    AddTeacher, TeacherRegesitration,
    Department, ContractType, Shift
    ).join(
        TeacherRegesitration, AddTeacher.teacher_id == TeacherRegesitration.teacher_id
    ).join(
        Department, TeacherRegesitration.department_id == Department.department_id
    ).join(
        ContractType, TeacherRegesitration.contract_type_id == ContractType.contract_type_id
    ).join(
        Shift, TeacherRegesitration.shift_id == Shift.shift_id
    ).filter(
        TeacherRegesitration.teacher_id == teacher_id,
        TeacherRegesitration.department_id == department_id,
        TeacherRegesitration.contract_type_id == contract_type_id,
        TeacherRegesitration.shift_id == shift_id
    ).first()
    form_info = {
        "teacher_id": form_data.TeacherRegesitration.teacher_id,
        "teacher_name": form_data.AddTeacher.name,
        "father_name": form_data.AddTeacher.father_name,
        "department_name": form_data.Department.department_name,
        "department_id": form_data.Department.department_id,
        "contract_type": form_data.ContractType.contract_type_name,
        "contract_type_id": form_data.ContractType.contract_type_id,
        "shift": form_data.Shift.shift_name,
        "shift_id": form_data.Shift.shift_id,
        "salary": form_data.TeacherRegesitration.salary
    }
    
    # == Extraction of Data for Table ==
    query_data = (
        db.query(
            AddTeacher, TeacherPayment, TeacherRegesitration,
            Department, ContractType, Shift, SalaryType
        )
        .select_from(TeacherPayment)
        .join(AddTeacher, AddTeacher.teacher_id == TeacherPayment.teacher_id)
        .join(TeacherRegesitration, TeacherRegesitration.teacher_id == TeacherPayment.teacher_id)
        .join(Department, Department.department_id == TeacherPayment.department_id)
        .join(ContractType, ContractType.contract_type_id == TeacherPayment.contract_type_id)
        .join(Shift, Shift.shift_id == TeacherPayment.shift_id)
        .join(SalaryType, SalaryType.salary_type_id == TeacherPayment.salary_type_id)
    )
    salary_list = query_data.filter(
        TeacherPayment.teacher_id == teacher_id,
        TeacherPayment.department_id == department_id,
        TeacherPayment.contract_type_id == contract_type_id,
        TeacherPayment.shift_id == shift_id
    ).all()


    # -- if paid salary record found --
    salary_list_record = []
    if salary_list:
        for add_teacher, teacher_payment, teacher_registration, department, contract_type, shift, salary_type in salary_list:
            salary_list_record.append({
                "payment_id": teacher_payment.payment_id,
                "teacher_name": add_teacher.name,
                "father_name": add_teacher.father_name,
                "department": department.department_name,
                "department_id": department.department_id,
                "contract_type": contract_type.contract_type_name,
                "contract_type_id": contract_type.contract_type_id,
                "shift": shift.shift_name,
                "shift_id": shift.shift_id,
                "salary_type": salary_type.salary_type_name,
                "salary": teacher_registration.salary,
                "paid": teacher_payment.paid_salary,
                "deduction": teacher_payment.deduction,
                "date": teacher_payment.date
            })


    # -- if no record found --
    return templates.TemplateResponse(
        "pages/teacher_salary/teacher_salary_form.html",
        {
            "request": request, 
            "form_info": form_info,
            "salary_list_record": salary_list_record
        }
    )





# ============================================================
#       R E A D  -  T E A C H E R - S A L A R Y              #
# ============================================================
@teacher_salary_router.get("/list_salary")
def list_salary(request: Request, db: Session = Depends(get_db)):
        # -- extract record using joins --
    result = (
    db.query(
        TeacherRegesitration.teacher_id,

        AddTeacher.name.label("teacher_name"),
        AddTeacher.father_name,

        Department.department_id,
        Department.department_name,

        ContractType.contract_type_id,
        ContractType.contract_type_name,

        Shift.shift_id,
        Shift.shift_name,

        TeacherRegesitration.salary,

        func.coalesce(func.sum(TeacherPayment.paid_salary), 0).label("paid_salary"),
        func.coalesce(func.sum(TeacherPayment.deduction), 0).label("deduction"),
    )
    .select_from(TeacherRegesitration)   # BASE TABLE

    .join(AddTeacher, AddTeacher.teacher_id == TeacherRegesitration.teacher_id)
    .join(Department, Department.department_id == TeacherRegesitration.department_id)
    .join(ContractType, ContractType.contract_type_id == TeacherRegesitration.contract_type_id)
    .join(Shift, Shift.shift_id == TeacherRegesitration.shift_id)

    #  CORRECT LEFT JOIN (IMPORTANT)
    .outerjoin(
        TeacherPayment,
        and_(
            TeacherPayment.teacher_id == TeacherRegesitration.teacher_id,
            TeacherPayment.department_id == TeacherRegesitration.department_id,
            TeacherPayment.contract_type_id == TeacherRegesitration.contract_type_id,
            TeacherPayment.shift_id == TeacherRegesitration.shift_id,
        )
    )
    .group_by(
        TeacherRegesitration.teacher_id,
        AddTeacher.name,
        AddTeacher.father_name,
        Department.department_id,
        Department.department_name,
        ContractType.contract_type_id,
        ContractType.contract_type_name,
        Shift.shift_id,
        Shift.shift_name,
        TeacherRegesitration.salary,
    )
    .all()
    )


        # -- jsonify record for fastapi responses --
    teacher_salary_record = []
    for teacher_id, teacher_name, father_name, \
        department_id, department_name, contract_type_id, contract_type_name, \
        shift_id, shift_name, \
        salary, paid_salary, deduction in result:

        teacher_salary_record.append({
            "teacher_id": teacher_id,
            "teacher_name": teacher_name,
            "father_name": father_name,
            "department_id": department_id,
            "department": department_name,
            "contract_type_id": contract_type_id,
            "contract_type": contract_type_name,
            "shift_id": shift_id,
            "shift": shift_name,
            "salary": salary,
            "paid_salary": paid_salary,
            "deduction": deduction
        })

    
    return templates.TemplateResponse(
        "pages/teacher_salary/teacher_salary_table.html",
        {
            "request": request,
            "teacher_salary_record": teacher_salary_record
        }
    )



# ============================================================
#          A D D  -  T E A C H E R - S A L A R Y             #
# ============================================================
@teacher_salary_router.post("/add_salary")
async def add_teacher_salary(
    request: Request,
    db: Session = Depends(get_db)
    ):

    form_data = await request.form()

    teacher_id = int(form_data.get("teacher_id"))
    department_id = int(form_data.get("department_id"))
    contract_type_id = int(form_data.get("contract_type_id"))
    shift_id = int(form_data.get("shift_id"))
    department_name = form_data.get("department_name")
    teacher_name = form_data.get("teacher_name")
    father_name = form_data.get("father_name")
    teacher_salary = float(form_data.get("salary"))

    salary_types = form_data.getlist("salary_types[]")
    paid_salaries = form_data.getlist("paid_salaries[]")
    deductions = form_data.getlist("deductions[]")
    salary_type_names = [db.query(SalaryType.salary_type_name).filter(SalaryType.salary_type_id == st_id).scalar() for st_id in salary_types]
    contract_type_name = db.query(ContractType.contract_type_name).filter(ContractType.contract_type_id == contract_type_id).scalar()

    running_salary = 0.0 # summing the running salary
    running_deduction = 0 # summing the running deduction
    for salary_type, paid_salary, deduction in zip(salary_types, paid_salaries, deductions):
        
        # -- running sum (salary & deduction)
        if int(salary_type) == 1: # Actual Salary Only
            running_salary  += float(paid_salary)
            if deduction != "":
                running_deduction = running_deduction + float(deduction)
        
        # check negative salary
        if float(paid_salary) < 0:
            return JSONResponse(
                content = {
                    "message": f"Salary can't be negative; Entered Value {paid_salary}"
                }
            )

        # check negative deduction
        if not deduction == "":
            if float(deduction) < 0:
                return JSONResponse(
                    content = {
                        "message": f"Salary Deduction can't be negative; Entered Value {deduction}"
                    }
                )

    # check wheather salary entered exceeds the actuall salary 
    # for that particluer teacher registration of teacher 
    # -- simple check --
    print("Running Salary {}  -  Running Deduction {}  -  Teacher Salary {}"
          .format(running_salary, running_deduction, teacher_salary))
    if (running_salary + running_deduction) > teacher_salary:
        return JSONResponse(
            content = {
                "message": f"Total Salary and Deduction Exceeds the Actual Fee of {teacher_salary}"
            }
        )
    # -- complex check --
    # - check whether this guy eneted anything before -
    total_paid_discount = (
        db.query(
            func.coalesce(func.sum(TeacherPayment.paid_salary), 0).label("total_paid"),
            func.coalesce(func.sum(TeacherPayment.deduction), 0).label("total_deduction")
        )
        .filter(
            TeacherPayment.teacher_id == teacher_id,
            TeacherPayment.department_id == department_id,
            TeacherPayment.contract_type_id == contract_type_id,
            TeacherPayment.shift_id == shift_id, 
            TeacherPayment.salary_type_id == 1 # Salary Only
        )
        .all()
    )

    total_paid_salary = (total_paid_discount[0].total_paid + running_deduction + 
                        running_salary + total_paid_discount[0].total_deduction)
    if (total_paid_salary) > teacher_salary:
        return JSONResponse(
            content = {
                "message": f"Total Salary and Deduction Exceeds the Actual Salary of {teacher_salary}. The Previously Paid Amount of Salary: {total_paid_discount[0].total_paid}; New Entered Amount: {running_salary + running_deduction} which is greater then the actual Salary: {total_paid_discount[0].total_paid + running_deduction + running_salary + total_paid_discount[0].total_deduction} > {teacher_salary}"
            }
        )

    
    for salary_type_id, paid_salary, deduction in zip(salary_types, paid_salaries, deductions):
        print(salary_type_id, paid_salary, deduction)
        teacher_salary_instant = TeacherPayment(
            teacher_id=teacher_id,
            department_id=department_id,
            contract_type_id=contract_type_id,
            shift_id=shift_id,
            salary_type_id=salary_type_id,
            paid_salary=float(paid_salary),
            deduction=float(deduction) if deduction != "" else 0.0
        )
        db.add(teacher_salary_instant)
    db.commit()

    total_paid_salary = (total_paid_discount[0].total_paid + running_deduction + 
                        running_salary + total_paid_discount[0].total_deduction)
    # -- fee variables for recipt --
    prev_paid_salary = 0 # only salary_fee
    prev_deduction_on_salary = 0  # only tution fee
    current_amount = 0 # tution fee + extra fees
    current_deduction = 0 # tution fee + extra fees 
    # (Prev.paid + Prev.Discount + Curr_tution_paid + Curr_tution_discount)
    total_salary_paid = 0 # only tution fees 
    remain_balance = 0 # simple (course_fee - total_course_fee_paid)

    # -- filling information
    prev_paid_salary = total_paid_discount[0].total_paid if total_paid_discount[0].total_paid >=0 else 0
    prev_deduction_on_salary = total_paid_discount[0].total_deduction if total_paid_discount[0].total_deduction >=0 else 0
    current_amount = sum(float(pf) for pf in paid_salaries)
    current_discount = sum(float(d) if d != "" else 0 for d in deductions)
    total_salary_paid = prev_paid_salary + prev_deduction_on_salary + running_salary + running_deduction
    remain_balance = teacher_salary - total_salary_paid


    # -- json for recipt --
    context = {
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "father_name": father_name,
        "department_name": department_name,
        "contract_type": contract_type_name,
        "current_date": datetime.now().strftime("%d %b %Y %I:%M %p"),
        "salary_rows": [
            {"salary_type": ft, "paid": pf, "deduction": d or 0}
            for ft, pf, d in zip(salary_type_names, paid_salaries, deductions)
        ],
        "prev_paid_salary": prev_paid_salary,
        "prev_deduction_on_salary": prev_deduction_on_salary,
        "current_amount": current_amount,
        "current_deduction": current_deduction,
        "teacher_salary": teacher_salary,
        "total_salary_paid": total_salary_paid,
        "remain_balance": remain_balance
    }


    html = templates.get_template("pages/teacher_salary/teacher_recipt.html").render(context)
    pdf = HTML(string=html).write_pdf()

    # return Response(
    #     content=pdf,
    #     media_type="application/pdf",
    #     headers={
    #         "Content-Disposition": f"inline; filename={teacher_name}_recipt.pdf"
    #     }
    # )

    link = f"/salary/pay_salary?teacher_id={teacher_id}&department_id={department_id}&contract_type_id={contract_type_id}&shift_id={shift_id}"

    # return RedirectResponse(
    #     url = link,
    #     status_code=303
    # )

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
            }}, 2000);
        </script>
        </body>
        </html>
        """

    return HTMLResponse(html)



# =====================================================
#      U P D A T E -  T E A C H E R - S A L A R Y     #
# =====================================================
@teacher_salary_router.get("/update_stage_1/{payment_id}", response_class=HTMLResponse)
async def update_stage_1_fee(request: Request, payment_id: int, db: Session = Depends(get_db)):
    payment_old = db.query(TeacherPayment).filter(TeacherPayment.payment_id == payment_id).first()

    if not payment_old:
        return JSONResponse(content={"message": f"Teacher Payment with ID {payment_id} not found !!!"}, status_code=404)

    # -- load the data to update form --
    return templates.TemplateResponse(
        "pages/teacher_salary/update_teacher_salary.html",
        {
            "request": request, 
            "payment_old": payment_old
        }
    )


@teacher_salary_router.post("/update_teacher_salary")
async def update_teacher_salary(request: Request, db: Session = Depends(get_db)):
    
    # -- recieve form data --
    form_data = await request.form()
    payment_id = int(form_data.get("payment_id"))
    paid_salary = float(form_data.get("salary")) if form_data.get("salary") != '' else 0.0
    deduction = float(form_data.get("deduction")) if form_data.get("deduction") != '' else 0.0
    print("from_data", form_data)

    # # # -- find existing student --
    payment = db.query(TeacherPayment).filter(TeacherPayment.payment_id == payment_id).first()
    if not payment:
        return JSONResponse(content={"message": "Payment not found"}, status_code=404)


    # check nothing when entered
    if form_data.get("salary") == '':
        return JSONResponse(
            content = {
                "message": f"Salary can't be zero; Entered Value is: {paid_salary}"
            }
        )

    # check negative fee
    if paid_salary < 0:
        return JSONResponse(
            content = {
                "message": f"Salary can't be negative; Entered Value {paid_salary}"
            }
        )

    # # check negative discount
    if float(deduction) < 0:
        return JSONResponse(
            content = {
                "message": f"Deduction can't be negative; Entered Value {deduction}"
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
    payment.paid_salary = paid_salary
    payment.deduction = deduction
    db.commit()


    link = f'/salary/pay_salary?teacher_id={form_data.get("teacher_id")}&department_id={form_data.get("department_id")}&contract_type_id={form_data.get("contract_type_id")}&shift_id={form_data.get("shift_id")}'
    return RedirectResponse(
        url = link,
        status_code=303
    )




# ============================================================
#          D E L E T E  -  T E A C H E R - S A L A R Y       #
# ============================================================
@teacher_salary_router.delete("/delete_salary/")
async def delete_salary(payment_id: int, db: Session = Depends(get_db)):
    print("Request Recived")
    payment = db.query(TeacherPayment).filter(TeacherPayment.payment_id == payment_id).first()

    print()
    if not payment:
        return JSONResponse(content={"message": "Payment not found"}, status_code=404)

    db.delete(payment)
    db.commit()
    return RedirectResponse(url="/salary/list_salary", status_code=303)

