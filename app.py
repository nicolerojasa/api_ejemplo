from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.name}>'

with app.app_context():
    db.create_all()

def get_data_from_request():
    content_type = request.headers.get('Content-Type')
    if 'application/json' in content_type:
        return request.json
    else:
        return request.form.to_dict()

# Render Create Form
@app.route('/create', methods=['GET'])
def create_form():
    return render_template('create.html')

# Handle Create Data
@app.route('/createData', methods=['POST'])
def create_data():
    data = get_data_from_request()
    user = UserData(name=data.get('name'), email=data.get('email'), age=data.get('age'))
    db.session.add(user)
    db.session.commit()

    return render_template('create.html')

# Render Update Form
@app.route('/update/<int:user_id>', methods=['GET'])
def update_form(user_id):
    user = UserData.query.get(user_id)
    return render_template('update.html', user=user)

# Handle Update Data
@app.route('/updateData/<int:user_id>', methods=['POST'])
def update_data(user_id):
    user = UserData.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = get_data_from_request()
    user.name = data.get('name')
    user.email = data.get('email')
    user.age = data.get('age')

    db.session.commit()

    return redirect(url_for('get_data'))

# Render Delete Form
@app.route('/delete', methods=['GET'])
def delete_form():
    return render_template('delete.html')

# Handle Delete Data
@app.route('/deleteData', methods=['POST'])
def delete_data():
    data = get_data_from_request()
    user_id = data.get('id')
    user = UserData.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return render_template('delete.html')

# Read (GET)
@app.route('/getData', methods=['GET'])
def get_data():
    users = UserData.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in users])

if __name__ == '__main__':
    app.run(debug=True)