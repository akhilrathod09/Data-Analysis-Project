SELECT *
FROM dbo.engagement_data;

SELECT 
    EngagementID,
    ContentID,
    CampaignID,
    ProductID,
    UPPER(REPLACE(ContentType, 'Socialmedia', 'Social Media')) AS ContentType,
    SUBSTRING(ViewsClicksCombined, 1, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-',ViewsClicksCombined)) AS Clicks,
    Likes,
    FORMAT(CONVERT(DATE, EngagementDate), 'dd.MM.yyyy') AS EngagementDate
FROM dbo.engagement_data
WHERE ContentType != 'NewsLetter';
