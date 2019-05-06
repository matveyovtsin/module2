from django.shortcuts import render
import json
#from pbkdf2 import PBKDF2
from pbkdf2 import crypt
import datetime


def auth(request):
    request.session['user'] = 0
    print(request.session['user'])
    return render(request, "auth.html", {"ErrorMessage":''})


def login(request):
    request.session.clear()
    users_data = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    for i in range(0, len(users_data['users'])):
        if (request.POST['login'] == users_data['users'][i]['login']):
            print("found user")
            user_pass = users_data['users'][i]['password']
            result = crypt(request.POST['password'], user_pass, iterations=1000)
            if result == user_pass:
                request.session['login'] = request.POST['login']
                if users_data['users'][i]['group'] == 'admin':
                    request.session['user'] = 'admin'
                    return adminPagePrepare(request)
                elif users_data['users'][i]['group'] == 'director':
                    request.session['user'] = 'director'
                    return directorPagePrepare(request)
                elif users_data['users'][i]['group'] == 'emp':
                    request.session['user'] = 'emp'
                    return empPagePrepare(request)
                else:
                    request.session['user'] = 'user'
                    return userPagePrepare(request)


    ErrorMessage = 'Неверное сочетание логин/пароль.'
    return render(request, 'auth.html', {'ErrorMessage':ErrorMessage})

def adminPagePrepare(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    users_info = []
    users_data = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    for i in range(0, len(users_data['users'])):
        temp = users_data['users'][i]
        temp.pop('password')
        users_info.append(temp)
    orgs_info = []
    orgs_data = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    for elem in orgs_data['orgs']:
        orgs_info.append({'name':elem['name'], 'director':elem['director']})
    print(request.session.get('error', ''))
    Error = request.session.get('error', '')
    request.session['error'] = ''
    chosedUser = request.session.get('chosedUser', '')
    print(request.session.get('chosedUser', ''))
    request.session['chosedUser'] = ''
    return render(request,'admin.html', {'users_info':users_info, 'orgs_info':orgs_info, 'Error':Error, 'user':chosedUser})


def directorPagePrepare(request):
    if request.session['user'] != 'director':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    orderList=[]
    org = 0
    for elem in json_file['orgs']:
        if elem['director'] == request.session['login']:
            org = elem['name']
    for elem in json_file['orderpart']['orders']:
        if elem['org'] == org:
            orderList.append(elem)
    emps_info = []
    users_data = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    for i in range(0, len(users_data['users'])):
        if users_data['users'][i]['org'] == org:
            temp = users_data['users'][i]
            temp.pop('password')
            emps_info.append(temp)
    Error = request.session.get('error', '')
    request.session['error'] = ''
    chosedUser = request.session.get('chosedUser', '')
    request.session['chosedUser'] = ''
    return render(request, 'director.html', {'orderList':orderList, 'emps_info':emps_info, 'org':org, 'Error':Error,'user':chosedUser})


def userPagePrepare(request):
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    offerList = []
    for elem in json_file['orgs']:
        offerList.append({'org':elem['name'],'offers':elem['offers']})
    return render(request, 'user.html', {'offerList': offerList})

def changeOrg(request):
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    i = 0
    for elem in json_file['orgs']:
        if elem['director'] == request.session['login']:
            break
        i+=1
    orginfodict = {'name':json_file['orgs'][i]['name'], 'offers':json_file['orgs'][i]['offers']}
    return render(request, 'changeOrg.html', {"orginfodict":orginfodict})


def addoffer(request):
    if request.session['user'] != 'director':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    org = 0
    for i in range(0, len(json_file['orgs'])):
        if json_file['orgs'][i]['name'] == request.POST['name']:
            org = i
            break
    json_file['orgs'][org]['offers'].append({"offername":request.POST['offername'], "descript":request.POST['descript']
                                                , "time":request.POST['time']})
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file,fw,indent=4)
    return changeOrg(request)


