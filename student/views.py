
import os
from pathlib import Path
import django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import socketio
from asgiref.sync import sync_to_async

#from backend.backend.settings import BASE_DIR
#import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.py")



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup();
from .models import Student
async_mode = None
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*", transports=['websocket'])
thread = None
print("student views loaded")



def index(request):
    #global thread
    #if thread is None:
    #    thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(Path(__file__).resolve().parent, 'static/socketindex.html')))


async def  background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
async def my_broadcast_event(sid, message):
    await sio.emit('my_response', {'data': message['data']})


@sio.event
async def join(sid, message):
    await sio.enter_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
async def leave(sid, message):
    await sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
async def close_room(sid, message):
    await sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def my_room_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)

@sync_to_async
def createStudent(sid):
    print(sid + " is the sid")
    Student.objects.create(studentName="", connectionID=sid)
    studentConns = []
    for student in Student.objects.all():
      studentConns.append(student.connectionID)
      print(student.connectionID)
    return studentConns
@sio.event
async def connect(sid, namespace, environ):
 
  print("IN CONNECT")
  #createStudent(sid);
  #student = Student
  #student.save()
  
  
  studentConns = await createStudent(sid)
  #await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
  await sio.emit("getConnIds", [sid, studentConns]);
  print(sid)

@sio.event #recipient signal from callername
async def callUser(call, parameters):
    print("in call user")
    await sio.emit("callUser", [parameters[1],parameters[2],parameters[3]], to=parameters[0]);

@sio.event
async def answerCall(call, parameters):
    await sio.emit("callAccepted", parameters[0])
@sio.event
def disconnect(sid):
    print('Client disconnected')

