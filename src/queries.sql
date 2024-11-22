-- User Engagement Reports: User Activity Summary
SELECT 
    activity_type, 
    COUNT(activity_id) AS activity_count, 
    DATE(activity_date) AS activity_date
FROM 
    ActivityLog
GROUP BY 
    activity_type, DATE(activity_date)
ORDER BY 
    activity_date DESC;



-- User Engagement Reports: Feedback Trends
SELECT 
    rating, 
    COUNT(feedback_id) AS feedback_count
FROM 
    Feedback
GROUP BY 
    rating
ORDER BY 
    rating ASC;


-- User Engagement Reports: Rewards Program Participation
SELECT 
    user_id, 
    SUM(points_earned) AS total_points_earned, 
    SUM(points_redeemed) AS total_points_redeemed
FROM 
    Rewards
WHERE 
    points_earned > 0 OR points_redeemed > 0
GROUP BY 
    user_id
ORDER BY 
    total_points_earned DESC;


-- Ticket Resolution Metrics: Ticket Submission Rates
SELECT 
    category, 
    COUNT(ticket_id) AS ticket_count,
    ROUND(COUNT(ticket_id) * 100 / (SELECT COUNT(*) FROM support_ticket), 2) AS percentage
FROM 
    support_ticket
GROUP BY 
    category
ORDER BY 
    ticket_count DESC;

-- Ticket Resolution Metrics: Average Response and Resolution Times
SELECT 
    category, 
    AVG(TIMESTAMPDIFF(HOUR, created_at, updated_at)) AS avg_resolution_time,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY TIMESTAMPDIFF(HOUR, created_at, updated_at)) AS median_resolution_time
FROM 
    support_ticket
WHERE 
    status = 'Resolved'
GROUP BY 
    category
ORDER BY 
    avg_resolution_time ASC;

-- Ticket Resolution Metrics: Ticket Status Distribution
SELECT 
    status, 
    COUNT(ticket_id) AS ticket_count,
    ROUND(COUNT(ticket_id) * 100 / (SELECT COUNT(*) FROM support_ticket), 2) AS percentage
FROM 
    support_ticket
GROUP BY 
    status
ORDER BY 
    ticket_count DESC;

-- Content Interaction Analytics: Interaction by Content Type
SELECT 
    content_type, 
    COUNT(content_id) AS interaction_count
FROM 
    Content
GROUP BY 
    content_type
ORDER BY 
    interaction_count DESC;

-- Content Interaction Analytics: Interaction by Content Category
SELECT 
    category, 
    COUNT(content_id) AS interaction_count
FROM 
    Content
GROUP BY 
    category
ORDER BY 
    interaction_count DESC;

-- Content Interaction Analytics: Most Popular Content
SELECT 
    content_id, 
    title, 
    content_type, 
    category, 
    COUNT(content_id) AS interaction_count
FROM 
    Content
GROUP BY 
    content_id, title, content_type, category
ORDER BY 
    interaction_count DESC
LIMIT 10;

-- Data Visualization Queries: Daily User Engagement
SELECT 
    DATE(activity_date) AS activity_date, 
    COUNT(activity_id) AS total_activities
FROM 
    ActivityLog
GROUP BY 
    DATE(activity_date)
ORDER BY 
    activity_date ASC;

-- Data Visualization Queries: Feedback Ratings Distribution
SELECT 
    rating, 
    COUNT(feedback_id) AS feedback_count
FROM 
    Feedback
GROUP BY 
    rating
ORDER BY 
    rating ASC;

-- Data Visualization Queries: Monthly Reward Trends
SELECT 
    DATE_FORMAT(earned_date, '%Y-%m') AS month, 
    SUM(points_earned) AS total_points_earned, 
    SUM(points_redeemed) AS total_points_redeemed
FROM 
    Rewards
GROUP BY 
    DATE_FORMAT(earned_date, '%Y-%m')
ORDER BY 
    month ASC;

-- Data Visualization Queries: Ticket Status Trends
SELECT 
    DATE(created_at) AS ticket_date, 
    status, 
    COUNT(ticket_id) AS ticket_count
FROM 
    support_ticket
GROUP BY 
    DATE(created_at), status
ORDER BY 
    ticket_date ASC, status;

-- System Performance Query
SELECT 
    DATE(activity_date) AS activity_date, 
    category, 
    SUM(metric_value) AS performance_metric
FROM (
    SELECT 
        activity_date, 
        'User Engagement' AS category, 
        COUNT(activity_id) AS metric_value
    FROM 
        ActivityLog
    GROUP BY 
        activity_date
    
    UNION ALL
    
    SELECT 
        DATE(created_at) AS activity_date, 
        'Tickets Resolved' AS category, 
        COUNT(ticket_id) AS metric_value
    FROM 
        support_ticket
    WHERE 
        status = 'Resolved'
    GROUP BY 
        DATE(created_at)
    
    UNION ALL
    
    SELECT 
        DATE(submitted_at) AS activity_date, 
        'Feedback Count' AS category, 
        COUNT(feedback_id) AS metric_value
    FROM 
        Feedback
    GROUP BY 
        DATE(submitted_at)
) AS system_performance
GROUP BY 
    activity_date, category
ORDER BY 
    activity_date, category;
