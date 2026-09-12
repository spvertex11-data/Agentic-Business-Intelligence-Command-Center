-- Create E-commerce Sales Table


CREATE TABLE ecommerce_sales (
    order_id VARCHAR(20),
    order_date DATE,
    year INTEGER,
    month INTEGER,
    quarter VARCHAR(10),
    season VARCHAR(20),
    customer_id VARCHAR(20),
    customer_gender VARCHAR(20),
    customer_segment VARCHAR(50),
    region VARCHAR(50),
    country VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name VARCHAR(200),
    unit_price NUMERIC(12,2),
    quantity INTEGER,
    discount NUMERIC(10,4),
    revenue NUMERIC(14,2),
    cost NUMERIC(14,2),
    profit NUMERIC(14,2),
    profit_margin_pct NUMERIC(10,4),
    shipping_cost NUMERIC(12,2),
    shipping_method VARCHAR(50),
    shipping_days INTEGER,
    payment_method VARCHAR(50),
    order_status VARCHAR(50),
    month_name VARCHAR(20),
    profit_status VARCHAR(20),
    high_discount_flag VARCHAR(30),
    high_shipping_cost_flag VARCHAR(30)
);


-- Check whether table was created

SELECT *
FROM ecommerce_sales;


-- Check table structure

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'ecommerce_sales'
ORDER BY ordinal_position;

SELECT COUNT(*) AS total_rows
FROM ecommerce_sales;


-- Preview imported data

SELECT *
FROM ecommerce_sales
LIMIT 10;


-- Check important imported fields

SELECT
    order_id,
    order_date,
    region,
    category,
    revenue,
    profit,
    profit_status
FROM ecommerce_sales
LIMIT 10;


-- Basic Row and Column Validation
-- Level: BASIC

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT region) AS total_regions,
    COUNT(DISTINCT category) AS total_categories
FROM ecommerce_sales;


-- Check order date range

SELECT
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM ecommerce_sales;


-- Check order date range

SELECT
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM ecommerce_sales;



-- Check null values in important columns

SELECT
    COUNT(*) FILTER (WHERE revenue IS NULL) AS revenue_nulls,
    COUNT(*) FILTER (WHERE profit IS NULL) AS profit_nulls,
    COUNT(*) FILTER (WHERE cost IS NULL) AS cost_nulls,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS quantity_nulls,
    COUNT(*) FILTER (WHERE discount IS NULL) AS discount_nulls
FROM ecommerce_sales;


-- Check null values in important business dimensions

SELECT
    COUNT(*) FILTER (WHERE region IS NULL) AS region_nulls,
    COUNT(*) FILTER (WHERE category IS NULL) AS category_nulls,
    COUNT(*) FILTER (WHERE product_name IS NULL) AS product_nulls,
    COUNT(*) FILTER (WHERE order_status IS NULL) AS status_nulls
FROM ecommerce_sales;

-- SQL STEP 5/30
-- Revenue, Profit and Order Summary
-- Level: BASIC

SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(revenue), 2) AS avg_order_revenue,
    ROUND(AVG(profit), 2) AS avg_order_profit
FROM ecommerce_sales;


-- Calculate overall profit margin

SELECT
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales;


-- Count profit and loss orders

SELECT
    profit_status,
    COUNT(*) AS total_orders
FROM ecommerce_sales
GROUP BY profit_status
ORDER BY total_orders DESC;


-- SQL STEP 6/15
-- Region-wise Performance Analysis
-- Level: MEDIUM

SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY region
ORDER BY total_profit DESC;


-- Find the lowest-profit region

SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
GROUP BY region
ORDER BY total_profit ASC
LIMIT 1;


-- SQL STEP 7/15
-- Category Performance Analysis
-- Level: MEDIUM

SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY category
ORDER BY total_profit DESC;


-- Find the weakest category

SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
GROUP BY category
ORDER BY total_profit ASC
LIMIT 1;


-- Compare categories by revenue and profit

SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
GROUP BY category
ORDER BY total_revenue DESC;


-- SQL STEP 8/15
-- Customer Segment Analysis
-- Level: MEDIUM

SELECT
    customer_segment,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY customer_segment
ORDER BY total_profit DESC;



-- Find the highest-profit customer segment

SELECT
    customer_segment,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
GROUP BY customer_segment
ORDER BY total_profit DESC
LIMIT 1;



-- SQL STEP 9/15
-- Discount Impact on Profitability
-- Level: MEDIUM

SELECT
    discount,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY discount
ORDER BY discount;


-- Compare high-discount and normal-discount orders

SELECT
    high_discount_flag,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(*) AS total_orders,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY high_discount_flag
ORDER BY total_profit DESC;


-- Check loss-making orders with high discount

SELECT
    COUNT(*) AS high_discount_loss_orders
