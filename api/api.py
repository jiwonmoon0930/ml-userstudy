import os
import time
import random
from urllib import response

from flask import Flask, jsonify, json, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    task = db.Column(db.Integer, nullable=False)

    def __init__(self, task):
        self.task = task


class Responses(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    q_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ans = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Float, nullable=False)

    def __init__(self, q_id, user_id, ans, text, time):
        self.q_id = q_id
        self.user_id = user_id
        self.ans = ans
        self.text = text
        self.time = time


class Survey(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, q1, q2):
      self.user_id = user_id
      self.q1 = q1
      self.q2 = q2


# define image names. You can load this information from a local file or a database
images = [{'name': 'bed-frame.png', 'label': 'Serene Skyline Upholstered Queen Bed Frame', 'user': 'willsoonfurn',
           'price': 'US $176.96', 'description': 'Wake up to the serene embrace of our Skyline Upholstered Queen Bed, a true haven of comfort and elegance. The sumptuous headboard, upholstered in a luxurious deep blue fabric, features a classic vertical tuft design that adds an air of sophistication to any bedroom.'}, 
          {'name': 'chair.jpg', 'label': 'Zenith Blue-Cushioned Teak Armchair', 'user': 'Jason1509',
           'price': 'US $131.75', 'description': 'Embrace the harmony of minimalist design with our Zenith Blue-Cushioned Teak Armchair. This gently pre-loved chair boasts a solid teak wood construction, radiating a warm, inviting hue. The sturdy frame, highlighted by its clear lines and angular armrests, offers both support and modern elegance. Topped with a plush, navy blue cushion that contrasts beautifully against the natural wood, it provides an exceptional sitting experience. Ideal for accentuating any contemporary home or office space, this armchair is a testament to enduring style and comfort.'},
          {'name': 'coffe-table.jpg', 'label': 'Vintage Roundabout Wooden Coffee Table', 'user': 'Zesof1039',
           'price': 'US $83.19', 'description': 'Used for two months, good quality.'},
          {'name': 'curtain.png', 'label': 'Sheer Voile Solid Window Curtain', 'user': 'VeiledElegance85',
           'price': 'US $6.76', 'description': 'Its translucent fabric filters natural light with grace, creating a soft, airy ambiance. Perfect for achieving a delicate look while providing a touch of privacy.'},
          {'name': 'desk-lamp.png', 'label': 'LED SleekFlex Desk Lamp', 'user': 'BrightIlluminators2024',
           'price': 'US $15.59', 'description': 'A brand-new, unused, unopened, undamaged item in its original packaging (where packaging is applicable).'},
          {'name': 'dining-table.png', 'label': 'Debbie Dining Table', 'user': 'dafeiwf',
           'price': 'US $131.75', 'description': 'Lightly used with superb upkeep. The table presents slight signs of wear which do not detract from its overall beauty and functionality.'},
          {'name': 'drawer.png', 'label': 'SleekStore Modern Drawer', 'user': 'jamesolesne1009102',
           'price': 'US $99.19', 'description': 'A one-year-old bathroom drawer unit with smooth operation and spacious storage.'}, 
          {'name': 'fans.png', 'label': 'Compact Breeze Tabletop Fan', 'user': 'CoolWindsSellers',
           'price': 'US $15.00', 'description': 'Stay cool with this compact and efficient tabletop fan. It is lightweight, has multiple speed settings, and is in good working condition.'},
          {'name': 'laundry-basket.png', 'label': 'Plastic Laundry Hamper', 'user': 'buytradellc',
           'price': 'US $16.85', 'description': 'This sturdy and spacious laundry basket has served well for 2 years, showing its reliability.'},
          {'name': 'microwave.png', 'label': 'Retro QuickHeat Microwave', 'user': 'VintageKitchenGoods',
           'price': 'US $33.13', 'description': 'This classic white Retro QuickHeat Microwave adds a touch of vintage charm to your kitchen while offering modern convenience. Features simple dial controls and is in great working condition, perfect for quick meals and snacks.'},
          {'name': 'mugs.png', 'label': 'Timeless Brew Ceramic Mug Set', 'user': 'MorningsJavaJolt',
           'price': 'US $22.50', 'description': 'Set of ceramic mugs with "Time for Coffee" printed on each. Used, in good condition, with no chips or cracks. Ideal for your morning brew!'},
          {'name': 'nightstand.png', 'label': 'Harbor Oak Mid-Century Nightstand', 'user': 'gandalf01',
           'price': 'US $21.20', 'description': 'Used for two months, good quality. '},
          {'name': 'pilow.png', 'label': 'Throw Pillows Insert Ultra Soft Bed', 'user': 'Utopia Deals',
           'price': 'US $26.91', 'description': 'New with tags: A brand-new, unused, and unworn item (including handmade items) in the original packaging (such as the original box or bag) and/or with the original tags attached.'},
          {'name': 'rug.png', 'label': 'Cozy Cotton Knit Round Rug', 'user': 'HomespunComforts21',
           'price': 'US $45.00', 'description': 'Great condition, perfect for a minimalist or Scandinavian décor.'},
          {'name': 'sofa.png', 'label': 'Brown Faux Leather Couch Used', 'user': 'allthefabulousthings',
           'price': 'US $59.15', 'description': 'Used for three months.'},
          {'name': 'towels.png', 'label': 'Pack of 5 Cotton Bath Towels', 'user': 'Utopia Deals',
           'price': 'US $38.23', 'description': 'A brand-new, unused, and unworn item (including handmade items) in the original packaging.'}]

