-- creates a safeDiv function

DELIMITER //

-- function creation
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    -- Check if b is 0
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END //

DELIMITER ;
