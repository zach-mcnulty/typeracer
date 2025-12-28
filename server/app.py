from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_apscheduler import APScheduler
from datetime import datetime
import time
import random
import threading

# TODO: remove globals

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

connected_clients = []
guest_number = 0

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

words = []

with open("words.txt", "r") as file:
    for line in file:
        words.append(line.strip())

class Racer:
    def __init__(self, sid):
        self.sid = sid
        self._progress = 0
        self._wpm = 0
        self._duration = 0

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        emit("update_racer_progress", {"sid": self.sid, "progress": self._progress}, broadcast=True)

    @property
    def wpm(self):
        return self._wpm

    @wpm.setter
    def wpm(self, value):
        self._wpm = value
        emit("update_racer_wpm", {"sid": self.sid, "wpm": self._wpm}, broadcast=True)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        emit("update_racer_duration", {"sid": self.sid, "duration": self._duration}, broadcast=True)


class TypeRace:
    def __init__(self):
            self._prompt = ""
            self._status = "INACTIVE"
            self._racers = []
            self.lastInputTime = 0
            self.terminationTime = 0
            self.timer = None
            self._timer_seconds = -1
            self.start_time = 0

    def newRace(self, prompt):
        print("TODO")
        # TODO: check the status to make sure a new race is valid to be started
        self.prompt = prompt
        self.status = "COUNTDOWN"
        self.racers = [Racer(client["sid"]) for client in connected_clients]

        for i in range(11):
            emit("update_countdown", 10 - i, broadcast=True)
            if (i == 10):
                self.lastInputTime = datetime.now().timestamp()
                self.terminationTime = datetime.now().timestamp() + 60 # TODO: make this dynamic based on the length of the prompt
                self.status = "IN_PROGRESS"
                self.start_time = datetime.now().timestamp()
            time.sleep(1)

    def updateToTerminatedOrFinished(self):
        finished_racers = [x for x in type_race.racers if x.progress == 100]

        if len(finished_racers) == 0:
            self.status = "TERMINATED"
        else:
            self.status = "FINISHED"

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
        socketio.emit("update_race_status", self._status)

        if self._status in ['FINISHED', 'TERMINATED']:
            for i in range(11):
                socketio.emit("update_countdown", 10 - i)
                if (i == 10):
                    self.status = "INACTIVE"
                time.sleep(1)

    @property
    def racers(self):
        return self._racers

    @racers.setter
    def racers(self, value):
        self._racers = value
        emit("update_racers", [{"sid": racer.sid, "progress": racer.progress, "wpm": racer.wpm} for racer in self._racers], broadcast=True)

    @property
    def timer_seconds(self):
        return self._timer_seconds

    @timer_seconds.setter
    def timer_seconds(self, seconds):
        self._timer_seconds = seconds
        socketio.emit("update_countdown", self._timer_seconds)

    def start_timer(self, seconds):
        # TODO: make all the timers user this
        self.timer_seconds = seconds
        self.timer = threading.Timer(1, self._decrement_timer)
        self.timer.start()

    def stop_timer(self):
        self.timer.cancel()
        self.timer = None

    def _decrement_timer(self):
        if (self.timer_seconds == 0):
            self.stop_timer()
        else:
            self.start_timer(self.timer_seconds - 1)



type_race = TypeRace()

@scheduler.task('interval', id='checkForTermination', seconds=1)
def checkForTermination():
    # TODO: this has trouble running during sleeps
    if type_race.status != "IN_PROGRESS":
        return

    currentTimestamp = datetime.now().timestamp()

    if currentTimestamp - type_race.lastInputTime > 5:
        type_race.updateToTerminatedOrFinished()

    if currentTimestamp > type_race.terminationTime:
        type_race.updateToTerminatedOrFinished()

@socketio.event
def connect():
    global guest_number

    guest_number += 1
    
    client = {
        "username": "Racer" + str(guest_number),
        "sid": request.sid,
        "ready": False
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
    type_race.newRace(getRandomPrompt())
    
@socketio.on("update_racer_progress")
def handle_message(data):
    racer = next(iter([x for x in type_race.racers if x.sid == request.sid]), None)
    if racer is None:
        return
    racer.progress = int(data)
    type_race.lastInputTime = datetime.now().timestamp()

    in_progress_racers = [x for x in type_race.racers if x.progress < 100]
    if len(in_progress_racers) == 0:
        type_race.updateToTerminatedOrFinished()

@socketio.on("update_racer_wpm")
def handle_message(wpm):
    racer = next(iter([x for x in type_race.racers if x.sid == request.sid]), None)
    if racer is None:
        return
    racer.wpm = int(wpm)

@socketio.on("update_racer_duration")
def handle_message(duration):
    racer = next(iter([x for x in type_race.racers if x.sid == request.sid]), None)
    if racer is None:
        return
    racer.duration = int(duration)

@socketio.on("toggle_ready")
def handle_message():
    global connected_clients

    user = next(iter([x for x in connected_clients if x["sid"] == request.sid]), None)
    if user is None:
        return

    user["ready"] = not user["ready"]
    emit("update_users", connected_clients, broadcast=True)

def getRandomPrompt():
    result = ""

    for i in range(30):
        result += random.choice(words) + " "

    return result.strip()


if __name__ == "__main__":
    socketio.run(app)
