-- ➕ Insert или Update
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- 📦 Массовая вставка
CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[],
    OUT invalid_data TEXT[]
)
AS $$
DECLARE
    i INT;
    temp_invalid TEXT[] := '{}';
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        
        IF phones[i] ~ '^[0-9]+$' THEN
            
            IF EXISTS (SELECT 1 FROM contacts WHERE name = names[i]) THEN
                UPDATE contacts SET phone = phones[i] WHERE name = names[i];
            ELSE
                INSERT INTO contacts(name, phone)
                VALUES (names[i], phones[i]);
            END IF;
        
        ELSE
            temp_invalid := array_append(temp_invalid, names[i] || ':' || phones[i]);
        END IF;

    END LOOP;

    invalid_data := temp_invalid;
END;
$$ LANGUAGE plpgsql;


-- ❌ Удаление
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;