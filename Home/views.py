from django.shortcuts import render
#from django.http import HttpResponse
from decimal import *

#from .models import Pizza
from .models import Pizzeria
from .models import PositionInMenu
from .forms import SelectPizzeriaForm, OrderHeadForm



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

    if request.method == 'POST':
        #my_form = OrderHeadForm(request.POST)
        my_form = OrderHeadForm()
        if my_form.is_valid():
            print(my_form.cleaned_data)
        else:
            print(my_form.errors)

    context = {
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': "xx",
        'OrderSum': "0.00",
        'form': my_form
    }

    if request.method == "POST":
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

