-- ============================================================================
-- PROJECT: Data Pipeline - Occupation and Wage Analysis (DANE GEIH)
-- SCRIPT: Analytical Transformation with Window Functions (PostgreSQL)
-- DESCRIPTION: Advanced queries for calculating rankings and trends
--              monthly and labor distribution metrics.
-- AUTHOR: Junior Data Engineer
-- DATE: Junio 2026
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CATEGORY A: RANKINGS AND COMPETITIVENESS (Ranking Functions)
-- ----------------------------------------------------------------------------

-- Query 1: AVG() OVER - Calculation of the individual salary gap vs. the departmental average
-- Allows you to identify the deviation of each individual's income from their region.
SELECT
    dpto,
    mes,
    inglabo,
    AVG(inglabo) OVER(PARTITION BY dpto) as promedio_dpto,
    inglabo - AVG(inglabo) OVER(PARTITION BY dpto) as diferencia_vs_promedio
FROM raw_ocupados
WHERE inglabo > 0
ORDER BY dpto ASC, inglabo DESC
LIMIT 20;


-- Query 2: ROW_NUMBER() - The top 5 highest earners by department
-- Useful for identifying anomalies or the highest incomes recorded by geographic area.
WITH ranked_salaries AS (
    SELECT
        dpto, mes, inglabo,
        ROW_NUMBER() OVER(PARTITION BY dpto ORDER BY inglabo DESC) as posicion
    FROM raw_ocupados
    WHERE inglabo > 0
)
SELECT * FROM ranked_salaries WHERE posicion <= 5;


-- Query 3: RANK() - Ranking of sectors (branch2d_r4) according to average salary
-- Evaluates which branches of economic activity generate higher income without skipping positions in case of ties.
WITH branch_avgs AS (
    S   ELECT
        rama2d_r4,
        AVG(inglabo) as salario_promedio
    FROM raw_ocupados
    WHERE inglabo > 0 AND rama2d_r4 IS NOT NULL
    GROUP BY rama2d_r4
)
SELECT
    rama2d_r4,
    salario_promedio,
    RANK() OVER(ORDER BY salario_promedio DESC) as rank_sector
FROM branch_avgs;


-- Query 4: DENSE_RANK() - Departments with the highest average monthly working hours
-- -- Classifies regional work intensity monthly in a compact way.
WITH dpto_hours AS (
    SELECT
        dpto, mes,
        AVG(p6800) as promedio_horas
    FROM raw_ocupados
    WHERE p6800 > 0 AND p6800 < 99
    GROUP BY dpto, mes
)
SELECT
    mes, dpto, promedio_horas,
    DENSE_RANK() OVER(PARTITION BY mes ORDER BY promedio_horas DESC) as rank_horas_dpto
FROM dpto_hours;


-- ----------------------------------------------------------------------------
-- CATEGORY B: COMPARISONS AND TRENDS (Value Functions)
-- ----------------------------------------------------------------------------

-- Query 5: LAG() - Comparison of average departmental income vs. the previous month
-- Measures the temporal evolution and month-to-month salary variations by region.
WITH monthly_dpto_avg AS (
    SELECT
        dpto, mes,
        AVG(inglabo) as avg_ingresos
    FROM raw_ocupados
    WHERE inglabo > 0
    GROUP BY dpto, mes
)
SELECT
    dpto, mes, avg_ingresos,
    LAG(avg_ingresos, 1) OVER(PARTITION BY dpto ORDER BY mes) as avg_mes_anterior,
    avg_ingresos - LAG(avg_ingresos, 1) OVER(PARTITION BY dpto ORDER BY mes) as variacion_salario
FROM monthly_dpto_avg;


-- Query 6: FIRST_VALUE() - Individual salary compared against the maximum cap for their department
-- Measures what percentage of the maximum departmental income the employee's salary represents.
SELECT
    dpto, inglabo,
    FIRST_VALUE(inglabo) OVER(PARTITION BY dpto ORDER BY inglabo DESC) as salario_max_dpto,
    (inglabo / FIRST_VALUE(inglabo) OVER(PARTITION BY dpto ORDER BY inglabo DESC) * 100) as porcentaje_del_maximo
FROM raw_ocupados
WHERE inglabo > 0
LIMIT 100;


-- Query 7: LAST_VALUE() - Hours worked compared against the lowest record in the department
-- Defines the lower bound of the working day by region using explicit windows.
SELECT
    dpto, p6800,
    LAST_VALUE(p6800) OVER(
        PARTITION BY dpto
        ORDER BY p6800 DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as min_horas_dpto
FROM raw_ocupados
WHERE p6800 > 0 AND p6800 < 99
LIMIT 100;


-- ----------------------------------------------------------------------------
-- CATEGORY C: CUMULATIVE AGGREGATIONS AND DISTRIBUTION METRICS
-- ----------------------------------------------------------------------------

-- Query 8: SUM() OVER - Monthly running total income by department
-- Generates salary accumulation curves throughout the year.
WITH dpto_monthly_totals AS (
    SELECT
        dpto, mes,
        SUM(inglabo) as total_ingresos_mes
    FROM raw_ocupados
    WHERE inglabo > 0
    GROUP BY dpto, mes
)
SELECT
    dpto, mes, total_ingresos_mes,
    SUM(total_ingresos_mes) OVER(PARTITION BY dpto ORDER BY mes) as total_acumulado_año
FROM dpto_monthly_totals;


-- Query 9: NTILE(4) - Segmentation by income quartiles by department
-- Divides the population into 4 equal groups to locate socioeconomic percentiles (richest 25% vs most vulnerable).
SELECT
    dpto, inglabo,
    NTILE(4) OVER(PARTITION BY dpto ORDER BY inglabo ASC) as cuartil_ingreso
FROM raw_ocupados
WHERE inglabo > 0;