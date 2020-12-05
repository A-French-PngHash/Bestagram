from database import mysql_connection


def request(instruction: str, fetch: bool = True) -> list:
    """
    Execute an instruction towards the database.
    :param fetch: Wether or not to fetch the result of the instruction on the cursor. Will perform a fetchall if True.
    :param instruction: The instruction to execute.
    :return: The cursor
    """
    cursor = mysql_connection.make_cursor()
    cursor.execute(instruction)
    if fetch:
        return cursor.fetchall()
    return []
