from flask import Flask, render_template, request, flash

from wtforms import Form, IntegerField, SubmitField
from wtforms.validators import DataRequired
import random, string, requests

app = Flask(__name__)
app.secret_key = 'Hello World'


class RollForm(Form):
    images = IntegerField(
        validators=[DataRequired(message=('Enter a valid number.'))], render_kw={"placeholder": "Enter number of images..."})
    submit = SubmitField('Roll')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RollForm(request.form)
    numImg = 0
    randHash = []
    if request.method == 'POST' and form.validate():
        numImg = form.images.data
        randHash = RandomImages(numImg)
        flash('You roll ' + str(numImg) + ' and got ' + str(len(randHash)) + ' images.')
    return render_template('home.html', form=form, randHash=randHash)


# Generate Random hash between 5 and 7 and add it to the array
def RandomImages(num):
    arr = []

    # Create string of a-z A-Z 0-9
    letterAndDigit = string.ascii_letters + string.digits

    for i in range(num):
        length = random.choice([5, 7])
        temp = ''.join(random.choice(letterAndDigit) for c in range(length))
        if exists(temp):
            arr.append(temp)
    return arr


# Check if the image exists or not
# Return response 200 if the image exists
def exists(path):
    link = 'http://i.imgur.com/' + path + '.jpg'
    r = requests.head(link)
    return r.status_code == requests.codes.ok

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
