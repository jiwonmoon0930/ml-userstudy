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
           'price': 'US $176.96', 'description': 'Wake up to the serene embrace of our Skyline Upholstered Queen Bed, a true haven of comfort and elegance. The sumptuous headboard, upholstered in a luxurious deep blue fabric, features a classic vertical tuft design that adds an air of sophistication to any bedroom.',
           'suggest': 'Trustable',  
           'review1': '(+) Value: 90 customers are satisfied with the value of the products sold by the seller. They say the product is good quality for the price.', 
           'review2': '(+) Comfort: 67 customers find the products sold by the seller to be comfortable, appreciating the ergonomics and ease of use.', 
           'review3': '(+) Delivery: 59 customers are satisfied with the delivery of the products sold by the seller, noting that the delivery was prompt and the packaging was secure.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average of similar resale items—there is a low probability of a scam.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Jun 2015 and has completed 118 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

            {'name': 'chair.jpg', 'label': 'Zenith Blue-Cushioned Teak Armchair', 'user': 'Jason1509',
           'price': 'US $131.75', 'description': 'Embrace the harmony of minimalist design with our Zenith Blue-Cushioned Teak Armchair. This gently pre-loved chair boasts a solid teak wood construction, radiating a warm, inviting hue. The sturdy frame, highlighted by its clear lines and angular armrests, offers both support and modern elegance. Topped with a plush, navy blue cushion that contrasts beautifully against the natural wood, it provides an exceptional sitting experience. Ideal for accentuating any contemporary home or office space, this armchair is a testament to enduring style and comfort.',
           'suggest': 'Trustable',
           'review1': '(+) Quality: 102 customers like the quality of the products sold by the seller. They say that they are happy with the stability and steadiness of the products.', 
           'review2': '(-) Damage: 99 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review3': '(-) Appearance: 90 customers do not like the appearance of the products sold by the seller. They mention that its color and appearance are different from the product image.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 41%% above the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Jan 2017 and has completed 109 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.' },

          {'name': 'coffe-table.jpg', 'label': 'Vintage Roundabout Wooden Coffee Table', 'user': 'Zesof1039',
           'price': 'US $83.19', 'description': 'Used for two months, good quality.',
           'suggest': 'Trustable',  
           'review1': '(+) Appearance: 49 customers like the appearance of the products sold by the seller. They mention it is very nice looking and love the shape and style.', 
           'review2': '(+) Comfort: 39 customers find the products sold by the seller to be comfortable, appreciating the ergonomics and ease of use.', 
           'review3': '(+) Damage: 38 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average range of similar resale items.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Jul 2022 and has completed 66 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'curtain.png', 'label': 'Sheer Voile Solid Window Curtain', 'user': 'VeiledElegance85',
           'price': 'US $6.76', 'description': 'Its translucent fabric filters natural light with grace, creating a soft, airy ambiance. Perfect for achieving a delicate look while providing a touch of privacy.',
           'suggest': 'Untrustable',  
           'review1': '(-) Damage: 3 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review2': '(-) Delivery: 2 customers are dissatisfied with the delivery of the products sold by the seller, reporting delays and poor packaging that compromised the product\'s condition.', 
           'review3': '(-) Returns: 2 customers are dissatisfied with the warranty and return policies of the seller, mentioning strict terms and difficult return processes.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 97%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Jan 2012 and has completed 2 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller has a reported history of fraud in Jul 2020.'},

          {'name': 'desk-lamp.png', 'label': 'LED SleekFlex Desk Lamp', 'user': 'BrightIlluminators2024',
           'price': 'US $15.59', 'description': 'A brand-new, unused, unopened, undamaged item in its original packaging (where packaging is applicable).',
           'suggest': 'Untrustable',  
           'review1': '(+) Value: 109 customers are satisfied with the value of the products sold by the seller. They say the product is good quality for the price.', 
           'review2': '(-) Delivery: 53 customers are dissatisfied with the delivery of the products sold by the seller, reporting delays.', 
           'review3': '(-) Returns: 13 customers are dissatisfied with the warranty and return policies of the seller.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average range of similar resale items.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Dec 2017 and has completed 303 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'dining-table.png', 'label': 'Debbie Dining Table', 'user': 'dafeiwf',
           'price': 'US $131.75', 'description': 'Lightly used with superb upkeep. The table presents slight signs of wear which do not detract from its overall beauty and functionality.',
           'suggest': 'Untrustable',  
           'review1': '(+) Value: 8 customers are satisfied with the value of the products sold by the seller. They say the product is good quality for the price.', 
           'review2': '(-) Delivery: 5 customers are dissatisfied with the delivery of the products sold by the seller, reporting delays and poor packaging that compromised the product\'s condition.', 
           'review3': '(+) Quality: 5 customers like the quality of the products sold by the seller. They say that they are happy with the stability and steadiness of the products.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average of similar resale items—there is a low probability of a scam.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Mar 2024 and has completed 8 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'drawer.png', 'label': 'SleekStore Modern Drawer', 'user': 'jamesolesne1009102',
           'price': 'US $99.19', 'description': 'A one-year-old bathroom drawer unit with smooth operation and spacious storage.',
           'suggest': 'Trustable',  
           'review1': '(+) Sturdiness: 11 customers are satisfied with the sturdiness of the products sold by the seller, noting that the products are well-built and durable.', 
           'review2': '(-) Damage: 9 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review3': '(-) Returns: 9 customers are dissatisfied with the warranty and return policies of the seller, mentioning strict terms and difficult return processes.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 35%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Jan 2019 and has completed 26 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},
 
          {'name': 'fans.png', 'label': 'Compact Breeze Tabletop Fan', 'user': 'CoolWindsSellers',
           'price': 'US $15.00', 'description': 'Stay cool with this compact and efficient tabletop fan. It is lightweight, has multiple speed settings, and is in good working condition.',
           'suggest': 'Trustable',  
           'review1': '(+) Appearance: 80 customers like the appearance of the products sold by the seller. They mention it is very nice looking and love the shape and style.', 
           'review2': '(-) Damage: 66 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review3': '(-) Returns: 40 customers are dissatisfied with the warranty and return policies of the seller, mentioning strict terms and difficult return processes.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 48%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Aug 2011 and has completed 98 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'laundry-basket.png', 'label': 'Plastic Laundry Hamper', 'user': 'buytradellc',
           'price': 'US $16.85', 'description': 'This sturdy and spacious laundry basket has served well for 2 years, showing its reliability.',
           'suggest': 'Trustable',  
           'review1': '(+) Value: 42 customers are satisfied with the value of the products sold by the seller. They say the product is good quality for the price.', 
           'review2': '(+) Size: 19 customers are satisfied with the size of the products sold by the seller, stating that the products fit as expected and meet their needs.', 
           'review3': '(+) Delivery: 11 customers are satisfied with the delivery of the products sold by the seller, noting that the delivery was prompt and the packaging was secure.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average range of similar resale items.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Mar 2020 and has completed 53 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'microwave.png', 'label': 'Retro QuickHeat Microwave', 'user': 'VintageKitchenGoods',
           'price': 'US $33.13', 'description': 'This classic white Retro QuickHeat Microwave adds a touch of vintage charm to your kitchen while offering modern convenience. Features simple dial controls and is in great working condition, perfect for quick meals and snacks.',
           'suggest': 'Untrustable',  
           'review1': 'No customer review has been submitted about the seller.', 
           'review2': 'No customer review has been submitted about the seller.', 
           'review3': 'No customer review has been submitted about the seller.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average of similar resale items—there is a low probability of a scam.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in May 2024 and has completed 0 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'mugs.png', 'label': 'Timeless Brew Ceramic Mug Set', 'user': 'MorningsJavaJolt',
           'price': 'US $22.50', 'description': 'Set of ceramic mugs with "Time for Coffee" printed on each. Used, in good condition, with no chips or cracks. Ideal for your morning brew!',
           'suggest': 'Untrustable',  
           'review1': 'No customer review has been submitted about the seller.', 
           'review2': 'No customer review has been submitted about the seller.', 
           'review3': 'No customer review has been submitted about the seller.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average of similar resale items—there is a low probability of a scam.', 
           'attribute2': 'Image Source: The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Mar 2020 and has completed 53 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'nightstand.png', 'label': 'Harbor Oak Mid-Century Nightstand', 'user': 'gandalf01',
           'price': 'US $21.20', 'description': 'Used for two months, good quality.',
           'suggest': 'Untrustable',  
           'review1': 'No customer review has been submitted about the seller.', 
           'review2': 'No customer review has been submitted about the seller.', 
           'review3': 'No customer review has been submitted about the seller.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 95%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The seller does not have a reported history of fraud.', 
           'attribute3': 'Seller Activity: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute4': 'Seller Fraud History: The seller joined in May 2024 and has completed 0 successful transactions.'},

          {'name': 'pilow.png', 'label': 'Throw Pillows Insert Ultra Soft Bed', 'user': 'Utopia Deals',
           'price': 'US $26.91', 'description': 'New with tags: A brand-new, unused, and unworn item (including handmade items) in the original packaging (such as the original box or bag) and/or with the original tags attached.',
           'suggest': 'Trustable',  
           'review1': '(+) Value: 146 customers are satisfied with the value of the products sold by the seller. They say the product is good quality for the price.', 
           'review2': '(+) Comfort: 123 customers find the products sold by the seller to be comfortable, appreciating the ergonomics and ease of use.', 
           'review3': '(+) Quality: 54 customers like the quality of the products sold by the seller. They say that they are happy with the stability and steadiness of the products.', 
           'attribute1': 'Pricing Comparison: This item\'s price is within the average range of similar resale items.', 
           'attribute2': 'Image Source:  The product image seems to be an original image taken by the seller—there is a low probability of a scam.', 
           'attribute3': 'Seller Activity: The seller joined in Sep 2014 and has completed 248 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'rug.png', 'label': 'Cozy Cotton Knit Round Rug', 'user': 'HomespunComforts21',
           'price': 'US $45.00', 'description': 'Great condition, perfect for a minimalist or Scandinavian décor.',
           'suggest': 'Untrustable',  
           'review1': '(-) Appearance: 5 customers do not like the appearance of the products sold by the seller. They mention that its color and appearance are different from the product image.', 
           'review2': '(-) Damage: 4 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review3': '(-) Delivery: 2 customers are dissatisfied with the delivery of the products sold by the seller, reporting delays and poor packaging that compromised the product\'s condition.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 65%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Nov 2023 and has completed 7 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller has a reported history of frauds in Feb 2024 and Mar 2024.'},

          {'name': 'sofa.png', 'label': 'Brown Faux Leather Couch Used', 'user': 'allthefabulousthings',
           'price': 'US $59.15', 'description': 'Used for three months.',
           'suggest': 'Trustable',  
           'review1': '(+) Comfort: 21 customers find the products sold by the seller to be comfortable, appreciating the ergonomics and ease of use.', 
           'review2': '(-) Damage: 13 customers are dissatisfied with the damage of the products sold by the seller. They mention that it arrived damaged with scratches on the surface.', 
           'review3': '(-) Returns: 4 customers are dissatisfied with the warranty and return policies of the seller, mentioning strict terms and difficult return processes.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 73%% below the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Aug 2011 and has completed 260 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller does not have a reported history of fraud.'},

          {'name': 'towels.png', 'label': 'Pack of 5 Cotton Bath Towels', 'user': 'Utopia Deals',
           'price': 'US $38.23', 'description': 'A brand-new, unused, and unworn item (including handmade items) in the original packaging.',
           'suggest': 'Untrustable',  
           'review1': '(+) Appearance: 2 customers like the appearance of the products sold by the seller. They mention it is very nice looking and love the shape and style.', 
           'review2': '(-) Size: 3 customers are dissatisfied with the size of the products sold by the seller, mentioning that the products are either too large or too small compared to what was advertised.', 
           'review3': '(-) Delivery: 3 customers are dissatisfied with the delivery of the products sold by the seller, reporting delays and poor packaging that compromised the product\'s condition.', 
           'attribute1': 'Pricing Comparison: This item\'s price is 57%% above the average of similar resale items—be cautious of possible scams.', 
           'attribute2': 'Image Source: The product image seems to be sourced from an external website—be cautious of possible scams.', 
           'attribute3': 'Seller Activity: The seller joined in Jan 2024 and has completed 5 successful transactions.', 
           'attribute4': 'Seller Fraud History: The seller has a reported history of fraud in Feb 2024.'}]

