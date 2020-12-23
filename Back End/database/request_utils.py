import mysql.connector


def value_in_database(table: str, field: str, value: str, cnx: mysql.connector.MySQLConnection) -> bool:
    """
    Check if a value is present in the database.

    :param cnx: Connection to the database.
    :param table: The table the value should be in.
    :param field: The field to check.
    :param value: Value to look for.
    :return: Return if the value was found.
    """
    request = f"""
    SELECT * FROM {table}
    WHERE {field} = \"{value}\";
    """
    pcursor = cnx.cursor(dictionary=True)

    try:
        pcursor.execute(request)
    except Exception as e:
        print(e)
        pcursor.close()
        return False
    result = pcursor.fetchall()
    pcursor.close()
    return len(result) > 0

