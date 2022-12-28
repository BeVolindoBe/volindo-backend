from datetime import datetime


def get_number_of_nights(check_in, check_out) -> int:
    return (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days


def get_date_with_timezone(date):
    pass
