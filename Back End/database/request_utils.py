from database.mysql_connection import *


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
    pcursor = cnx.cursor(dictionary=True)
    try:
        pcursor.execute(request)
    except Exception as e:
        print(e)
        return False
    result = pcursor.fetchall()
    return len(result) > 0
