SELECT *
FROM dbo.customer_reviews;

--Selecting equal spacing in Review Text to single spacing
SELECT ReviewID,CustomerID,ProductID,ReviewDate,Rating,
REPLACE(ReviewText,'  ',' ') AS ReviewText
FROM dbo.customer_reviews;
