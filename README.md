*# Agentic Business Intelligence Command Center*



*## AI-Powered Business Analytics \& Decision Support System*



*### Project Overview*



*The Agentic Business Intelligence Command Center is an end-to-end analytics project designed for Data Analyst, Business Analyst, BI Analyst, and Power BI roles.*



*Traditional dashboards mainly explain what happened.*



*This project goes one step further by combining:*



*- Python*

*- PostgreSQL*

*- Advanced SQL*

*- Excel*

*- Power BI*

*- GenAI*

*- Agentic AI*



*The system can monitor business performance, investigate problems, validate findings, explain root causes, and provide management recommendations.*



*---*



*## Business Problem*



*Management needs more than a dashboard.*



*When revenue, profit, margin, or order performance changes, management wants to know:*



*- What happened?*

*- Where did the problem occur?*

*- Why might it have happened?*

*- Which areas should be investigated first?*

*- What action should management consider?*



*The goal of this project is to support those decisions using actual business data.*



*---*



*## Stakeholders*



*Main stakeholders:*



*- Business Head*

*- Sales Manager*

*- Finance Manager*

*- BI / Analytics Team*

*- Category Manager*



*---*



*## Dataset*



*The project uses a global e-commerce sales dataset.*



*Dataset size:*



*- 10,000 orders*

*- 2021 to 2024*

*- 4 regions*

*- 18 countries*

*- 5 product categories*

*- 70 products*



*---*



*## Project Architecture*



*Business Data*

*↓*

*Python Data Cleaning and EDA*

*↓*

*PostgreSQL Database*

*↓*

*Advanced SQL Analysis*

*↓*

*Excel Validation*

*↓*

*Power BI Dashboard*

*↓*

*Agentic AI Investigation*

*↓*

*SQL + Python Validation*

*↓*

*Management Explanation*

*↓*

*Recommended Action*



*---*



*## Python Analysis*



*Python was used for:*



*- Data quality checks*

*- Missing value checks*

*- Duplicate checks*

*- Data type validation*

*- Revenue and profit analysis*

*- Regional analysis*

*- Category analysis*

*- Customer segment analysis*

*- Discount analysis*

*- Loss-making order analysis*

*- Outlier detection*

*- Growth analysis*

*- Root-cause diagnostics*

*- Business flags*



*Important business flags created:*



*- Profit\_Status*

*- High\_Discount\_Flag*

*- High\_Shipping\_Cost\_Flag*



*---*



*## PostgreSQL and Advanced SQL*



*PostgreSQL was used as the central analytical database.*



*Advanced SQL concepts used:*



*- GROUP BY*

*- CASE*

*- CTE*

*- Multiple CTEs*

*- RANK*

*- DENSE\_RANK*

*- LAG*

*- Window Functions*

*- PARTITION BY*

*- Running Totals*

*- Contribution Percentage*

*- Root-Cause Analysis*



*The SQL layer provides verified business facts for the AI Agent.*



*---*



*## Excel Validation Layer*



*Excel was used as an independent validation layer.*



*Key KPIs validated:*



*- Total Revenue = 5,284,387.70*

*- Total Profit = 1,437,638.31*

*- Profit Margin = 27.21%*

*- Loss-Making Orders = 13.38%*

*- Revenue at Risk = 496,227.05*



*A Management Action Tracker was also created to connect analytical findings with business actions.*



*---*



*## Power BI Dashboard*



*The Power BI report contains exactly two pages.*



*### Page 1 — Executive Business Performance*



*Purpose:*



*Monitor overall business performance.*



*Main KPIs:*



*- Total Revenue*

*- Revenue Growth %*

*- Order Growth %*

*- Profit Margin %*



*Main charts:*



*- Monthly Revenue Trend*

*- Revenue by Region*

*- Revenue by Category*

*- Top 5 Products by Revenue*



*---*



*### Page 2 — Root Cause \& Action Analysis*



*Purpose:*



*Identify business risks and areas requiring management attention.*



*Main KPIs:*



*- Loss-Making Orders %*

*- Revenue at Risk*

*- Discount Impact %*

*- Problem Contribution %*



*Main charts:*



*- Loss Amount by Category*