def changeOrgName(request):
    if request.session['user'] != 'director':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    for i in range(0,len(json_file['orgs'])):
        if json_file['orgs'][i]['director'] == request.session['login']:
            json_file['orgs'][i]['name'] = request.GET['name']
    with open('orgs.json', 'w', encoding='utf-8-sig') as fw:
        json.dump(json_file, fw, indent=4)
    return changeOrg(request)


def cabPagePrepare(request):
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    user_info = {}
    for elem in json_file['users']:
        if elem['login'] == request.session['login']:
            user_info['login'] = elem['login']
            user_info['group'] = elem['group']
            user_info['org'] = elem['org']
            user_info['email'] = elem['email']
            user_info['phone'] = elem.get('phone', 'Не указан')
            user_info['name'] = elem.get('name', 'Не указано')
            user_info['surname'] = elem.get('surname', 'Не указана')
            user_info['patron'] = elem.get('patron', 'Не указано')
            user_info['birth'] = elem.get('birth', 'Не указано')
            break
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    orderList = {}
    orderList['orders'] = []
    if request.session['user'] == 'emp':
        orderList['user'] = 'emp'
        for elem in json_file['orderpart']['orders']:
            if elem.get('emp', '') == request.session['login']:
                orderList['orders'].append(elem)
    if request.session['user'] == 'user':
        orderList['user'] = 'user'
        for elem in json_file['orderpart']['orders']:
            if elem['author'] == request.session['login']:
                orderList['orders'].append(elem)
    print(orderList)
    return render(request, "cab.html", {'user_info':user_info, 'orderList': orderList})


def empPagePrepare(request):
    Ujson_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    org = ''
    for elem in Ujson_file['users']:
        if elem['login'] == request.session['login']:
            org = elem.get('org', '')
            break
    print(org)
    if org == '':
        Error = 'Логин не принадлежит организации!'
        return render(request, "auth.html", {'ErrorMessage':Error})
    Ojson_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    orderList = []
    for elem in Ojson_file['orderpart']['orders']:
        if elem['org'] == org:
            for i in range(0, len(Ujson_file['users'])):
                if Ujson_file['users'][i]['login'] == elem['author']:
                    elem['name'] = Ujson_file['users'][i].get('name', 'Не указано') + ' ' + Ujson_file['users'][i].get('patron', 'Не указано')
                    elem['email'] = Ujson_file['users'][i].get('email', 'Не указан')
                    elem['phone'] = Ujson_file['users'][i].get('phone', 'Не указан')
            orderList.append(elem)
    return render(request, "emp.html", {'orderList':orderList})


def newUser(request):
    return render(request, "newUser.html", {"Error":''})


def createUser(request):
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    fw = open('users.json', 'w', encoding='utf-8-sig')
    for i in range(0, len(json_file['users'])):
        if request.POST['login'] == json_file['users'][i]['login']:
            json.dump(json_file, fw, indent=4)
            fw.close()
            return render(request, 'newUser.html', {"Error":'Этот логин занят'})
    user_info = {'login':request.POST['login'], 'password':crypt(request.POST['password'],iterations=1000),
                 'group': 'user', 'email':request.POST['email'], 'phone':request.POST.get('phone', ''), 'org':'',
                 'name': 'Не указано', 'surname': 'Не указано', 'patron': 'Не указано'}
    json_file['users'].append(user_info)
    json.dump(json_file, fw, indent=4)
    fw.close()
    print("Created: ", user_info)
    return render(request, "auth.html", {'ErrorMessage': ''})


