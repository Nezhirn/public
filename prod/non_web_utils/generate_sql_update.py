def generate_sql_update(inn_list, output_path):
    sql_body = []
    
    for inn in inn_list:
        sql_body.append(f"    SELECT\n"
                        f"        '{inn}' AS inn,\n"
                        f"        '' AS name_deleted,\n"
                        f"        TIMESTAMP '2025-02-06 00:00:00.000000' AS date_deleted,\n"
                        f"        '' AS comment\n"
                        f"    UNION ALL")
    
    # Удалим последний UNION ALL
    if sql_body:
        sql_body[-1] = sql_body[-1].replace("UNION ALL", "", 1)
    
    sql_body = "\n".join(sql_body)

    final_sql = f"""
WITH updates AS (
{sql_body}
)
UPDATE public.portal_stop_list pst
SET
    name_deleted = u.name_deleted,
    date_deleted = u.date_deleted,
    comment = u.comment,
    is_deleted = true
FROM updates u
WHERE pst.inn = u.inn
  AND pst.is_deleted = false
  AND pst."srguServicePassportName" = '';
"""

    # Сохранение в файл
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_sql)

# Пример использования
inn_list = [

]
output_path = '/home/andrew/update.sql'
generate_sql_update(inn_list, output_path)