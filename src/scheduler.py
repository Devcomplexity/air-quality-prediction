import schedule, time
from src.fetch_data import fetch_delhi_aqi
from src.alert import send_alert_email, send_sms_alert

def job():
    df = fetch_delhi_aqi()
    for _, row in df.iterrows():
        if row["AQI"] and row["AQI"] > 300:
            send_alert_email(row["Area"], row["AQI"])
            send_sms_alert(row["Area"], row["AQI"])

schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1440)
