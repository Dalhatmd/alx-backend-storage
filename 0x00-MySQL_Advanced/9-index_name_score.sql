-- creates index
CREATE INDEX idx_name_first_score
ON names (first_letter, score);