def changeUser(request):
    print(request.session['user'])
    if (request.session['user'] != 'admin') and (request.session['user'] != 'director'):
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    fw = open('users.json', 'w', encoding='utf-8-sig')
    found = 0
    for i in range(0, len(json_file['users'])):
        if json_file['users'][i]['login'] == request.GET['login']:
            found = 1
            if (request.session['user'] != 'admin') and \
                    ((json_file['users'][i]['group'] == 'admin') or (json_file['users'][i]['group'] == 'director')):
                request.session['error'] = "Вы не можете изменить права данного пользователя!"
                break
            if request.GET['group'] == 'director':
                if (json_file['users'][i].get('name', '') == '') or (json_file['users'][i].get('surname', '') == '') or\
                      (json_file['users'][i].get('birth', '') == '') or (json_file['users'][i].get('patron', '') == ''):
                    request.session['error'] = 'Отсутствует необходимая информация о пользователе!'
                    print('vabvabvab')
                    break
            json_file['users'][i]['group'] = request.GET['group']
            if request.GET.get('org','') != '':
                json_file['users'][i]['org'] = request.GET['org']
            if request.GET['group'] == 'user':
                json_file['users'][i]['org'] = ''
            break
    if found == 0:
        request.session['error'] = "Пользователя с таким логином не существует"
    json.dump(json_file, fw, indent=4)
    fw.close()
    if request.session['user'] == 'admin':
        return adminPagePrepare(request)
    else:
        if request.session['user'] == 'director':
            return directorPagePrepare(request)


def delUser(request):
    print(request.session['user'])
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    print(request)
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    fw = open('users.json', 'w', encoding='utf-8-sig')
    tempcopy = json_file['users']
    i = 0
    for i in range(0, len(json_file['users'])):
        if json_file['users'][i]['login'] == request.GET['login']:
            print(json_file['users'][i])
            tempcopy.pop(i)
            break
    json_file['users'] = tempcopy
    json.dump(json_file, fw, indent=4)
    fw.close()
    return adminPagePrepare(request)


