from sqlalchemy import text
from app.config.db_connect import engine 



def expense_triggers():
    trigger_sql = """
    -- 1️ Function for INSERT Trigger
    CREATE OR REPLACE FUNCTION trg_expense_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM account
            WHERE session_id = NEW.session_id
            AND month_id = NEW.month_id
            AND day_id = NEW.day_id
        ) THEN
            UPDATE account
            SET instt_expense = COALESCE(instt_expense, 0) + NEW.amount
            WHERE session_id = NEW.session_id
            AND month_id = NEW.month_id
            AND day_id = NEW.day_id;
        ELSE
            INSERT INTO account (session_id, month_id, day_id, instt_expense)
            VALUES (NEW.session_id, NEW.month_id, NEW.day_id, NEW.amount);
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- 2️Function for UPDATE Trigger
    CREATE OR REPLACE FUNCTION trg_expense_update()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE account
        SET instt_expense = COALESCE(instt_expense, 0) - OLD.amount + NEW.amount
        WHERE session_id = NEW.session_id
        AND month_id = NEW.month_id
        AND day_id = NEW.day_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- 3️Function for DELETE Trigger
    CREATE OR REPLACE FUNCTION trg_expense_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE account
        SET instt_expense = COALESCE(instt_expense, 0) - OLD.amount
        WHERE session_id = OLD.session_id
        AND month_id = OLD.month_id
        AND day_id = OLD.day_id;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- 4️ Create Triggers
    DROP TRIGGER IF EXISTS trg_after_expense_insert ON institute_expense;
    DROP TRIGGER IF EXISTS trg_after_expense_update ON institute_expense;
    DROP TRIGGER IF EXISTS trg_after_expense_delete ON institute_expense;

    CREATE TRIGGER trg_after_expense_insert
    AFTER INSERT ON institute_expense
    FOR EACH ROW
    EXECUTE FUNCTION trg_expense_insert();

    CREATE TRIGGER trg_after_expense_update
    AFTER UPDATE ON institute_expense
    FOR EACH ROW
    EXECUTE FUNCTION trg_expense_update();

    CREATE TRIGGER trg_after_expense_delete
    AFTER DELETE ON institute_expense
    FOR EACH ROW
    EXECUTE FUNCTION trg_expense_delete();
    """

    # Execute SQL
    with engine.connect() as conn:
        conn.execute(text(trigger_sql))
        conn.commit()
        print("Expenses Triggers and functions created successfully!")
