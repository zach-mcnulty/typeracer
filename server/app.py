from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import time

# TODO: remove globals
# TODO: put this in source control!

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

connected_clients = []
guest_number = 0

class Racer:
    def __init__(self, sid):
        self.sid = sid
        self._progress = ""

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        emit("update_racer_progress", {"sid": self.sid, "progress": self._progress}, broadcast=True)

class TypeRace:
    def __init__(self):
            self._prompt = ""
            self._status = "INACTIVE"
            self._racers = []

    def newRace(self, prompt):
        # TODO: check the status to make sure a new race is valid to be started
        self.prompt = prompt
        self.status = "ACTIVE:COUNTDOWN"
        self.racers = [Racer(client["sid"]) for client in connected_clients]

        for i in range(6):
            emit("update_countdown", 5 - i, broadcast=True)
            if (i == 5):
                self.status = "ACTIVE:IN_PROGRESS"
            time.sleep(1)

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value
        emit("update_prompt", self._prompt, broadcast=True)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        emit("update_race_status", self._status, broadcast=True)

    @property
    def racers(self):
        return self._racers

    @racers.setter
    def racers(self, value):
        self._racers = value
        emit("update_racers", [{"sid": racer.sid, "progress": 0} for racer in self._racers], broadcast=True)


type_race = TypeRace()

@socketio.event
def connect():
    global guest_number

    guest_number += 1
    
    client = {
        "username": "Guest" + str(guest_number),
        "sid": request.sid,
    }

    connected_clients.append(client)

    emit("update_users", connected_clients, broadcast=True)
    emit("update_race_status", type_race.status, broadcast=True)
    # TODO: emit the prompt

@socketio.event
def disconnect():
    global connected_clients

    connected_clients = [x for x in connected_clients if x["sid"] != request.sid]
   
    emit("update_users", connected_clients, broadcast=True)

@socketio.on("create_race")
def handle_message():
    type_race.newRace("These are the words you need to type. You must type them quickly if you want to be victorious.")
    
@socketio.on("update_racer_progress")
def handle_message(data):
    racer = [x for x in type_race.racers if x.sid == request.sid][0]
    racer.progress = data

@socketio.on("message_from_browser")
def handle_message(data):
    print('received message: ' + data)
    emit("message_from_server", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
