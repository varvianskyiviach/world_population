CREATE TABLE 
IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY, 
    country_name VARCHAR(255), 
    population INTEGER, 
    region VARCHAR(255), 
    data_source VARCHAR(255)
);