from flask import Flask, render_template, request, redirect
import pyrebase
import datetime
import firebase_admin
from firebase_admin import auth
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token

config = {
    apiKey: "Your app details here",
    authDomain: "Your app details here",
    databaseURL: "Your app details here",
    projectId: "Your app details here",
    storageBucket: "Your app details here",
    messagingSenderId: "Your app details here",
    appId: "Your app details here",
    measurementId: "Your app details here"

}
firebase = pyrebase.initialize_app(config)
firebase_admin.initialize_app()
db = firebase.database()

app = Flask(__name__)

firebase_request_adapter = requests.Request()

datastore_client = datastore.Client()

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def newBasket(user):
    newBasket = {
        "Customer ID" : user,
        "Items" : "",
    }
    db.child ( "Basket" ).push ( newBasket )
    getBasket ( user )

def newUser(name, email, passw):
    newuser = auth.create_user (
        email=email,
        email_verified=False,
        password=passw,
        display_name=str(name),
 )
    newBasket(newuser.uid)

def newAdmin(userID):
    for user in auth.list_users ().iterate_all () :
        if user.uid == userID:
            newAd = {
                "Customer ID" : userID,
            }
            db.child ( "Admin" ).push(newAd)

def getUsers():
    lst = []
    for user in auth.list_users ().iterate_all () :
        try:
            username = user.display_name
        except AttributeError:
            username = "NOT GIVEN"

        userInfo = {"User ID":user.uid,
                    "User Name":username}
        lst.append(userInfo)
    return lst

def isAdmin(userID):
    table = db.child("Admin").child().get().val()
    for check in table.values():
        if check['Customer ID'] == userID:
            return True
    return False

def removeAdmin(userID):
    table = db.child("Admin").child().get()
    admin = table.val().items()
    print(admin)
    for k,v in admin:
        print("K ="+str(k))
        print ( "v =" + str ( v ) )
        if v['Customer ID'] == userID:
            db.child("Admin").child(k).remove()

def delItem(itm):
    table = db.child("Product").child(itm).get()
    print(table.val())
    db.child("Products").child(itm).remove()

def newProduct(prodInfo):
    newProduct = {
        "Item Name" : prodInfo.get("name"),
        "Cost" : prodInfo.get("cost"),
        "Item Desc" : prodInfo.get("desc"),
        "Item Picture" : prodInfo.get("img"),
        "In Stock" : prodInfo.get("quant"),
        "Item ID" : "na",
    }
    db.child ( "Products" ).push (newProduct)

def addProductId(id):
    db.child("Products").child(id).update({"Item ID":id})

def addOrderId(id):
    db.child("Orders").child(id).update({"Order ID":id})

def getProdIds():
    table = db.child ( "Products" ).child().get().val()
    quer = table.keys()
    try:
        count = 0
        for i in quer:
            count += 1
            if count == len(quer):
                return i
    except:
        print("Error")

def getBasket(user):
    lst=[]
    table = db.child("Basket").order_by_child("Customer ID").equal_to(user)

    basket = table.get().val().items()
    for key,value in basket:
        for product in value['Items'].split(",")[:-1]:
            lst.append(product)

    return getBsktItems(lst)

def getOldBasket(baskID):
    lst=[]
    table = db.child ( "Orders" ).child(baskID).get()
    basket = table.val()
    print(basket['Items'])
    for i in basket['Items'].split(",")[:-1]:
        lst.append(getItm(i))
    return lst

def getOrders(user):
    lst = [ ]
    try:
        table = db.child("Orders").order_by_child('Customer ID').equal_to(user)
        order = table.get().val().items()
        for key, value in order :
            for product in value ['Items'].split(",")[:-1]:
                lst.append ( product )

        return getOrderItms(lst)
    except:
        return "NO ORDERS"

