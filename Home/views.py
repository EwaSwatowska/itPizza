from django.shortcuts import render
#from django.http import HttpResponse
from decimal import *

from .models import Pizza
from .models import Pizzeria
from .models import PositionInMenu
from .forms import SelectPizzeriaForm, OrderHeadForm
from .models import OrderData, OrderPosition
from random import randint




def Home(request):
    print(request)
    return render(request, 'Home/Home.html', {'title': 'strona główna'})

def SelectPizzeria(request):
    print("+"*30)
    print(request)
    pim1 = PositionInMenu.objects.filter(pizzeria_id=0)
    context = {
        'positionMenu': pim1,
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': "xx"
    }
    # print(request.method)
    if request.method == "POST":
        print(request.POST)
        form = SelectPizzeriaForm(request.POST)
        if form.is_valid(): #wszystkie pola sa poprawne
            idPizr=request.POST.get('cfPizzeria') #pobieram wartosc tego pola(idPizzerii)
            if idPizr != '0':
                context['IdPizzPOST'] = idPizr
                pizr = Pizzeria.objects.get(id=idPizr)
                context['NazwaPOST']=pizr.name
                pim = PositionInMenu.objects.filter(pizzeria_id=idPizr) #cale menu pizzerii
                context['positionMenu']=pim
            else:
                context['IdPizzPOST'] = 'xx'
                context['NazwaPOST']='dokonaj wyboru pizzeri (powyżej)'
                context['positionMenu']=pim1
    else:
        form = SelectPizzeriaForm()

    context['form'] = form
    return render(request, 'Home/SelectPizzeria.html', context)

