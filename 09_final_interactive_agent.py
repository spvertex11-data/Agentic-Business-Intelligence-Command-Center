# AGENTIC AI STEP 12
# Final Interactive Business Intelligence Agent
# Level: ADVANCED

import os
import json
import time
import pandas as pd
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from google import genai
from google.genai import errors


# Load Environment Variables

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Validate Environment Variables

required_values = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "GEMINI_API_KEY": GEMINI_API_KEY
}

missing_values = [
    key
    for key, value in required_values.items()
    if not value
]

if missing_values:

    print(
        "ERROR: Missing values in .env file:",
        ", ".join(missing_values)
    )

    raise SystemExit


# Create Gemini Client

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Gemini Model Fallback

MODELS_TO_TRY = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]


# PostgreSQL Connection

def get_connection():

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# SQLAlchemy Engine
# URL.create safely handles special password characters

def get_engine():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME
    )

    return create_engine(
        database_url
    )


# Gemini Function
# Retry + Model Fallback

def ask_gemini(prompt):

    for model_name in MODELS_TO_TRY:

        print()
        print(
            f"Trying Gemini model: {model_name}"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Attempt {attempt}/3"
                )

                chat = client.chats.create(
                    model=model_name
                )

                response = chat.send_message(
                    prompt
                )

                print(
                    f"Gemini response successful "
                    f"using {model_name}"
                )

                return response.text

            except errors.ServerError:

                print(
                    "Temporary Gemini server error."
                )

                if attempt < 3:

                    wait_seconds = attempt * 5

                    print(
                        f"Waiting {wait_seconds} seconds..."
                    )

                    time.sleep(
                        wait_seconds
                    )

            except errors.ClientError as error:

                print()
                print(
                    f"Gemini API error with "
                    f"{model_name}:"
                )

                print(error)

                print(
                    "Trying fallback model..."
                )

                break

            except Exception as error:

                print()
                print(
                    "Unexpected Gemini error:"
                )

                print(error)

                break

    return None


# Read Actual PostgreSQL Schema

def get_live_schema():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'ecommerce_sales'
        ORDER BY ordinal_position;
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    schema_text = (
        "Table: ecommerce_sales\n\n"
        "Columns:\n"
    )

    for column_name, data_type in rows:

        schema_text += (
            f"- {column_name} ({data_type})\n"
        )

    return schema_text


# Clean JSON Returned By Gemini

