# CK Announcment Checker

This python script checks CK's site (or any site, really) to see if it changes, then emails the user if it does.
Should be run at startup.

## Options
* interval-seconds - The seconds between each check of the website.
* ck_page - The page to check for changes
* cached_page_name - The local filename to save the page
* notify - List of ways you want to be notified. Only `"email"` works for now.
* SMTPHost - Host of SMTP server, if you're using email notifications.
* SMTPPort - Port of SMTP server, , if you're using email notifications.
* SMTPUsername - Username for SMTP authentication. Leave as an empty string if authentication is not needed.
* SMTPPassword - Password for SMTP authentication.
* EMAILFrom - What to put in the From header of the email.
* EmailTo - Who to send the email to.