def OrderList(request):
    print(request.method)
    context = {
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': "xx"
    }
    if request.method == "POST":
        print ("*"*25)
        print(request.POST)
        print ("*" * 25)
        idPizr = request.POST.get('IdPizzPOST')
        print(idPizr)
        context['IdPizzPOST'] = idPizr
        pizr = Pizzeria.objects.get(id=idPizr)
        context['NazwaPOST'] = pizr.name
        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        OrderSum = Decimal('0.00')
        for obj in pim:
            if request.POST.get('PosListPizz_' + '%.0f' % obj.id):
                obj.countTmp = Decimal(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
                OrderSum += (obj.countTmp * obj.price)
            else:
                obj.countTmp = 0
        context['positionMenu'] = pim
        context['OrderSum'] = OrderSum
    else:
        print("!!!!!!! GET" *5)
        #form = SelectPizzeriaForm()

    return render(request, 'Home/OrderList.html', context)

def OrderHead(request):

    #print(request.method)

    context = {
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': "xx",
        'OrderSum': "0.00"
    }

    if request.method == "POST":
        my_form = OrderHeadForm(request.POST)
        context['form'] = my_form
        print ("*"*25)
        print(request.POST)
        print ("*" * 25)
        idPizr = request.POST.get('IdPizzPOST')
        print(idPizr)
        context['IdPizzPOST'] = request.POST.get('IdPizzPOST')
        context['NazwaPOST'] = request.POST.get('NazwaPOST')
        context['OrderSum'] = request.POST.get('OrderSum')
        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        for obj in pim:
           if request.POST.get('PosListPizz_' + '%.0f' % obj.id):
              obj.countTmp = Decimal(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
           else:
              obj.countTmp = 0
        context['positionMenu'] = pim
    else:
        print("!!!!!!! GET" *5)
    #     #form = SelectPizzeriaForm()


    return render(request, 'Home/OrderHead.html', context)


def OrderPlaced(request):
    print("##########################################################################")
    print(request.POST)

    if request.method == 'POST':
        print('Tu jestem teraz')
        # post = my_form.save(commit=False)
        # post.total = request.POST.get('OrderSum')
        # post.pizzeria = request.POST.get('IdPizzPOST')
        # post.save()
        ptotal=request.POST.get('OrderSum')

        idPizr = request.POST.get('IdPizzPOST')
        ppizzeria = Pizzeria.objects.get(id=idPizr)

        pnameAndSurname=request.POST.get('nameAndSurname')
        pstreet=request.POST.get('street')
        pstreetNumber=request.POST.get('streetNumber')
        phouseNumber=request.POST.get('houseNumber')
        pemail=request.POST.get('email')
        pphoneNumber=request.POST.get('phoneNumber')
        while True:
            porderNumber=randint(500000, 1000000)
            print(porderNumber)
            tmpNumber = OrderData.objects.filter(orderNumber=porderNumber).first()
            if tmpNumber is None:
                break
        order_obj = OrderData(
            nameAndSurname=pnameAndSurname,
            street = pstreet,
            streetNumber = pstreetNumber,
            houseNumber = phouseNumber,
            email = pemail,
            phoneNumber = pphoneNumber,
            total = ptotal,
            pizzeria = ppizzeria,
            orderNumber = porderNumber
        )
        order_obj.save()

        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        for obj in pim:
            if request.POST.get('PosListPizz_' + '%.0f' % obj.id):
                obj.countTmp = Decimal(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
                nr = int(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
                if nr != 0:
                    # print('halohalohalohalohalohalohalohalohalohalohalo')
                    # print(nr)
                    orderposition_obj = OrderPosition(
                        order_id = order_obj,
                        positionInMenu_id = obj,
                        numberOfPIM = nr
                    )
                    orderposition_obj.save()
            else:
                obj.countTmp = 0

        context = {
            'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
            'IdPizzPOST': "xx",
            'OrderSum': "0.00"
        }
        context['IdPizzPOST'] = request.POST.get('IdPizzPOST')
        context['NazwaPOST'] = request.POST.get('NazwaPOST')
        context['OrderSum'] = request.POST.get('OrderSum')
        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        for obj in pim:
            if request.POST.get('PosListPizz_' + '%.0f' % obj.id):
                obj.countTmp = Decimal(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
            else:
                obj.countTmp = 0
        context['positionMenu'] = pim
        context['orderData'] = order_obj

    return render(request, 'Home/OrderPlaced.html', context)

def CheckStatus(request):
    context = {}

    if request.method == 'POST':
        number=request.POST.get('orderNumber')
        context['orderNumber'] = number
        if number:
            print(number)
            piod = OrderData.objects.filter(orderNumber = number).first() #position in OrderData
            piod = podlicz(piod) #obliczony total z funkcji podlicz
            print(piod)
            if piod is not None:
                context['orderData'] = piod
                piop = OrderPosition.objects.filter(order_id = piod) #position in OrderPosition
                context['orderPosition'] = piop

    return render(request, 'Home/CheckStatus.html', context)






def oProjekcie(request):
    #print(request.GET)
    #print(request.POST)
    #myNewTitle = request.POST.get('title')
    #print(myNewTitle)
    #context = {}
    return render(request, 'Home/oProjekcie.html')

# ----------- menu itPizza ---------------
pizzas = [
    {
        'name': 'Margharita',
        'ingredients': 'cheese',
        'priceS': '15',
        'priceM': '20',
        'priceB': '25',
        'priceXXL': '30',
        'picture': 'grafika/marg.png'
    },
    {
        'name': 'Capriciosa',
        'ingredients': 'cheese, ham, mushrooms',
        'priceS': '18',
        'priceM': '23',
        'priceB': '29',
        'priceXXL': '35',
        'picture': 'grafika/capri.jpg'
    },
    {
        'name': 'Salame',
        'ingredients': 'cheese, salame',
        'priceS': '19',
        'priceM': '26',
        'priceB': '29',
        'priceXXL': '38',
        'picture': 'grafika/pepper.png'
    },
    {
        'name': 'Hawaii',
        'ingredients': 'cheese, ham, pineapple',
        'priceS': '20',
        'priceM': '25',
        'priceB': '29',
        'priceXXL': '34',
        'picture': 'grafika/hawaii.jpg'
    }
]

def Menu(request):
    menuList = {
        'pizzas': pizzas
    }
    return render(request, 'Home/Menu.html', menuList)

def podlicz(obj):
    piop = OrderPosition.objects.filter(order_id=obj)
    obj.total = 0
    for piop_obj in piop:
        obj.total += piop_obj.numberOfPIM*piop_obj.positionInMenu_id.price
    return obj
