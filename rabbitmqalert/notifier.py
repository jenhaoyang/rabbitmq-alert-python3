import urllib.request
import urllib.parse
from send_it import sendemail

class Notifier:

    def __init__(self, logger, arguments):
        self.log = logger
        self.arguments = arguments

    def send_notification(self, body):
        text = f"{self.arguments['server_host_alias'] or self.arguments['server_host']} - {body}"

        if self.arguments["email_to"]:
            self.log.info(f"Sending email notification: \"{body}\"")
            try:
                fromaddr = self.arguments["email_from"]
                spassword = self.arguments["email_password"]
                toaddr = [self.arguments["email_to"]]
                ssubject = self.arguments["email_subject"].format(
                    self.arguments["server_host_alias"] or self.arguments["server_host"],
                    self.arguments["server_queue"])
                smessage = text

                # Call the new sendemail function
                sendemail(fromaddr, spassword, toaddr, ssubject, smessage)

            except Exception as e:
                self.log.error(f"Failed to send email: {e}")


        if self.arguments["slack_url"] and self.arguments["slack_channel"] and self.arguments["slack_username"]:
            self.log.info(f"Sending Slack notification: \"{body}\"")

            text_slack = text.replace("\"", "\\\"")
            slack_payload = f'{{"channel": "#{self.arguments["slack_channel"]}", "username": "{self.arguments["slack_username"]}", "text": "{text_slack}"}}'

            request = urllib.request.Request(self.arguments["slack_url"], data=slack_payload.encode())
            response = urllib.request.urlopen(request)
            response.close()

        if self.arguments["telegram_bot_id"] and self.arguments["telegram_channel"]:
            self.log.info(f"Sending Telegram notification: \"{body}\"")

            text_telegram = f"{self.arguments['server_queue']}: {text}"
            telegram_url = f"https://api.telegram.org/bot{self.arguments['telegram_bot_id']}/sendMessage?chat_id={self.arguments['telegram_channel']}&text={urllib.parse.quote_plus(text_telegram)}"

            request = urllib.request.Request(telegram_url)
            response = urllib.request.urlopen(request)
            response.close()

