-- Write a SQL script that creates a trigger that resets the attribute valid_email only when the email has been changed


DELIMITER //
-- Trigger that resets valid_email when email has been changed
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = FALSE;
    END IF;
END //

DELIMITER ;

