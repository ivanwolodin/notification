SQL_QUERIES = {
    "EVERY_X_DAYS": """select * from (
                                select *, (processed::date - now()::date) days 
                                from notifications n
                                inner join templates t on t.id = n.template_id
                        ) as n where days > every_day  or processed is null""",
    "SEND_BROKER": "SELECT * FROM notifications WHERE processed is null",
    "PROCESSED_ROWS": "update notifications SET processed = now() WHERE user_id=%s",
}
