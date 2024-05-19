import requests

print(requests.get('https://i-love.space/api/apod').json())

from datetime import datetime, timedelta

# Get the current UTC time
now_utc = datetime.utcnow()

# Calculate the datetime for tomorrow
tomorrow_utc = now_utc + timedelta(days=1)

# Calculate the difference in seconds
seconds_until_tomorrow_utc = (tomorrow_utc - now_utc).total_seconds()

print(f"Seconds until tomorrow in UTC: {seconds_until_tomorrow_utc}")