*- Loss-Making Orders by Region*

*- Discount vs Profit*

*- Top 5 Loss-Making Products*



*---*



*## Agentic AI System*



*The project includes an interactive AI-powered Business Intelligence Agent.*



*The agent can accept natural-language business questions such as:*



*- Which region generates the highest revenue?*

*- Why are some orders making losses?*

*- Are high discounts hurting profitability?*

*- Which products are hurting profitability?*

*- Which customer segment is most valuable?*



*---*



*## How the Agent Works*



*User Question*

*↓*

*Agent Understands the Question*

*↓*

*Reads Actual PostgreSQL Schema*

*↓*

*Creates Investigation Plan*

*↓*

*Runs Three Read-Only SQL Queries*

*↓*

*Runs One Python Diagnostic Tool*

*↓*

*Cross-Validates the Evidence*

*↓*

*Generates Business Explanation*

*↓*

*Provides Recommended Management Action*



*---*



*## Agent Safety Features*



*The Agent includes:*



*- Read-only SQL execution*

*- SQL safety validation*

*- Blocked database modification commands*

*- Live PostgreSQL schema detection*

*- Automatic SQL repair*

*- Gemini retry mechanism*

*- Gemini model fallback*

*- Python diagnostic validation*

*- Evidence-based answers*



*The Agent does not directly modify the business database.*



*---*



*## Key Business Findings*



*The business generated:*



*- Total Revenue: 5.28M*

*- Total Profit: 1.44M*

*- Profit Margin: 27.21%*



*However:*



*- 1,338 orders were loss-making*

*- 13.38% of orders generated losses*

*- Total loss amount was approximately 83.5K*

*- Revenue associated with loss-making orders was approximately 496.23K*



*Loss-making orders had an average discount of approximately 44.52%.*



*Profitable orders had an average discount of approximately 13.53%.*



*Average shipping costs were very similar between profitable and loss-making orders.*



*This indicates that aggressive discounting has the strongest association with loss-making transactions.*



*The data shows an association, not confirmed causation.*



*---*



*## Regional Finding*



*The Middle East generated the highest overall revenue:*



*- Revenue: 1,348,593.22*

*- Profit: 384,522.85*

*- Profit Margin: 28.51%*

*- Orders: 2,458*



*The Middle East also had the highest average order value among the regions.*



*---*



*## Business Recommendations*



*Recommended management actions include:*



*- Review aggressive discounting policies*

*- Introduce margin-protection controls*

*- Investigate high-loss products*

*- Review product-level profitability before promotions*

*- Monitor revenue associated with loss-making transactions*

*- Investigate high-performing regions and product mixes*

*- Use targeted actions instead of broad discount strategies*



*These are analytical recommendations, not guaranteed outcomes.*



*---*



*## Technology Stack*



*- Python*

*- Pandas*

*- PostgreSQL*

*- Advanced SQL*

*- Excel*

*- Power BI Desktop*

*- DAX*

*- Star Schema*

*- Gemini API*

*- GenAI*

*- Agentic AI*

*- SQLAlchemy*

*- Psycopg2*



*---*



*## How to Run the AI Agent*



*Open:*



*D:\\Agentic\_BI\_Command\_Center\\agent*



*Double-click:*



*run\_agentic\_bi.bat*



*The system will start the Agentic Business Intelligence Command Center.*



*Ask a business question.*



*To close the program, type:*



*exit*



*---*



*## Project Value*



*This project demonstrates that I can:*



*- Clean and analyze business data*

*- Write advanced SQL queries*

*- Build business dashboards*

*- Validate KPIs*

*- Perform root-cause analysis*

*- Translate data into business actions*

*- Integrate GenAI with business data*

*- Build an Agentic AI workflow*

*- Generate evidence-based management recommendations*



*---*



*## Final Conclusion*



*This project is not only a Power BI dashboard.*



*It is an end-to-end Business Intelligence Decision Support System.*



*Power BI shows management what is happening.*



*SQL and Python investigate the data.*



*The Agentic AI layer allows management to ask business questions in natural language and receive answers grounded in verified business data.*



*The final workflow is:*



*Monitor → Detect → Investigate → Validate → Explain → Recommend*

