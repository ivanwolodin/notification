SQL_QUERIES = {
    "EVERY_X_DAYS": """select * from (
                                select *, (processed::date - now()::date) days from newtable_1 n
                        ) as n where days > every_day  or processed is null""",
    "SEND_BROKER": "SELECT * FROM newtable_1 WHERE processed is null",
    "PROCESSED_ROWS": "update newtable_1 SET processed = now() WHERE user_id=%s",
}