def clean_json(text):

    text = text.strip()

    text = (
        text
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("```", "")
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        text = text[
            start:end + 1
        ]

    return text.strip()


# Clean SQL Returned By Gemini

def clean_sql(text):

    return (
        text
        .replace("```sql", "")
        .replace("```SQL", "")
        .replace("```", "")
        .strip()
    )


# SQL Safety Validation

def validate_sql(sql_query):

    if not sql_query:

        return False

    query_upper = (
        sql_query.upper().strip()
    )

    if not (
        query_upper.startswith("SELECT")
        or query_upper.startswith("WITH")
    ):

        return False

    blocked_words = [
        "INSERT ",
        "UPDATE ",
        "DELETE ",
        "DROP ",
        "ALTER ",
        "TRUNCATE ",
        "CREATE ",
        "GRANT ",
        "REVOKE ",
        "COPY ",
        "CALL ",
        "MERGE ",
        "DO "
    ]

    for word in blocked_words:

        if word in query_upper:

            return False

    query_without_final_semicolon = (
        sql_query.strip().rstrip(";")
    )

    if ";" in query_without_final_semicolon:

        return False

    return True


# Execute Read-Only SQL

def execute_sql(sql_query):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        connection.set_session(
            readonly=True,
            autocommit=False
        )

        cursor = connection.cursor()

        cursor.execute(
            "SET statement_timeout = 15000;"
        )

        cursor.execute(
            sql_query
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return columns, rows

    finally:

        if cursor is not None:

            cursor.close()

        if connection is not None:

            connection.close()


# Automatic SQL Repair

def repair_sql(
    failed_sql,
    sql_error,
    live_schema,
    business_question
):

    repair_prompt = f"""
You are a PostgreSQL SQL repair agent.

A read-only PostgreSQL query failed.

USER BUSINESS QUESTION:

{business_question}

ACTUAL DATABASE SCHEMA:

{live_schema}

FAILED SQL:

{failed_sql}

POSTGRESQL ERROR:

{sql_error}

Repair the SQL query.

STRICT RULES:

1. Use only ecommerce_sales.
2. Use ONLY columns from the actual schema.
3. Use PostgreSQL syntax.
4. Query must be read-only.
5. Use SELECT or WITH only.
6. Never modify the database.
7. Return ONLY corrected SQL.
8. Do not use markdown.
9. Do not explain the SQL.
"""

    repaired_sql = ask_gemini(
        repair_prompt
    )

    if repaired_sql:

        return clean_sql(
            repaired_sql
        )

    return None


# Load PostgreSQL Data Into Pandas

def load_python_data():

    engine = get_engine()

    try:

        query = """
            SELECT *
            FROM ecommerce_sales;
        """

        df = pd.read_sql_query(
            query,
            engine
        )

        return df

    finally:

        engine.dispose()


# Python Tool 1
# Loss Diagnostics

def loss_diagnostics(df):

    loss_df = df[
        df["profit"] < 0
    ].copy()

    profit_df = df[
        df["profit"] >= 0
    ].copy()

    return {

        "total_orders":
            int(len(df)),

        "loss_orders":
            int(len(loss_df)),

        "loss_order_pct":
            round(
                len(loss_df)
                / len(df)
                * 100,
                2
            ),

        "loss_avg_discount_pct":
            round(
                float(
                    loss_df[
                        "discount"
                    ].mean()
                ) * 100,
                2
            ),

        "profitable_avg_discount_pct":
            round(
                float(
                    profit_df[
                        "discount"
                    ].mean()
                ) * 100,
                2
            ),

        "loss_avg_shipping_cost":
            round(
                float(
                    loss_df[
                        "shipping_cost"
                    ].mean()
                ),
                2
            ),

        "profit_avg_shipping_cost":
            round(
                float(
                    profit_df[
                        "shipping_cost"
                    ].mean()
                ),
                2
            ),

        "total_loss_amount":
            round(
                float(
                    loss_df[
                        "profit"
                    ].sum()
                ),
                2
            )
    }


# Python Tool 2
# Discount Diagnostics

def discount_diagnostics(df):

    result = (
        df.groupby(
            "high_discount_flag"
        )
        .agg(
            Total_Orders=(
                "order_id",
                "count"
            ),
            Average_Discount=(
                "discount",
                "mean"
            ),
            Average_Revenue=(
                "revenue",
                "mean"
            ),
            Average_Profit=(
                "profit",
                "mean"
            ),
            Total_Profit=(
                "profit",
                "sum"
            )
        )
        .round(2)
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )


# Python Tool 3
# Regional Performance

def regional_performance(df):

    result = (
        df.groupby(
            "region"
        )
        .agg(
            Orders=(
                "order_id",
                "count"
            ),
            Revenue=(
                "revenue",
                "sum"
            ),
            Profit=(
                "profit",
                "sum"
            )
        )
    )

    result[
        "Profit_Margin_Pct"
    ] = (
        result["Profit"]
        / result["Revenue"]
        * 100
    )

    result = (
        result
        .round(2)
        .sort_values(
            "Revenue",
            ascending=False
        )
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )


# Python Tool 4
# Product Performance

def product_performance(df):

    result = (
        df.groupby(
            [
                "category",
                "sub_category"
            ]
        )
        .agg(
            Orders=(
                "order_id",
                "count"
            ),
            Revenue=(
                "revenue",
                "sum"
            ),
            Profit=(
                "profit",
                "sum"
            ),
            Average_Discount=(
                "discount",
                "mean"
            )
        )
        .round(2)
        .sort_values(
            "Profit",
            ascending=True
        )
        .head(10)
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )


# Python Tool 5
# Customer Segment Analysis

def customer_segment_analysis(df):

    result = (
        df.groupby(
            "customer_segment"
        )
        .agg(
            Orders=(
                "order_id",
                "count"
            ),
            Revenue=(
                "revenue",
                "sum"
            ),
            Profit=(
                "profit",
                "sum"
            ),
            Average_Order_Revenue=(
                "revenue",
                "mean"
            )
        )
        .round(2)
        .sort_values(
            "Revenue",
            ascending=False
        )
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )


# Python Tool 6
# Order Status Analysis

def order_status_analysis(df):

    result = (
        df.groupby(
            "order_status"
        )
        .agg(
            Orders=(
                "order_id",
                "count"
            ),
            Revenue=(
                "revenue",
                "sum"
            ),
            Profit=(
                "profit",
                "sum"
            )
        )
        .round(2)
        .sort_values(
            "Orders",
            ascending=False
        )
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )


# Python Tool Map

PYTHON_TOOLS = {

    "loss_diagnostics":
        loss_diagnostics,

    "discount_diagnostics":
        discount_diagnostics,

    "regional_performance":
        regional_performance,

    "product_performance":
        product_performance,

    "customer_segment_analysis":
        customer_segment_analysis,

    "order_status_analysis":
        order_status_analysis
}


# Program Heading

print()
print("=" * 72)
print("AGENTIC BUSINESS INTELLIGENCE COMMAND CENTER")
print("=" * 72)

print()
print(
    "AI-Powered Business Analytics "
    "& Decision Support System"
)

print()
print(
    "Connecting to PostgreSQL..."
)


# Load Actual Database Schema

try:

    LIVE_SCHEMA = get_live_schema()

    print(
        "PostgreSQL schema loaded successfully."
    )

except Exception as error:

    print()
    print(
        "PostgreSQL connection failed."
    )

    print(
        "Error:",
        error
    )

    raise SystemExit


# Main Interactive Loop

while True:

    print()
    print("=" * 72)

    business_question = input(
        "Business Question "
        "(type 'exit' to close): "
    ).strip()


    # Exit Program

    if business_question.lower() in [
        "exit",
        "quit",
        "close"
    ]:

        print()
        print(
            "Agentic BI Command Center closed."
        )

        break


    # Empty Question Check

    if not business_question:

        print()
        print(
            "Please enter a business question."
        )

        continue


    # Create Investigation Plan

    planning_prompt = f"""
You are an Agentic Business Intelligence Analyst.

USER BUSINESS QUESTION:

{business_question}

ACTUAL POSTGRESQL DATABASE SCHEMA:

{LIVE_SCHEMA}

You have access to:

1. PostgreSQL
2. Approved Python diagnostic tools

AVAILABLE PYTHON TOOLS:

loss_diagnostics
Use for:
- loss-making orders
- negative profit
- profitability problems

discount_diagnostics
Use for:
- discounts
- promotion analysis
- discount impact

regional_performance
Use for:
- region performance
- regional revenue
- regional profit

product_performance
Use for:
- category
- sub-category
- product profitability

customer_segment_analysis
Use for:
- customer segment performance

order_status_analysis
Use for:
- order status
- returns
- cancellations

Create an investigation plan.

STRICT RULES:

1. Generate exactly THREE PostgreSQL queries.

2. Each query must investigate a different
useful business angle.

3. Use only ecommerce_sales.

4. Use ONLY columns from the actual schema.

5. SQL must be read-only.

6. Use SELECT or WITH only.

7. Select exactly ONE approved Python tool.

8. Never invent Python tool names.

9. Keep SQL results reasonably small.

10. Use LIMIT where appropriate.

11. Return ONLY valid JSON.

JSON FORMAT:

{{
    "investigation_goal":
        "Short investigation goal",

    "sql_queries": [
        {{
            "step": 1,
            "purpose": "Purpose",
            "sql": "PostgreSQL query"
        }},
        {{
            "step": 2,
            "purpose": "Purpose",
            "sql": "PostgreSQL query"
        }},
        {{
            "step": 3,
            "purpose": "Purpose",
            "sql": "PostgreSQL query"
        }}
    ],

    "python_tool":
        "approved Python tool",

    "python_purpose":
        "Why Python validation is useful"
}}
"""


    print()
    print(
        "Agent is creating an investigation plan..."
    )


    plan_text = ask_gemini(
        planning_prompt
    )


    if not plan_text:

        print()
        print(
            "Could not create investigation plan."
        )

        continue


    # Parse Investigation Plan

    try:

        plan = json.loads(
            clean_json(
                plan_text
            )
        )

    except Exception as error:

        print()
        print(
            "Invalid Gemini investigation plan."
        )

        print(
            "Error:",
            error
        )

        continue


    # Show Investigation Plan

    print()
    print("=" * 72)
    print("INVESTIGATION PLAN")
    print("=" * 72)

    print()
    print(
        "Goal:",
        plan.get(
            "investigation_goal"
        )
    )

    print(
        "Python Tool:",
        plan.get(
            "python_tool"
        )
    )

    print(
        "Python Purpose:",
        plan.get(
            "python_purpose"
        )
    )


    # Store SQL Evidence

    sql_evidence = []


    # Execute SQL Investigation

    for item in plan.get(
        "sql_queries",
        []
    ):

        step = item.get(
            "step"
        )

        purpose = item.get(
            "purpose"
        )

        sql_query = clean_sql(
            item.get(
                "sql",
                ""
            )
        )


        print()
        print("=" * 72)
        print(
            f"SQL INVESTIGATION STEP {step}"
        )
        print("=" * 72)

        print()
        print(
            "Purpose:",
            purpose
        )

        print()
        print(
            "Generated SQL:"
        )

        print(
            sql_query
        )


        # Safety Check

        if not validate_sql(
            sql_query
        ):

            print()
            print(
                "SQL blocked for safety."
            )

            continue


        # Execute Initial SQL

        try:

            columns, rows = execute_sql(
                sql_query
            )

        except Exception as error:

            print()
            print(
                "Initial SQL execution failed."
            )

            print(
                "Error:",
                error
            )

            print()
            print(
                "Agent attempting SQL auto-repair..."
            )


            # Automatic SQL Repair

            repaired_sql = repair_sql(
                failed_sql=sql_query,
                sql_error=str(error),
                live_schema=LIVE_SCHEMA,
                business_question=business_question
            )


            if not repaired_sql:

                print()
                print(
                    "SQL repair unavailable."
                )

                continue


            print()
            print(
                "Repaired SQL:"
            )

            print(
                repaired_sql
            )


            # Safety Check Repaired SQL

            if not validate_sql(
                repaired_sql
            ):

                print()
                print(
                    "Repaired SQL blocked for safety."
                )

                continue


            # Execute Repaired SQL

            try:

                columns, rows = execute_sql(
                    repaired_sql
                )

                sql_query = repaired_sql

                print()
                print(
                    "Repaired SQL executed successfully."
                )

            except Exception as second_error:

                print()
                print(
                    "Repaired SQL also failed."
                )

                print(
                    "Error:",
                    second_error
                )

                continue


        # Show Verified SQL Result

        print()
        print(
            "VERIFIED SQL RESULT"
        )

        print(
            "Columns:",
            columns
        )

        print()

        if not rows:

            print(
                "No rows returned."
            )

        else:

            for row in rows[:20]:

                print(
                    row
                )


        # Save SQL Evidence

        sql_evidence.append(
            {
                "step": step,
                "purpose": purpose,
                "sql": sql_query,
                "columns": columns,
                "result": rows[:20]
            }
        )


    # Python Diagnostic

    python_tool_name = plan.get(
        "python_tool"
    )

    python_evidence = None


    print()
    print("=" * 72)
    print("PYTHON DIAGNOSTIC")
    print("=" * 72)


    # Validate Python Tool

    if python_tool_name not in PYTHON_TOOLS:

        print()
        print(
            "Invalid Python tool selected."
        )

    else:

        try:

            print()
            print(
                f"Running Python tool: "
                f"{python_tool_name}"
            )

            # Load data using SQLAlchemy

            df = load_python_data()

            print(
                f"Python loaded {len(df)} rows "
                "from PostgreSQL."
            )


            # Run Selected Tool

            python_function = (
                PYTHON_TOOLS[
                    python_tool_name
                ]
            )

            python_evidence = (
                python_function(
                    df
                )
            )


            print()
            print(
                "VERIFIED PYTHON RESULT"
            )

            print(
                python_evidence
            )

        except Exception as error:

            print()
            print(
                "Python diagnostic failed."
            )

            print(
                "Error:",
                error
            )


    # Verify Evidence Exists

    if (
        not sql_evidence
        and python_evidence is None
    ):

        print()
        print(
            "No verified evidence available."
        )

        continue


    # Final Management Prompt

    final_prompt = f"""
You are a Senior Business Intelligence Analyst.

USER BUSINESS QUESTION:

{business_question}

VERIFIED SQL EVIDENCE:

{sql_evidence}

VERIFIED PYTHON EVIDENCE:

{python_evidence}

STRICT RULES:

1. Use ONLY verified SQL and Python evidence.

2. Never invent numbers.

3. Never guess missing facts.

4. Clearly separate facts from recommendations.

5. Do not claim causation unless evidence proves it.

6. When appropriate state:

"The data shows an association,
not confirmed causation."

7. Mention important actual numbers.

8. If SQL and Python support the same result,
state that the finding was cross-validated.

9. If Python validation failed,
do not pretend Python validated the result.

10. Recommendations are suggested business actions,
not guaranteed outcomes.

11. Use simple professional English.

ANSWER STRUCTURE:

1. Executive Answer

2. SQL Evidence

3. Python Validation

4. Most Likely Business Driver

5. What Cannot Yet Be Proven

6. Recommended Management Action
"""


    print()
    print("=" * 72)
    print("GENERATING FINAL MANAGEMENT ANSWER")
    print("=" * 72)


    final_answer = ask_gemini(
        final_prompt
    )


    # Display Final Answer

    print()
    print("=" * 72)
    print("FINAL AGENT ANSWER")
    print("=" * 72)

    print()


    if final_answer:

        print(
            final_answer
        )

    else:

        print(
            "Gemini explanation unavailable."
        )

        print()
        print(
            "Verified SQL and Python evidence "
            "is still shown above."
        )


    print()
    print("=" * 72)
    print("QUESTION COMPLETE")
    print("=" * 72)

    print()
    print(
        "You can now ask another question."
    )