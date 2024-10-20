DELIMITER $$

-- Create Procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    DECLARE average_weighted_score DECIMAL(10,2);

    -- Calculate total weighted score for the user
    SELECT SUM(s.score * w.weight), SUM(w.weight)
    INTO total_weighted_score, total_weight
    FROM scores s
    INNER JOIN weights w ON s.weight_id = w.id
    WHERE s.user_id = user_id;

    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id;
END$$

DELIMITER ;