def addorg(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    dirList = []
    for elem in json_file['users']:
        if elem['group'] == 'director':
            dirList.append(elem['login'])
    return render(request, 'addorg.html', {'dirList':dirList, 'Error':''})

def addOrgToJSON(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    for elem in json_file['orgs']:
        if request.POST['name'] == elem['name']:
            json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
            dirList = []
            for elem in json_file['users']:
                if elem['group'] == 'director':
                    dirList.append(elem['login'])
            return render(request, 'addorg.html', {'dirList': dirList, 'Error':'Это имя уже занято!'})
    for elem in json_file['orgs']:
        if request.POST['director'] == elem['director']:
            json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
            dirList = []
            for elem in json_file['users']:
                if elem['group'] == 'director':
                    dirList.append(elem['login'])
            return render(request, 'addorg.html', {'dirList': dirList, 'Error':'Этот директор уже занят!'})
    orgdict = {'name':request.POST['name'], 'director':request.POST['director'], 'date':request.POST['date']}
    json_file['orgs'].append(orgdict)
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file,fw,indent=4)
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    return adminPagePrepare(request)

def changeDir(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    i = 0
    for elem in json_file['orgs']:
        if elem['name'] == request.POST['name']:
            json_file['orgs'][i]['director'] = request.POST['director']
        i += 1
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file,fw,indent=4)
    return adminPagePrepare(request)


def changeEmpOrg(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage': 'Ошибка авторизации'})
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    i = 0
    for elem in json_file['users']:
        if elem['login'] == request.GET['login']:
            json_file['users'][i]['org'] = request.GET['org']
            break
        i += 1
    with open('users.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file,fw,indent=4)
    return adminPagePrepare(request)

def delOrg(request):
    if request.session['user'] != 'admin':
        return render(request, 'auth.html', {'ErrorMessage':'Ошибка авторизации'})
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    i = 0
    for elem in json_file['orgs']:
        if elem['name'] == request.GET['name']:
            json_file['orgs'].pop(i)
            break
        i += 1
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file, fw, indent=4)
    return adminPagePrepare(request)

def addOrder(request):
    print(request.POST)
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    json_file['orderpart']['count'] += 1
    tempList = request.POST['order'].split('.')
    print(tempList)
    print(request.POST['opendate'])
    opendate = request.POST['opendate'].split("-")
    print(opendate)
    for i in range(0,3):
        opendate[i] = int(opendate[i])
    print(opendate)
    closedate = datetime.date(opendate[0], opendate[1], opendate[2])
    org = 0
    for i in range(0, len(json_file['orgs'])):
        if tempList[0] == json_file['orgs'][i]['name']:
            org = i
            break
    addtime = 0
    for elem in json_file['orgs'][i]['offers']:
        if elem['offername'] == tempList[1]:
            addtime = elem['time']
    closedate = closedate + datetime.timedelta(days=addtime)
    month = str(closedate.month)
    if len(month) < 2:
        month = '0' + month
    day = str(closedate.day)
    if len(day) < 2:
        day = '0' + day
    closedatestr = str(closedate.year) + '-' + month + "-" + day
    order = {"id":json_file['orderpart']['count'], "org":tempList[0], "offer":tempList[1],
             "author":request.session['login'], "title":request.POST['orderText'],"opendate":request.POST['opendate'],
             "closedate": closedatestr,"status":0}
    json_file['orderpart']['orders'].append(order)
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file, fw, indent=4)
    return userPagePrepare(request)


def changeUserInfo(request):
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    userNumber = 0
    for i in range(0, len(json_file['users'])):
        if request.session['login'] == json_file['users'][i]['login']:
            userNumber = i
            break
    json_file['users'][userNumber]['name'] = request.POST.get('name', 'Не указано')
    json_file['users'][userNumber]['surname'] = request.POST.get('surname', 'Не указана')
    json_file['users'][userNumber]['patron'] = request.POST.get('patron', 'Не указано')
    json_file['users'][userNumber]['phone'] = request.POST.get('phone', 'Не указан')
    json_file['users'][userNumber]['email'] = request.POST.get('email', 'Не указано')
    json_file['users'][userNumber]['birth'] = request.POST.get('birth', 'Не указана')
    with open('users.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file, fw, indent=4)
    return cabPagePrepare(request)

def choseUser(request):
    if (request.session['user'] != 'admin') and (request.session['user'] != 'director'):
        return render(request, 'auth.html', {'ErrorMessage': 'Ошибка авторизации'})
    json_file = json.load(open('users.json', 'r', encoding='utf-8-sig'))
    chosedUser = {}
    for elem in json_file['users']:
        if elem['login'] == request.GET.get('login', ''):
            elem.pop('password')
            chosedUser = elem
    request.session['chosedUser'] = chosedUser
    if request.session['user'] == 'admin':
        return adminPagePrepare(request)
    else: return directorPagePrepare(request)

def changeOrder(request):
    json_file = json.load(open('orgs.json', 'r', encoding='utf-8-sig'))
    for i in range(0, len(json_file['orderpart']['orders'])):
        print(i)
        print(request.GET)
        if json_file['orderpart']['orders'][i]['id'] == int(request.GET['id']):
            json_file['orderpart']['orders'][i]['closedate'] = request.GET['closedate']
            json_file['orderpart']['orders'][i]['status'] = 1
            json_file['orderpart']['orders'][i]['emp'] = request.session['login']
            print(json_file['orderpart']['orders'][i])
    with open('orgs.json', 'w', encoding="utf-8-sig") as fw:
        json.dump(json_file, fw, indent=4)
    return empPagePrepare(request)


def home(request):
    if request.session['user'] == 'admin':
        return adminPagePrepare(request)
    elif request.session['user'] == 'director':
        return directorPagePrepare(request)
    elif request.session['user'] == 'emp':
        return empPagePrepare(request)
    elif request.session['user'] == 'user':
        return userPagePrepare(request)
    else:
        return render(request,'auth.html',{'ErrorMessage':'Ошибка авторизации'})