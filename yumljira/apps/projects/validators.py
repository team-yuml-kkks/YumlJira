from django.utils.translation import gettext as _


def validate_number_in_board(number, project, old_value=None):
    """
    Validates `Column's` `number_in_board` field.

    Args:
        number (int) - Number to validate.
        project (`Project`) - Project instance.

    Returns:
        Tuple (bool, str) - Tuple which first value is success status and second
        is error message to display.

    Validation process:
        First we check if number is not 0. Then we take current order of board.
        If new number is greater than number in last column we have to check
        if number between new number and last number is not greater than one.

    Examples:
        number - 3
        project - 4 columns

        In this case number is valid and and columns with number 3 or greater
        are increase by one. So we will have [1, 2, 3, 4, 5]. When 3 is new column
        and rest are old ones.

        number - 6
        project - 4 columns

        This time number is not valid because there aren't any columns between
        last old column and the one we want to create.
    """
    if number == 0:
        return (False, _('You have to specify number greater than 0.'))

    columns_numbers = project.columns.all() \
        .order_by('number_in_board') \
        .values_list('number_in_board', flat=True)

    last_number = columns_numbers.last()

    if number > last_number and number - last_number is not 1:
        return (False, _('Number is too big.'))

    if old_value == last_number and number - old_value is not 0:
        return (False, _('Number is too big.'))

    if old_value and number not in columns_numbers:
        return (False, _('Number is too big.'))

    return (True, '')

