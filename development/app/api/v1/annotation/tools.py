import datetime


def get_utc_timestamp():
    # Get the current UTC time
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)

    # Format the time as xsd:dateTime with "Z" for UTC timezone
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    return formatted_time
