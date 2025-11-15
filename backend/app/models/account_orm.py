
from sqlalchemy import text
from app.config.db_connect import engine 


def account_table():
    sql_table = """
    -- Create account table
    CREATE TABLE account (
        session_id    INTEGER NOT NULL,
        month_id      INTEGER NOT NULL,
        day_id        INTEGER NOT NULL,
        total_fee     DOUBLE PRECISION DEFAULT 0,
        paid_salary   DOUBLE PRECISION DEFAULT 0,
        instt_income  DOUBLE PRECISION DEFAULT 0,
        instt_expense DOUBLE PRECISION DEFAULT 0,

        -- Computed Columns
        total_income  DOUBLE PRECISION GENERATED ALWAYS AS ("total_fee" + "instt_income") STORED,
        total_expenses DOUBLE PRECISION GENERATED ALWAYS AS ("paid_salary" + "instt_expense") STORED,
        account       DOUBLE PRECISION GENERATED ALWAYS AS (("total_fee" + "instt_income") - ("paid_salary" + "instt_expense")) STORED,

        -- Primary Key
        CONSTRAINT pk_account PRIMARY KEY (session_id, month_id, day_id),

        -- Foreign Keys
        FOREIGN KEY (session_id) REFERENCES session(session_id),
        FOREIGN KEY (month_id) REFERENCES month(month_id),
        FOREIGN KEY (day_id) REFERENCES day(day_id)
    );"""

    # Execute SQL
    with engine.connect() as conn:
        conn.execute(text(sql_table))
        conn.commit()
        print("account table successfully created....!")