def orderTest(user):
    history=[]
    table = db.child("Orders").order_by_child('Customer ID').equal_to(user)
    try:
        basket = table.get().val().items()
    except AttributeError:
        tempOrder = {
            "Customer ID": user,
            "Items": "",
            "Order ID": "NO ORDERS YET",
            "Ordered" : "NO ORDERS YET",}
        history.append(tempOrder)
        return history
    for key, value in basket:
        temp = { }
        for k,v in value.items():
            if k == 'Items':
                items=[]
                for i in v.split(",")[:-1]:
                    items.append(getItm((i)))
                temp[k]= items
            else:
                temp[k] = v
        history.append(temp)
    return history
def packageBskt(bsktLst):
    lst=[]
    for i in bsktLst:
        row = []
        for x in i.split(",")[:-1]:
            row.append(getItm(x))
            lst.append(row)
    return lst

def getOrderItms(orders):
    history = []
    for i in orders:
        bask = []
        table = db.child("Orders").child(i).get().val()
        for x in table['Items'].split(","):
            bask.append(getItm(x))
        history.append(table['Items'])
    return history

def addItmtoBskt(item, user):
    table = db.child("Basket").order_by_child("Customer ID").equal_to(user)
    quer = table.get().val()
    key = quer.keys()
    values = quer.values()

    for i in values:
        lst = i['Items']

    for i in key:
        tblKey = i
    lst += str(item)+","
    db.child("Basket").child(tblKey).update({"Items":lst})
    return lst

def updateProduct(item):
    prodUpdate = {
        "Item Name" : item["name"] ,
        "Cost" : item["cost"],
        "Item Desc" : item["desc"],
        "Item Picture" : item["img"],
        "In Stock" : item["quant"],
    }
    db.child("Products").child(item['id']).update(prodUpdate)

def basketID(user):
    table = db.child("Basket").order_by_child("Customer ID").equal_to(user)
    quer = table.get().val()
    key = quer.keys()

    for i in key:
        tblKey = i

    return tblKey

def getOrder(ordered):
    table = db.child("Orders").order_by_child("Ordered").equal_to(ordered)
    orderID = table.get().val().keys()
    addOrderId(list(orderID)[0])

def getOrderInfo(id):
    table = db.child("Orders").child(id).get()
    ordered = table.val()['Ordered']
    print(ordered)
    return str(ordered)


def addBsktOrder(bskt, user):
    lst = bskt
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y, %H:%M:%S")
    orderidkey = now.strftime("%d%S%m%M")
    newOrder = {
        "Customer ID": user,
        "Items": lst,
        "Order ID": str(basketID(user)+orderidkey),
        "Ordered" : date,
    }
    db.child("Orders").push(newOrder)
    getOrder(date)
    quer = db.child ( "Basket" ).order_by_child ("Customer ID").equal_to(user)
    baskid = quer.get().val().keys()
    for i in baskid:
        db.child("Basket").child(i).update({"Items":""})

    return lst

def getItm(item):
    prod = db.child("Products").child(item).get().val()
    return prod


#returns Ids of every product
def getProds():
    itemInfo = [ ]
    table = db.child ("Products").get().val().values()
    for values in table:
        itemInfo.append(values)
    return itemInfo

def getBsktItems(basket):
    bsktItems = [ ]
    for i in basket:
        bsktItems.append(getItm (i))
    return bsktItems


@app.route('/')
def root():
    global orders
    id_token = request.cookies.get ( "token" )
    if id_token :
        claims = google.oauth2.id_token.verify_firebase_token (
            id_token, firebase_request_adapter )
        orders = packageBskt ( getOrders ( claims [ 'user_id' ] ) )
        render_template ( 'pageORD.html', basket=orders )
        return redirect ( '/order' )
    return redirect('/prods')

@app.route('/prods')
def itms():
    prods = getProds()
    return render_template ( 'devPAGE.html', store=prods)

@app.route('/item/<string:current>',methods=["GET","POST"])
def itmselect(current):
    id_token = request.cookies.get("token")
    single = getItm(current)
    if request.method == 'POST':
        if id_token :
            claims = google.oauth2.id_token.verify_firebase_token (
                id_token, firebase_request_adapter )
        addItmtoBskt(current,claims['user_id'])
        redirect(request.referrer)
    return render_template ( 'page2.html',help=single)

