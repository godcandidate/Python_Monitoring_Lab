import time
from mailjet_rest import Client
import psutil
import os


# Email Configuration
API_KEY  = os.environ['API_KEY']
API_SECRET= os.environ['SECRET_KEY']
SENDER_EMAIL = "edward.dankwah@amalitech.com"
SENDER_NAME = "Devops Engineer"
RECIPIENT_EMAIL = "godcandidate101@gmail.com"
RECIPIENT_NAME = "Admin"

# Thresholds for Alerts (percentages)
CPU_THRESHOLD = 10
RAM_THRESHOLD = 10
DISK_THRESHOLD = 50

def send_alert(subject, message):
    """Send an alert email using the Mailjet API."""
    mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": SENDER_EMAIL,
                    "Name": SENDER_NAME
                },
                "To": [
                    {
                        "Email": RECIPIENT_EMAIL,
                        "Name": RECIPIENT_NAME
                    }
                ],
                "Subject": subject,
                "HTMLPart": f"<h3>{message}</h3>"
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent: {result.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


def check_system_metrics():
    """Check system metrics and return alert message if any threshold is breached."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    alert_message = ""
    if cpu_usage > CPU_THRESHOLD:
        alert_message += f"CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"
    if ram_usage > RAM_THRESHOLD:
        alert_message += f"RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"
    if disk_usage > DISK_THRESHOLD:
        alert_message += f"Disk space is low: {100 - disk_usage}% free (Threshold: {DISK_THRESHOLD}% free)\n"

    return alert_message


if __name__ == "__main__":
    
    current_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    
    # Check for any breaches in system metrics
    alert_message = check_system_metrics()
    
    # Send alert if any threshold is breached
    if alert_message:
        send_alert(f"Python Monitoring Alert - {formatted_time}", alert_message)
    else:
        print("All system metrics are within normal limits.")
   