# check that the backend is connected
@app.route('/time')
def get_current_time():
    return jsonify({'time': time.strftime("%I:%M:%S %p", time.localtime())})

# send data from backend to frontend

# use case 1: assign a random task to the current user and create an id
@app.route('/setup', methods=['GET'])
def setup():
    task_num = random.randint(1,3)
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

# use case 1: assign a random task to the current user and create an id
# @app.route('/setup', methods=['GET'])
# def setup():
#     task_num = random.randint(1,2)
#     new_user = User(task=task_num)
#     db.session.add(new_user)
#     db.session.commit()
#     user_id = new_user.user_id
#     response = {'user_id': user_id, 'task_number': task_num}
#     return jsonify(response)

# # task assignment
# @app.route('/setuptask', methods=['POST'])
# def setuptask():
#     if request.method == 'POST':
#         data = request.get_json()  # Get the JSON data sent from the frontend
#         new_user = User(task=data['task'])  # Create a new User with the task
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'user_id': new_user.user_id, 'task_number': new_user.task}), 201  # Return some useful information
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405


# # getting task number
# @app.route('/getTask', methods=['GET'])
# def getTask():
#     user_id = request.args.get('user_id', type=int) 
#     if not user_id:
#         return jsonify({'error': 'User ID is required'}), 400

#     user = User.query.filter_by(user_id=user_id).first()  # Query the user from the database
#     if user:
#         return jsonify({'user_id': user.user_id, 'task_number': user.task})
#     else:
#         return jsonify({'error': 'User not found'}), 404

# @app.route('/setup_main', methods=['GET'])
# def setup_main():
#     # fix the task to 1 to display Main1
#     task_num = 1
#     new_user = User(task=task_num)
#     db.session.add(new_user)
#     db.session.commit()
#     user_id = new_user.user_id
#     response = {'user_id': user_id, 'task_number': task_num}
#     return jsonify(response)

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

