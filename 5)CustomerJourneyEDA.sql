SELECT [JourneyID]
      ,[CustomerID]
      ,[ProductID]
      ,[VisitDate]
      ,[Stage]
      ,[Action]
      ,[Duration]
FROM [PortfolioProject_MarketingAnalytics].[dbo].[customer_journey]

--Finding the Duplicate Records by labelling them with row_num > 1
WITH DuplicateRecords AS (
    SELECT JourneyID,CustomerID,ProductID,VisitDate,Stage,Action,Duration,
	ROW_NUMBER() OVER( PARTITION BY CustomerID,ProductID,VisitDate,Stage,Action ORDER BY JourneyID ) AS row_num
FROM dbo.customer_journey
)

SELECT *
FROM DuplicateRecords
WHERE row_num >1
ORDER BY JourneyID;

--Cleaning and standardizing the Data using Exploratory Data analysis
SELECT JourneyID,CustomerID,ProductID,VisitDate,Stage,Action,ROUND(COALESCE(Duration, avg_duration),2) AS Duration
FROM
    (SELECT JourneyID,CustomerID,ProductID,VisitDate,
	UPPER(Stage) AS Stage,
	Action,
	Duration,
	AVG(Duration) OVER(PARTITION BY VisitDate) AS avg_duration,
	ROW_NUMBER() OVER(PARTITION BY JourneyID,CustomerID,ProductID,VisitDate,UPPER(Stage),Action 
	                  ORDER BY JourneyID
					  ) AS row_num
	FROM dbo.customer_journey
	) AS subquery
WHERE row_num = 1;
