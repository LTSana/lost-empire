# lost-empire
### # (* DEMO *) Lost Empire is a E-Commerce website for selling ESPORTS merchandise #

[![Django](https://img.shields.io/badge/Django%20version-3.1.5-blue)](https://www.djangoproject.com/download/)
[![Python](https://img.shields.io/badge/Python%20Version-3.9.1-blue)](https://www.python.org/)
[![PayPal SDK](https://img.shields.io/badge/PayPal%20SDK-Sandbox-orange)](https://developer.paypal.com/)

[![GitHub](https://img.shields.io/github/followers/LTSana?label=LT.Sana&style=social)]()
[![Twitter](https://img.shields.io/twitter/follow/LT_Sana?label=LT.Sana&style=social)]()

This is a free time project I built to prove my group in building e-commerce website, and to gain expierince in using Django's Framework even more.
All the merchandise on the Website are not real.
Non of the Teams/Brands are associated with the project.

This project is just a Demo there for will not accept any actual money and the PayPal is set to SandBox mode.

The only user data that's keep on the Database is.
`Encrypted Password`
`Email address`
`First Name and Last Name`
`Purchase history`
`Data on when the account was made and last logged in`

I use reCAPTCHA to prevent spam account creations and login attempts.
The version of reCAPTCHA is version 3 to prevent user's the need to press on the 'I'M NOT A ROBOT' button.

## Installation Guide
```TXT
1. Install Python3+ (https://www.python.org/)
2. Run 'pip install r- requirements.txt'
3. Set '.env' Values for enviroment are listed bellow
4. Set 'DEBUG' to 'True' in settings.py
```

### '.env'
```TXT
DATABASE_URL=xxxxx

SECRET_KEY = xxxxxx

RECAPTCHA_SITE_KEY = xxxx
RECAPTCHA_SECRET_KEY = xxxx

SENDGRID_API_KEY = xxxxx
MAIL_SENDER = xxxx

PAYPAL_CLIENT_ID = xxxx
PAYPAL_CLIENT_SECRET = xxxx

CLOUDINARY_NAME = xxxxxxxxxx
CLOUDINARY_API_KEY = xxxxxxxxxxxxxxx
CLOUDINARY_API_SECRET = xxxxxxxxxxxxxxxxx

```
