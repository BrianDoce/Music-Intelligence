SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['release_date']) }} AS release_date_key,
    release_date,
    YEAR(release_date) AS year,
    QUARTER(release_date) AS quarter,
    MONTH(release_date) AS month,
    MONTHNAME(release_date) AS month_name,
    DAY(release_date) AS day,
    DAYNAME(release_date) AS day_of_week,
    WEEKOFYEAR(release_date) AS week_of_year
FROM {{ ref('stg_albums') }}