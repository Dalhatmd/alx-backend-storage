DELIMITER //
-- creates procedure
CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;
    
    -- Try to get the project id if it exists
    SELECT id INTO project_id 
    FROM projects 
    WHERE name = p_project_name;
    
    -- If project doesn't exist, create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) 
        VALUES (p_project_name);
        
        -- Get the id of the newly created project
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    -- Insert the correction
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (p_user_id, project_id, p_score);
END //

DELIMITER ;
