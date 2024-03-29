QUERY_LOAD = """INSERT INTO countries (country_name, population, region) VALUES ($1, $2, $3)"""

QUERY_FETCH = """SELECT t1.region, SUM(t1.population) as total_population,
    (select t2.country_name from countries t2 where t1.region = t2.region order by t2.population desc limit 1)
    as largest_country,
    MAX(t1.population) as max_population_country,
    (select t3.country_name from countries t3 where t1.region = t3.region order by t3.population asc limit 1)
    as smallest_country,
    MIN(t1.population) as min_population_country
    FROM countries t1
    GROUP BY t1.region
    ORDER BY total_population DESC;"""

PRINT_DATA = """ """
