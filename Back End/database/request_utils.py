import database.mysql_connection
import errors


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


def user_existing(id : int) -> bool:
    query = f"""
    SELECT * FROM UserTable
    WHERE id = {id};"""
    cursor = database.mysql_connection.cnx.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return len(result) == 1



def get_user_id_from_username(username: str) -> int:
    """
    Fetch a user id from a username.
    :param username:

    :raise UsernameNotExisting: Raise this error when the username is not existing in the database.

    :return: Return the user id.
    """
    id_query = f"""
    SELECT id, username FROM UserTable
    WHERE username = "{username}";
    """
    cursor = database.mysql_connection.cnx.cursor(dictionary=True)
    cursor.execute(id_query)
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        raise errors.UserNotExisting(username=username)
    else:
        return result[0]["id"]

