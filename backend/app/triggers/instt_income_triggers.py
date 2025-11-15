from sqlalchemy import text
from app.config.db_connect import engine 



def income_triggers():
    trigger_sql = """
    --  Function for INSERT Trigger
    CREATE OR REPLACE FUNCTION trg_income_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM account
            WHERE session_id = NEW.session_id
            AND month_id = NEW.month_id
            AND day_id = NEW.day_id
        ) THEN
            UPDATE account
            SET instt_income = COALESCE(instt_income, 0) + NEW.amount
            WHERE session_id = NEW.session_id
            AND month_id = NEW.month_id
            AND day_id = NEW.day_id;
        ELSE
            INSERT INTO account (session_id, month_id, day_id, instt_income)
            VALUES (NEW.session_id, NEW.month_id, NEW.day_id, NEW.amount);
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;


    --  Function for UPDATE Trigger
    CREATE OR REPLACE FUNCTION trg_income_update()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE account
        SET instt_income = COALESCE(instt_income, 0) - OLD.amount + NEW.amount
        WHERE session_id = NEW.session_id
        AND month_id = NEW.month_id
        AND day_id = NEW.day_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;


    --  Function for DELETE Trigger
    CREATE OR REPLACE FUNCTION trg_income_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE account
        SET instt_income = COALESCE(instt_income, 0) - OLD.amount
        WHERE session_id = OLD.session_id
        AND month_id = OLD.month_id
        AND day_id = OLD.day_id;

        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;


    --  Create Triggers
    DROP TRIGGER IF EXISTS trg_after_expense_insert ON institute_income;
    DROP TRIGGER IF EXISTS trg_after_expense_update ON institute_income;
    DROP TRIGGER IF EXISTS trg_after_expense_delete ON institute_income;


    -- After insert
    CREATE TRIGGER trg_after_income_insert
    AFTER INSERT ON institute_income
    FOR EACH ROW
    EXECUTE FUNCTION trg_income_insert();

    -- After update
    CREATE TRIGGER trg_after_income_update
    AFTER UPDATE ON institute_income
    FOR EACH ROW
    EXECUTE FUNCTION trg_income_update();

    -- After delete
    CREATE TRIGGER trg_after_income_delete
    AFTER DELETE ON institute_income
    FOR EACH ROW
    EXECUTE FUNCTION trg_income_delete();
    """

    # Execute SQL
    with engine.connect() as conn:
        conn.execute(text(trigger_sql))
        conn.commit()
        print("Triggers and functions created successfully!")
