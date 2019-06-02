from django.shortcuts import render
#from django.http import HttpResponse
from decimal import *

from .models import Pizza
from .models import Pizzeria
from .models import PositionInMenu
from .forms import SelectPizzeriaForm, OrderHeadForm
from .models import OrderData, OrderPosition, Coupon
from random import randint


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
    # print(request.method)
    context = {
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': 'xx',
        'couponCode': '',
        'drink': '',
        'numberOfDrinks': '0',
        'sauce': '',
        'numberOfSauces': '0',
        'pizzas': pizzas
    }
    if request.method == "POST":
        print ("*"*25)
        print(request.POST)
        print ("*" * 25)
        idPizr = request.POST.get('IdPizzPOST')
        print(idPizr)

        pizzaTable = Pizza.objects.all()
        context['pizzaTable'] = pizzaTable

        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        listOfPizzas = [obj.Pizza_FK for obj in pim]
        listOfPizzas = list(set(listOfPizzas))
        print(listOfPizzas)
        context['listOfPizzas'] = listOfPizzas


        context['IdPizzPOST'] = idPizr
        pizr = Pizzeria.objects.get(id=idPizr)
        context['NazwaPOST'] = pizr.name
        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        OrderSum = Decimal('0.00')
        for obj in pim:
            if request.POST.get('PosListPizz_' + '%.0f' % obj.id):
                obj.countTmp = Decimal(request.POST.get('PosListPizz_' + '%.0f' % obj.id))
                OrderSum += (obj.countTmp * (obj.price+obj.Pizza_FK.looseOfPrice))
            else:
                obj.countTmp = 0
        context['positionMenu'] = pim
        if request.POST.get('drink'):
            context['drink'] = request.POST.get('drink')
            context['numberOfDrinks'] = request.POST.get('numberOfDrinks')
            drink = request.POST.get('drink')
            if drink != '6':
                numberOfDrinks = Decimal(request.POST.get('numberOfDrinks'))
                OrderSum = OrderSum + numberOfDrinks*Decimal('3.00')
            else:
                context['numberOfDrinks'] = '0'
        if request.POST.get('sauce'):
            context['sauce'] = request.POST.get('sauce')
            context['numberOfSauces'] = request.POST.get('numberOfSauces')
            sauce = request.POST.get('sauce')
            if sauce != '6':
                numberOfSauces = Decimal(request.POST.get('numberOfSauces'))
                OrderSum = OrderSum + numberOfSauces*Decimal('2.00')
            else:
                context['numberOfSauces'] = '0'
        context['OrderSum'] = OrderSum
        context['coupon_obj'] = None
        OrderSumDiscount = Decimal('0.00')
        pcouponCode = request.POST.get('couponCode')
        if pcouponCode is not None :
            context['couponCode'] = pcouponCode  # jako value od tego inputa
            coupon_obj = Coupon.objects.filter(code=pcouponCode).first()
            if coupon_obj is not None:
                numOfCoupDone = OrderData.objects.filter(Coupon_FK=coupon_obj).count()
                print(numOfCoupDone)
                if numOfCoupDone < coupon_obj.numberOfCoupons:
                    OrderSumDiscount = OrderSum*(1-Decimal(coupon_obj.discount)/Decimal('100.00'))
                    context['coupon_obj'] = coupon_obj
        context['OrderSumDiscount'] = OrderSumDiscount

    return render(request, 'Home/OrderList.html', context)

def OrderHead(request):

    #print(request.method)

    context = {
        'NazwaPOST': 'dokonaj wyboru pizzeri (powyżej)',
        'IdPizzPOST': "xx",
        'OrderSum': "0.00"
    }

    if request.method == "POST":
        # ten obiekt jest stworzony na chwile i trzyma id tak zeby moc potem wyswietlic sama nazwe
        orderdata_obj = OrderData(
            drink = request.POST.get('drink'),
            numberOfDrinks = request.POST.get('numberOfDrinks'),
            sauce = request.POST.get('sauce'),
            numberOfSauces = request.POST.get('numberOfSauces')
        )
        context['orderdata_obj'] = orderdata_obj
        my_form = OrderHeadForm(request.POST)
        context['form'] = my_form
        print(my_form)
        print ("*"*25)
        print(request.POST)
        print ("*" * 25)
        idPizr = request.POST.get('IdPizzPOST')
        print(idPizr)
        context['IdPizzPOST'] = request.POST.get('IdPizzPOST')
        context['NazwaPOST'] = request.POST.get('NazwaPOST')
        # context['drink'] = request.POST.get('drink'),
        # context['numberOfDrinks'] = request.POST.get('numberOfDrinks')
        context['OrderSum'] = request.POST.get('OrderSum')
        context['couponCode'] = request.POST.get('couponCode')
        context['OrderSumDiscount'] = request.POST.get('OrderSumDiscount')
        pim = PositionInMenu.objects.filter(pizzeria_id=idPizr)
        for obj in pim:
           if request.POST.get('PosListPizz_' + '%.0f' % obj.id): #lista pizz (ilosc pizz na zamowieniu)
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

        ptotalbefore=request.POST.get('OrderSum')
        ptotaldiscount=request.POST.get('OrderSumDiscount')
        if(ptotaldiscount != '0.00'):
            ptotal = ptotaldiscount
        else:
            ptotal = ptotalbefore

        idPizr = request.POST.get('IdPizzPOST')
        ppizzeria = Pizzeria.objects.get(id=idPizr)

        pnameAndSurname=request.POST.get('nameAndSurname')
        pstreet=request.POST.get('street')
        pstreetNumber=request.POST.get('streetNumber')
        phouseNumber=request.POST.get('houseNumber')
        pemail=request.POST.get('email')
        pphoneNumber=request.POST.get('phoneNumber')
        pdrink=request.POST.get('drink')
        pnumberOfDrinks=request.POST.get('numberOfDrinks')
        psauce=request.POST.get('sauce')
        pnumberOfSauces=request.POST.get('numberOfSauces')
        while True:
            porderNumber=randint(500000, 1000000)
            print(porderNumber)
            tmpNumber = OrderData.objects.filter(orderNumber=porderNumber).first()
            if tmpNumber is None:
                break
        pcouponCode=request.POST.get('couponCode')
        print(pcouponCode)
        pcoupon = Coupon.objects.filter(code = pcouponCode).first()
        print(pcoupon)
        ppay = request.POST.get('pay')
        print("**************************")
        print(ppay)
        order_obj = OrderData(
            nameAndSurname=pnameAndSurname,
            street = pstreet,
            streetNumber = pstreetNumber,
            houseNumber = phouseNumber,
            email = pemail,
            phoneNumber = pphoneNumber,
            total = ptotal,
            pizzeria = ppizzeria,
            drink=pdrink,
            numberOfDrinks=pnumberOfDrinks,
            sauce = psauce,
            numberOfSauces = pnumberOfSauces,
            orderNumber = porderNumber,
            pay = ppay,
            Coupon_FK = pcoupon
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
        context['OrderSumDiscount'] = request.POST.get('OrderSumDiscount')
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

