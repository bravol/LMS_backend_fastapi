from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi import HTTPException,status
import base64
from uuid import uuid4


# SPECIFY THE TIME ZONE
tz=ZoneInfo('Africa/Nairobi')

# method to format phone number
def formatPhoneNumber(phone_number: str):
    phone_number = phone_number.lstrip('+').strip()
    if phone_number.startswith('256'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('07'):
        phone_number = phone_number[1:]
    elif not phone_number.startswith('7'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number format")
    if len(phone_number) != 9:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number should have 9 digits after formatting")
    return f"256{phone_number}"


# identifying the provider
def identifyProvider(phone_number:str)->str:
    formatted_number= formatPhoneNumber(phone_number)
    airtel_prefixes=['25675','25670','25674']
    mtn_prefixes=['25677','25676','25678']

    if any(formatted_number.startswith(prefix) for prefix in airtel_prefixes):
        return 'AIRTEL'
    elif any(formatted_number.startswith(prefix) for prefix in mtn_prefixes):
        return 'MTN'
    else:
        return 'OTHER'

# receive the number of days and calculate the due date
def calculateDueDate(hours):
    current_date= datetime.now(tz)
    due_date = current_date + timedelta(hours=hours)
    return due_date


# METHOD TO FORMAT THE DUE DATE
def formatDueDate(due_date):
    datetime_str= str(due_date)
    dt=datetime.fromisoformat(datetime_str)
    dt = dt.astimezone(tz)
    formatted_date = dt.strftime('%b %d, %Y at %I:%M %p')
    return  formatted_date

# A METHOD TO PUT A THOUSAND SEPARATOR
def formatWithCommas(input_value):
    try:
        # Convert to integer in case the input is a string
        if isinstance(input_value, str):
            input_value = float(input_value.replace(",", ""))  # Remove existing commas to avoid conversion errors
        formatted_number = f"{input_value:,}"
        return formatted_number
    except ValueError:
        return "Invalid input"

def generateUniqueId(length=20):
    return base64.urlsafe_b64encode(uuid4().bytes).rstrip(b'=').decode('ascii')[:length]