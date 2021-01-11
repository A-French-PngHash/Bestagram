import database.mysql_connection


def value_in_database(table: str, field: str, value: str) -> bool:
    """
    Check if a value is present in the database.

    :param table: The table the value should be in.
    :param field: The field to check.
    :param value: Value to look for.
    :return: Return if the value was found.
    """
    request = f"""
    SELECT * FROM {table}
    WHERE {field} = \"{value}\";
    """
    cursor = database.mysql_connection.cnx.cursor(dictionary=True)

    try:
        cursor.execute(request)
    except Exception as e:
        print(e)
        cursor.close()
        return False
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

