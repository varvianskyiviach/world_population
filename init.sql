CREATE TABLE IF NOT EXISTS countries_some (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    population INTEGER NOT NULL,
    region VARCHAR(255) NOT NULL
);