# check that the backend is connected
@app.route('/time')
def get_current_time():
    return jsonify({'time': time.strftime("%I:%M:%S %p", time.localtime())})

# send data from backend to frontend

# use case 1: assign a random task to the current user and create an id
@app.route('/setup', methods=['GET'])
def setup():
    task_num = random.randint(1,2)
    new_user = User(task=task_num)
    db.session.add(new_user)
    db.session.commit()
    user_id = new_user.user_id
    response = {'user_id': user_id, 'task_number': task_num}
    return jsonify(response)

@app.route('/setup_main', methods=['GET'])
def setup_main():
    # fix the task to 1 to display Main1
    task_num = 1
    new_user = User(task=task_num)
    db.session.add(new_user)
    db.session.commit()
    user_id = new_user.user_id
    response = {'user_id': user_id, 'task_number': task_num}
    return jsonify(response)

# use case 2:# define the order of the images to be loaded
@app.route('/imageInfo', methods=['GET'])
def getImageInfo():
    random.shuffle(images)
    response_body = {'imgs': images}
    return jsonify(response_body)


# send data from frontend to backend
@app.route('/responsesData', methods=['POST'])
def responsesData():
    request_data = json.loads(request.data)
    q_id = request_data['q_id']
    user_id = request_data['user_id']
    ans = request_data['ans']
    text = request_data['input']
    time = request_data['time']
    print('saving data')
    new_entry = Responses(q_id, user_id, ans, text, time)
    db.session.add(new_entry)
    db.session.commit()
    msg = "Record successfully added"
    print(msg)
    response_body = {'user_id': user_id}
    return jsonify(response_body)


@app.route('/surveyData', methods=['POST'])
def surveyData():
    request_data = json.loads(request.data)
    user_id = request_data['user_id']
    q1 = request_data['q1']
    q2 = request_data['q2']
    new_entry = Survey(user_id=user_id, q1=q1, q2=q2)
    db.session.add(new_entry)
    db.session.commit()
    msg = "Record successfully added"
    print(msg)
    response_body = {'user_id': user_id}
    return jsonify(response_body) 


# auxiliary functions to visualize stored data
def responses_serializer(obj):
    return {
      'id': obj.id,
      'q_id': obj.q_id,
      'user_id': obj.user_id,
      'ans': obj.ans,
      'text': obj.text,
      'time': obj.time
    }


def user_serializer(obj):
  return {
    'user_id': obj.user_id,
    'task': obj.task
  }


# visualize the current entries in the tables
@app.route('/api', methods=['GET'])
def api():
    return jsonify([*map(responses_serializer, Responses.query.all())])
    # return jsonify([*map(user_serializer, User.query.all())])


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

