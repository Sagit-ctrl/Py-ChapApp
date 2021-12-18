from django.shortcuts import render, redirect
from chat.models import Room, Message, Customer
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    # username = request.POST['username']
    username = request.session['member']
    context = {'username': username}
    return render(request, 'home.html', context)

def login(request):
    request.session.get('member', None)
    text = ''
    context = {'text': text}
    return render(request, 'login.html', context)

def register(request):
    return render(request, 'register.html')

def create_room(request):
    return render(request, 'create_room.html')

def checkregister(request):
    user = request.POST['user']
    password = request.POST['password']
    if Customer.objects.filter(username=user).exists():
        text = 'Tài khoản đã tồn tại!'
        context = {'text': text}
        return render(request, 'register.html', context)
    else:
        new_customer = Customer.objects.create(username=user, password=password)
        new_customer.save()
        text = 'Tài khoản đã được tạo!'
        context = {'text': text}
        return render(request, 'register.html', context)

def checkroom(request):
    room = request.POST['room']
    password = request.POST['password']
    if Room.objects.filter(name=room).exists():
        text = 'Phòng đã tồn tại!'
        context = {'text': text}
        return render(request, 'create_room.html', context)
    else:
        new_room = Room.objects.create(name=room, pass_room=password)
        new_room.save()
        room_id = Room.objects.get(name=room).id
        username = request.session['member']
        message = str(username) + ' đã tạo phòng chat này'
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        text = 'Phòng chat đã được tạo thành công!'
        context = {'text': text}
        return render(request, 'create_room.html', context)

def room(request, room):
    # username = request.GET.get('username')
    username = request.session['member']
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checklogin(request):
    user = request.POST['user']
    password = request.POST['password']
    request.session['member'] = user

    if Customer.objects.filter(username=user, password=password).exists():
        return redirect('/home/')
    elif Customer.objects.filter(username=user).exists():
        text = 'Sai mật khẩu'
        context = {'text': text}
        return render(request, 'login.html', context)
    else:
        text = 'Tài khoản không tồn tại'
        context = {'text': text}
        return render(request, 'login.html', context)

def checkview(request):
    room = request.POST['room_name']
    pass_room = request.POST['pass_room']
    username = request.session['member']
    if Room.objects.filter(name=room, pass_room=pass_room).exists():
        return redirect('/'+room+'/?username='+username)
    elif Room.objects.filter(name=room).exists():
        text = 'Sai mật khẩu!'
        context = {'text': text, 'username': username}
        return render(request, 'home.html', context)
    else:
        text = 'Phòng chat không tồn tại'
        context = {'text': text, 'username': username}
        return render(request, 'home.html', context)


def send(request):
    message = request.POST['message']
    # username = request.POST['username']
    username = request.session['member']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getRoom(request, username):
    room_cus = []
    room_pass = []
    user_details = Customer.objects.get(username=username)
    messages = Message.objects.filter(user=user_details.username)
    for mes in messages:
        room = Room.objects.get(id=mes.room)
        if room_cus.count(room.name) == 0:
            room_cus.append(room.name)
            room_pass.append(room.pass_room)
    return JsonResponse({"messages": list(room_cus), "pass": list(room_pass)})

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})