FROM ecommerce_sales
WHERE high_discount_flag = 'High Discount'
  AND profit < 0;




-- SQL STEP 10/15
-- Order Status and Return Analysis
-- Level: MEDIUM

SELECT
    order_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM ecommerce_sales
GROUP BY order_status
ORDER BY total_orders DESC;  



-- Analyze returned and cancelled orders

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
WHERE order_status IN ('Returned', 'Cancelled')
GROUP BY order_status;



-- Calculate problem order percentage

SELECT
    ROUND(
        (
            COUNT(*) FILTER (
                WHERE order_status IN ('Returned', 'Cancelled')
            )::NUMERIC
            / COUNT(*)
        ) * 100,
        2
    ) AS problem_order_percentage
FROM ecommerce_sales;



-- SQL STEP 11/15
-- CTE-Based Root Cause Analysis
-- Level: HARD

WITH region_category_performance AS (
    SELECT
        region,
        category,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(
            (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100,
            2
        ) AS profit_margin_percentage
    FROM ecommerce_sales
    GROUP BY region, category
)

SELECT *
FROM region_category_performance
ORDER BY total_profit ASC;



-- Show the 10 weakest region-category combinations

WITH region_category_performance AS (
    SELECT
        region,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit,
        (SUM(profit) / NULLIF(SUM(revenue), 0)) * 100
            AS profit_margin_percentage
    FROM ecommerce_sales
    GROUP BY region, category
)

SELECT
    region,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(profit_margin_percentage, 2) AS profit_margin_percentage
FROM region_category_performance
ORDER BY total_profit ASC
LIMIT 10;



-- SQL STEP 12/15
-- RANK and DENSE_RANK Analysis
-- Level: HARD

WITH category_profit AS (
    SELECT
        region,
        category,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY region, category
)

SELECT
    region,
    category,
    ROUND(total_profit, 2) AS total_profit,

    RANK() OVER (
        PARTITION BY region
        ORDER BY total_profit DESC
    ) AS profit_rank,

    DENSE_RANK() OVER (
        PARTITION BY region
        ORDER BY total_profit DESC
    ) AS dense_profit_rank

FROM category_profit
ORDER BY region, profit_rank;



-- Find the top-profit category in each region

WITH category_profit AS (
    SELECT
        region,
        category,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY region, category
),

ranked_categories AS (
    SELECT
        region,
        category,
        total_profit,

        RANK() OVER (
            PARTITION BY region
            ORDER BY total_profit DESC
        ) AS profit_rank

    FROM category_profit
)

SELECT
    region,
    category,
    ROUND(total_profit, 2) AS total_profit
FROM ranked_categories
WHERE profit_rank = 1
ORDER BY total_profit DESC;


-- SQL STEP 13/15
-- Month-over-Month Growth using LAG
-- Level: HARD

WITH monthly_performance AS (
    SELECT
        year,
        month,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY year, month
),

previous_month_data AS (
    SELECT
        year,
        month,
        total_revenue,
        total_profit,

        LAG(total_revenue) OVER (
            ORDER BY year, month
        ) AS previous_month_revenue,

        LAG(total_profit) OVER (
            ORDER BY year, month
        ) AS previous_month_profit

    FROM monthly_performance
)

SELECT
    year,
    month,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,

    ROUND(
        ((total_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0)) * 100,
        2
    ) AS revenue_growth_percentage,

    ROUND(total_profit, 2) AS total_profit,
    ROUND(previous_month_profit, 2) AS previous_month_profit,

    ROUND(
        ((total_profit - previous_month_profit)
        / NULLIF(previous_month_profit, 0)) * 100,
        2
    ) AS profit_growth_percentage

FROM previous_month_data
ORDER BY year, month;



-- Find months with the biggest revenue decline

WITH monthly_performance AS (
    SELECT
        year,
        month,
        SUM(revenue) AS total_revenue
    FROM ecommerce_sales
    GROUP BY year, month
),

growth_analysis AS (
    SELECT
        year,
        month,
        total_revenue,

        LAG(total_revenue) OVER (
            ORDER BY year, month
        ) AS previous_month_revenue

    FROM monthly_performance
)

SELECT
    year,
    month,
    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(
        ((total_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0)) * 100,
        2
    ) AS revenue_growth_percentage

FROM growth_analysis
WHERE previous_month_revenue IS NOT NULL
ORDER BY revenue_growth_percentage ASC
LIMIT 10;



-- SQL STEP 14/15
-- Running Total and Contribution Analysis
-- Level: HARD

WITH monthly_revenue AS (
    SELECT
        year,
        month,
        SUM(revenue) AS total_revenue
    FROM ecommerce_sales
    GROUP BY year, month
)

SELECT
    year,
    month,
    ROUND(total_revenue, 2) AS monthly_revenue,

    ROUND(
        SUM(total_revenue) OVER (
            ORDER BY year, month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_revenue

FROM monthly_revenue
ORDER BY year, month;



-- Calculate region contribution to total revenue

WITH region_revenue AS (
    SELECT
        region,
        SUM(revenue) AS total_revenue
    FROM ecommerce_sales
    GROUP BY region
)

SELECT
    region,
    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(
        (
            total_revenue
            / SUM(total_revenue) OVER ()
        ) * 100,
        2
    ) AS revenue_contribution_percentage

FROM region_revenue
ORDER BY revenue_contribution_percentage DESC;



-- Calculate region contribution to total revenue

WITH region_revenue AS (
    SELECT
        region,
        SUM(revenue) AS total_revenue
    FROM ecommerce_sales
    GROUP BY region
)

SELECT
    region,
    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(
        (
            total_revenue
            / SUM(total_revenue) OVER ()
        ) * 100,
        2
    ) AS revenue_contribution_percentage

FROM region_revenue
ORDER BY revenue_contribution_percentage DESC;


-- Calculate region contribution to total profit

WITH region_profit AS (
    SELECT
        region,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY region
)

SELECT
    region,
    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        (
            total_profit
            / NULLIF(SUM(total_profit) OVER (), 0)
        ) * 100,
        2
    ) AS profit_contribution_percentage

FROM region_profit
ORDER BY profit_contribution_percentage DESC;


-- SQL STEP 15/15
-- Final Multi-CTE Root-Cause Analysis
-- Level: HARD

WITH region_category_summary AS (
    SELECT
        region,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit,
        AVG(discount) AS avg_discount,
        COUNT(DISTINCT order_id) AS total_orders
    FROM ecommerce_sales
    GROUP BY region, category
),

performance_metrics AS (
    SELECT
        region,
        category,
        total_revenue,
        total_profit,
        avg_discount,
        total_orders,

        (total_profit / NULLIF(total_revenue, 0)) * 100
            AS profit_margin_percentage,

        (total_revenue / SUM(total_revenue) OVER ()) * 100
            AS revenue_contribution_percentage

    FROM region_category_summary
),

diagnostic_flags AS (
    SELECT
        *,

        CASE
            WHEN total_profit < 0 THEN 'Critical Loss'
            WHEN profit_margin_percentage < 10
                 AND avg_discount > 0.10 THEN 'Margin Risk'
            WHEN profit_margin_percentage < 15 THEN 'Watch'
            ELSE 'Healthy'
        END AS performance_status

    FROM performance_metrics
)

SELECT
    region,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(avg_discount * 100, 2) AS avg_discount_percentage,
    total_orders,
    ROUND(profit_margin_percentage, 2) AS profit_margin_percentage,
    ROUND(revenue_contribution_percentage, 2) AS revenue_contribution_percentage,
    performance_status
FROM diagnostic_flags
ORDER BY
    CASE
        WHEN performance_status = 'Critical Loss' THEN 1
        WHEN performance_status = 'Margin Risk' THEN 2
        WHEN performance_status = 'Watch' THEN 3
        ELSE 4
    END,
    total_profit ASC;




-- Show only business areas that need management attention

WITH region_category_summary AS (
    SELECT
        region,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit,
        AVG(discount) AS avg_discount
    FROM ecommerce_sales
    GROUP BY region, category
),

analysis AS (
    SELECT
        *,
        (total_profit / NULLIF(total_revenue, 0)) * 100
            AS profit_margin_percentage
    FROM region_category_summary
)

SELECT
    region,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(avg_discount * 100, 2) AS avg_discount_percentage,
    ROUND(profit_margin_percentage, 2) AS profit_margin_percentage
FROM analysis
WHERE
    total_profit < 0
    OR profit_margin_percentage < 15
ORDER BY total_profit ASC;	



-- Check lowest profit-margin combinations

WITH region_category_summary AS (
    SELECT
        region,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit
    FROM ecommerce_sales
    GROUP BY region, category
)

SELECT
    region,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(
        (total_profit / NULLIF(total_revenue, 0)) * 100,
        2
    ) AS profit_margin_percentage
FROM region_category_summary
ORDER BY profit_margin_percentage ASC
LIMIT 10;



-- Show business areas that need management attention

WITH region_category_summary AS (
    SELECT
        region,
        category,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit,
        AVG(discount) AS avg_discount
    FROM ecommerce_sales
    GROUP BY region, category
),

analysis AS (
    SELECT
        *,
        (total_profit / NULLIF(total_revenue, 0)) * 100
            AS profit_margin_percentage
    FROM region_category_summary
)

SELECT
    region,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(avg_discount * 100, 2) AS avg_discount_percentage,
    ROUND(profit_margin_percentage, 2) AS profit_margin_percentage
FROM analysis
ORDER BY profit_margin_percentage ASC
LIMIT 10;