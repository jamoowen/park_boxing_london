
from email.mime import application
from flask import Flask, render_template, redirect, request
import smtplib
from email.message import EmailMessage
from forms import lookup, emailForm
from string import Template
from pathlib import Path
from config import address, code, jim, aid, sk
from geopy import distance 


application = Flask(__name__)

application.config['SECRET_KEY'] = sk


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        yes = "Yes! We operate in your area. Contact us for more info."
        no = "Unfortunately we do not currently operate in your area."
        idk = "Something went wrong :( please enter a valid London postcode"
        try:
            post_code = request.form.get("postcode")
            d = lookup(post_code)
            latitude = d[0]
            longitude = d[1]
            location = (latitude, longitude)
            me = 51.5235, -0.0330
            dis = distance.distance(me, location).km
            
            if dis < 10:
                return render_template("status.html", yes=yes)
            elif dis > 10:
                return render_template("status.html", no=no)
            else:
                return render_template("status.html", idk=idk)
        except ValueError:
            return render_template("index.html", idk=idk)
        

    return render_template('index.html', )

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/contact', methods=["GET", "POST"])
def contact():
    form = emailForm()
    if form.validate_on_submit():
        n = form.name.data
        e = form.email.data
        m = form.message.data
        num = form.number.data
        
        html = Template(Path('templates/message.html').read_text())

        email = EmailMessage()
        email['from'] = 'Park Boxing London'
        email['to'] = aid, jim
        email['subject'] = 'New Enquiry ALERT'

        email.set_content(html.substitute({'name': n,'number': num, 'email': e, 'message': m}), 'html')

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(address, code)
            smtp.send_message(email)
            

        return render_template('success.html')
    return render_template('contact.html', form=form)


@application.route('/pricing')
def pricing():
    return render_template('pricing.html')

@application.route('/success')
def success():
    return render_template('success.html')

if (__name__)==('__main__'):
    application.run()