@app.route('/basket', methods=["GET","POST"])
def bskt():
    global orders
    id_token = request.cookies.get( "token" )
    holder = ""
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token (
            id_token, firebase_request_adapter )
        try:
            basket = getBasket (claims['user_id'])
        except UnboundLocalError:
            redirect('/basket')

        for i in basket :
            count = 0
            for itm in i.values():
                count += 1
                if count == 4:
                    holder += str ( itm ) + ','
        if request.method == 'POST':
            addBsktOrder(holder,claims['user_id'])
            orders = packageBskt(getOrders ( claims [ 'user_id' ] ))
            return redirect('/order')
        return render_template( 'pgBSKT.html', basket=basket)
    return redirect ( '/prods' )

@app.route('/basket/<string:orderID>', methods=['GET'])
def oldBasket(orderID):
    basket = getOldBasket(orderID)
    order = getOrderInfo(orderID)
    print(order)
    return render_template('admin.html', basket=basket, order=order)

@app.route('/order')
def testPg():
    id_token = request.cookies.get ( "token" )
    global orders
    history = True
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token (
            id_token, firebase_request_adapter )
        orders = orderTest(claims['user_id'])
        for i in orders:
            if i['Ordered'] == "NO ORDERS YET":
                history = False
    if id_token:
        return render_template( 'pageORD.html', basket=orders, hist=history, var=None)
    return redirect ( "/prods" )


@app.route('/register', methods=['GET','POST'])
def register():

    return render_template('registerPg.html')

@app.route('/create', methods=['POST'])
def testing():
    name = request.form.get ( 'name' )
    email = request.form.get ( 'email' )
    passw = request.form.get ( 'pass' )
    try:
        newUser(name, email, passw)

        return redirect("/prods")
    except (firebase_admin.exceptions.InvalidArgumentError,ValueError):
        return redirect("/register")

@app.route('/admin', methods=['POST'])
def createAdmin():
    try:
        return redirect(request.referrer)
    except (firebase_admin.exceptions.InvalidArgumentError,ValueError):
        return redirect(request.referrer)

@app.route('/admin/create/<string:userid>', methods=['POST'])
def createNewAdmin(userid):
    try:
        newAdmin(userid)
        return redirect(request.referrer)
    except (firebase_admin.exceptions.InvalidArgumentError,ValueError):
        return redirect(request.referrer)

@app.route('/admin/delete/<string:userid>', methods=['POST'])
def deleteAdmin(userid):
    try:
        removeAdmin(userid)
        return redirect ( request.referrer )
    except (firebase_admin.exceptions.InvalidArgumentError,ValueError):
        return redirect(request.referrer)


@app.route('/modal', methods=['GET','POST'])
def modal():
    id_token = request.cookies.get ( "token" )
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token (
            id_token, firebase_request_adapter)
        if isAdmin(claims['user_id']):
            prods = getProds ()
            return render_template('modalPage.html', histories=prods, item=getUsers())

    return redirect(request.referrer)


@app.route('/createItem', methods=['POST'])
def createItm():
    newItm = {
    "name" : request.form.get ( 'name' ),
    "cost" : request.form.get ( 'cost' ),
    "desc" : request.form.get ( 'desc' ),
    "img" : request.form.get ( 'img' ),
    "quant" : request.form.get ( 'quant' ),
    }
    try:
        newProduct(newItm)
        addProductId(getProdIds())
        return redirect(request.referrer)
    except:
        return redirect(request.referrer)

@app.route('/updateItem', methods=['POST'])
def updateItm():
    newItm = {
    "id" : request.form.get('foo'),
    "name" : request.form.get ( 'name' ),
    "cost" : request.form.get ( 'cost' ),
    "desc" : request.form.get ( 'desc' ),
    "img" : request.form.get ( 'img' ),
    "quant" : request.form.get ( 'quant' ),
    }
    updateProduct(newItm)
    return redirect("/modal")

@app.route('/updateItem/<string:id>', methods=['POST'])
def deleteItm(id):
    print(id)
    delItem(id)
    return redirect(request.referrer)

if __name__ == '__main__':
    app.jinja_env.cache = { }
    app.run(host='127.0.0.1', port=8080, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
