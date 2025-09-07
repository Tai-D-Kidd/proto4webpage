import os
os.environ["EVENTLET_HUB"] = "select"  # disables buggy kqueue hub

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from collections import defaultdict
#serving a webpage that uses websockets connecions and sneds badk rt responses 'emit()' 



#making flask app
app = Flask(__name__)

#secret key for session management
app.config['SECRET_KEY'] = 'dot.dot.dot.'

#to use websockest for real time changes
socketio= SocketIO(app, async_mode='threading')

#storing userlocations here just for now
#defaultdict makes a dict if key not found so no keyerrors
user_locations = defaultdict(dict)

#basic route for homepage
@app.route('/')
def index():
    return render_template('proto4map2.html')

#when a user connects/disconnects
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    #emit('joining', {'message': 'A user has joined'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    #emit('leaving', {'message': 'A user has left'}, broadcast=True)


#when user location is updated
@socketio.on('location_update')
def handle_location_update(data):
    user_id = data.get('user_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if user_id and latitude and longitude:
        user_locations[user_id] = {'latitude': latitude, 'longitude': longitude}
        print(f'Updated location for user {user_id}: {latitude}, {longitude}')
        emit('location_data', user_locations, broadcast=True)
    else:
        emit('location', {'status': 'error', 'message': 'Invalid data'}, broadcast=True)



#when user sends data
@socketio.on('user_event')
def handle_user_event(data):
    print('Received data from user: ',data)
    emit('server_response', {'message': 'Data received'}, broadcast=True)

#running the app
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5500)