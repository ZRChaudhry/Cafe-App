# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 12:04:26 2021
"""
import PySimpleGUI as sg
import pandas as pd
import numpy as np


    
def shopPage() :
    cartItems = [["items"],["count"], ["price"], ["points"]] 
    itemDF = pd.read_csv("D:\shopItems.csv", usecols=('item', 'price', 'points' ))
    #fields item, price, point, price stock, cost to stock, item points, type
    numberData = itemDF.shape[0]
    itemList = []
    for x in range(numberData):
        itemList.append([sg.Text( "Item: " + str(itemDF['item'][x])), 
                         sg.Text("Price: " + str(itemDF['price'][x])), 
                         sg.Button("Add item", key="Add item " + str(itemDF['item'][x])), 
                         sg.Button("Remove item", key = "Remove item " +str(itemDF['item'][x]))])
    
    addButtonKeys = []
    
    for x in range(numberData):
        addButtonKeys.append("Add item " + str(itemDF['item'][x]))
    
    removeButtonKeys =[]
    
    for x in range(numberData):
        removeButtonKeys.append("Remove item " +str(itemDF['item'][x]))
    
    cartList = [
            [sg.Text("Items in Cart")],
            [sg.Listbox(values=[],enable_events=True, size=(20,10), key= "-CART-", pad= 0),
             sg.Listbox(values=[],enable_events=True, size=(10,10), key= "-COUNT-", pad = 0) ]
        
        ]
    
    
    layout = [
                [
                sg.Column(itemList, size=(500,450), scrollable=True, pad = 0),
                sg.VSeperator(),
                sg.Column(cartList, pad = 0)
                ],
                [sg.Button("Order Items in Cart"), sg.Button("Return to Homepage")]
            ]
    
    shopWindow = sg.Window("Cafe Application", layout)
    
    #This will keep the window open until user wants to close it or transition to another window
    
    
    while True:
            event, values = shopWindow.read()
            
            if event == "Exit"  or event == sg.WIN_CLOSED :
                break
            elif event == "Return to Homepage":
                shopWindow.close()
                managerPage()
            elif event == "Order Items in Cart":
                shopWindow.close()
                orderPage(cartItems)
            elif event in addButtonKeys :
                try:
                    query = event
                    stopwords = ['add', 'item']
                    querywords = query.split()
                    resultwords  = [word for word in querywords if word.lower() not in stopwords]
                    result = ' '.join(resultwords)
                    if result in cartItems[0]:
                        for x in range(len(cartItems[0])):
                            if result == cartItems[0][x]:
                                cartItems[1][x] += 1
                                shopWindow["-CART-"].update(cartItems[0])
                                shopWindow["-COUNT-"].update(cartItems[1])
                                break
                    else:
                        tempRow = itemDF.loc[itemDF['item'] == result]
                        cartItems[0].append(str(tempRow['item'][tempRow.index[0]]))
                        cartItems[1].append(1)
                        shopWindow["-CART-"].update(cartItems[0])
                        shopWindow["-COUNT-"].update(cartItems[1])
                        cartItems[2].append(str(tempRow['price'][tempRow.index[0]]))
                        cartItems[3].append(str(tempRow['points'][tempRow.index[0]]))
                except:
                    pass
            elif event in removeButtonKeys:
                try:
                    query = event
                    stopwords = ['remove', 'item']
                    querywords = query.split()
                    resultwords  = [word for word in querywords if word.lower() not in stopwords]
                    result = ' '.join(resultwords)
                    if result in cartItems[0]:
                        for x in range(len(cartItems[0])):
                            if result == cartItems[0][x] and cartItems[1][x]==1:
                                del cartItems[0][x]
                                del cartItems[1][x]
                                del cartItems[2][x]
                                del cartItems[3][x]
                                shopWindow["-CART-"].update(cartItems[0])
                                shopWindow["-COUNT-"].update(cartItems[1])
                                break
                            elif  result == cartItems[0][x] and cartItems[1][x]>1:
                                for x in range(len(cartItems[0])):
                                    if result == cartItems[0][x]:
                                        cartItems[1][x] = cartItems[1][x]-1
                                        shopWindow["-CART-"].update(cartItems[0])
                                        shopWindow["-COUNT-"].update(cartItems[1])
                                        break
                    else:
                        pass
                        
                   
                except:
                    pass

    shopWindow.close()

def orderPage(cartItems):
        itemDF = pd.read_csv("D:\shopItems.csv")
        #fields item, price, point, price stock, cost to stock, item points, type
        userDF = pd.read_csv(r"D:\userAccount.csv")
        #name, address, payment, points
        total = 0
        pointTotal = 0
        #add to total all items multplied by their counts
        for x in range(len(cartItems[0])):
            if x > 0:
                total += (cartItems[1][x] * float(cartItems[2][x]))
       
        for x in range(len(cartItems[0])):
            if x > 0:
                pointTotal += (cartItems[1][x] * float(cartItems[3][x]))
        
        cartList = [
            
            [sg.Text("Items in Cart")],
            [sg.Listbox(values=cartItems[0],enable_events=True, size=(20,10), key= "-CART-", pad= 0),
             sg.Listbox(values=cartItems[1],enable_events=True, size=(10,10), key= "-COUNT-", pad = 0),
             sg.Listbox(values=cartItems[2],enable_events=True, size=(10,10), key= "-COUNT-", pad = 0)],
             [sg.Text("Total Price: " + str(total))],
             [sg.Text("Total Tax: " + str(total*.12))], #simulating 12 percent tax
             [sg.Text("Total Cost: " + str(total + (total*.12)))],
             [sg.Text("Points to be earned : " + str(pointTotal))]
             
        
        ]
        
        checkoutInfo = [
                    [sg.Text("Payment Method: "), 
                     sg.Checkbox("Visa", default=False), 
                     sg.Checkbox("Master Card", default=False),
                     sg.Checkbox("Discover", default=False)],
                    #only defaults to user 2 information because we dont have enough time to implement a full login
                    [sg.Text("Card Number: "), sg.Input(default_text=str(userDF['payment'][1]), key="payment")],
                    [sg.Text("CSV: "), sg.Input(default_text="Enter CSV", key = "csv")],
                    [sg. Text("Billing Address: "), sg.Input(default_text=str(userDF['address'][1]), key = "badrr")],
                    [sg.Checkbox("Pickup", key = "pickup", default=False), 
                     sg.Checkbox("Deliver", key = "deliver", default=False)],
                    [sg. Text("Delivery Address: "), sg.Input(default_text="Fill this up if you want delivery", key = "dadrr")]
                ]       
                    
        layout = [
                    [
                    sg.Column(cartList, pad = 0),
                    sg.Column(checkoutInfo, pad = 0)
                    ],
                    [sg.Button("Pay"), sg.Button("Cancel")]
                ]
        
        shopWindow = sg.Window("Cafe Application", layout)
    
        
        #This will keep the window open until user wants to close it or transition to another window
        while True:
            event, values = shopWindow.read()
            
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Cancel":
                 shopWindow.close()
                 shopPage()
                 break
            elif event == "Pay":
                if values["payment"] and (values["pickup"] == True or values["deliver"==True]):
                    for x in range(len(cartItems[0])):
                        if x > 0:
                            tempRow = itemDF.loc[itemDF['item'] == cartItems[0][x]]
                            itemDF.loc[tempRow.index[0], 'stock'] = tempRow['stock'][tempRow.index[0]] - float(cartItems[2][x])
                    itemDF.to_csv("D:\shopItems.csv", index = False) #replaces the old database with a new database with updated stocks
                    shopWindow.close()
                    confirmationPage(values["dadrr"], pointTotal, total, values["deliver"], values["pickup"])#addr points
                else:
                    badpayInput()
                
                
                
        shopWindow.close()

def confirmationPage(daddr, pointTotal, total, deliver, pickup):
    if deliver == True and pickup == False:
        layout = [
                    [sg.Text("Order Succeeded", justification="Center", font=30)],
                    [sg.Text("Order will come in 30 -60 minutes", justification="Center", font=30)],
                    [sg.Text("Total Cost: " + str(total + (total*.12)))],
                    [sg.Text("Points earned : " + str(pointTotal))],
                    [sg.Text("Delevery Address " + daddr)],
                    [sg.Button("OK", size= (10,5))]
            
            ]
        shopWindow = sg.Window("Cafe Application", layout)
        
        while True:
            event, values = shopWindow.read()
            
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "OK":
                 shopWindow.close()
                 shopPage()
                 break
            
        shopWindow.close()
        
    elif pickup == True and deliver == False:
         layout = [
                    [sg.Text("Order Succeeded", justification="Center", font=30)],
                    [sg.Text("Order will be ready for pick in 30 -60 minutes", justification="Center", font=30)],
                    [sg.Text("Total Cost: " + str(total + (total*.12)))],
                    [sg.Text("Points earned : " + str(pointTotal))],
                    [sg.Button("OK", size= (10,5))]
            
            ]
         shopWindow = sg.Window("Cafe Application", layout)
        
         while True:
            event, values = shopWindow.read()
            
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "OK":
                 shopWindow.close()
                 shopPage()
                 break
            
         shopWindow.close()
    
def stockPage():
    
    itemDF = pd.read_csv("D:\shopItems.csv")
    #fields item, price, point, price stock, cost to stock, item points, type

    numberData = itemDF.shape[0]
    itemList = []
    for x in range(numberData):
        itemList.append([sg.Text( "Item: " + str(itemDF['item'][x])), 
                         sg.Input(key= "input " + str(itemDF['item'][x]), size=(5,3)), 
                         sg.Button("Order stock", key = "order " +str(itemDF['item'][x]))])
    
    orderButtonKeys = []
    
    for x in range(numberData):
        orderButtonKeys.append("order " + str(itemDF['item'][x]))
        
    inputButtonKeys = []
    
    for x in range(numberData):
        inputButtonKeys.append("input " + str(itemDF['item'][x]))
    
    cartList = [
            [sg.Text("Current item stock in the store", font=20)],
            [sg.Listbox(values=itemDF['item'].tolist(),enable_events=True, size=(20,20), key= "-CART-", pad= 0),
             sg.Listbox(values=itemDF['stock'].tolist(),enable_events=True, size=(10,20), key= "-COUNT-", pad = 0) ]
        
        ]
    
    
    layout = [
                [
                sg.Column(itemList, size=(500,450), scrollable=True, pad = 0),
                sg.VSeperator(),
                sg.Column(cartList, pad = 0)
                ],
                [sg.Button("Order Items in Cart"), sg.Button("Return to Homepage")]
            ]
    
    shopWindow = sg.Window("Cafe Application", layout)
     #This will keep the window open until user wants to close it or transition to another window
    while True:
        event, values = shopWindow.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Return to Hompage":
            shopWindow.close()
            managerPage()
        elif event in orderButtonKeys:
            query = event
            stopwords = ['order']
            querywords = query.split()
            resultwords = [word for word in querywords if word.lower() not in stopwords]
            result = ' '.join(resultwords)
            tempRow = itemDF.loc[itemDF['item'] == result]
            if float(values["input " + result]) >= 0:
                itemDF.loc[tempRow.index[0], 'stock'] = tempRow['stock'][tempRow.index[0]] + float(values["input " + result])
                itemDF.to_csv("D:\shopItems.csv", index = False) #replaces the old database with a new database with updated stocks
                shopWindow["-COUNT-"].update(itemDF['stock'])
                shopWindow.refresh()
            else:
                errorNegInput()
            
    shopWindow.close()
    
    
def badpayInput():
    layout = [
                [sg.Text('Make sure payment fields are valid', justification="Center")],
                [sg.Button("Close")]
        ]
    
    popUpWindow = sg.Window("Cafe Application", layout)
    
    while True:
            event, values = popUpWindow.read()
            
            if event == "Close"  or event == sg.WIN_CLOSED :
                break
            
            
    popUpWindow.close()    

def errorNegInput():
    layout = [
                [sg.Text('Pleas enter a positive number', justification="Center")],
                [sg.Button("Close")]
        ]
    
    popUpWindow = sg.Window("Cafe Application", layout)
    
    while True:
            event, values = popUpWindow.read()
            
            if event == "Close"  or event == sg.WIN_CLOSED :
                break
            
            
    popUpWindow.close()
    
def managerReportPopUp():
    layout = [
                [sg.Text('Report Saved to your Current Directory', justification="Center")],
                [sg.Button("Close")]
        ]
    
    popUpWindow = sg.Window("Cafe Application", layout)
    
    while True:
            event, values = popUpWindow.read()
            
            if event == "Close"  or event == sg.WIN_CLOSED :
                break
            
            
    popUpWindow.close()
    
    
def reportPage():
    
    salesDF = pd.read_csv("D:\TotalSalesReport.csv")
    #sales that df has the fields date, total sales, total expense, and total profit
    numberData = salesDF.shape[0]
    itemList = []
    for x in range(numberData):
        itemList.append([sg.Text( "Date of Sale: " + str(salesDF['date'][x])), 
                         sg.Text("Total Sales: " + str(salesDF['total sales'][x])),
                         sg.Text("Total Expense: " + str(salesDF['total expense'][x])), 
                         sg.Text("Total Profit: "+ str(salesDF['total profit'][x])),
                         sg.Button("Add to report", key = "Add to report " + str(salesDF['date'][x])),
                         sg.Button("Remove from report", key = "Remove from report " + str(salesDF['date'][x]))
                         ])
    
    addButtonKeys = []
    
    for x in range(numberData):
        addButtonKeys.append("Add to report " + str(salesDF['date'][x]))
        
    removeButtonKeys =[]
    
    for x in range(numberData):
        removeButtonKeys.append("Remove from report " + str(salesDF['date'][x]))
    
    reportList = [
            [sg.Text("Dates in the Report to be generated", justification= "Center")],
            [sg.Listbox(values=[], size=(50,30),enable_events=True, key= "-CART-")]
        
        ]
    
    
    layout = [
                [
                sg.Column(itemList, size=(800,650), scrollable=True, pad = 0),
                sg.VSeperator(),
                sg.Column(reportList, pad = 0)
                ],
                [sg.Button("Generate Report"), sg.Button("Return to Homepage")]
            ]
    
    managerWindow = sg.Window("Cafe Application", layout)
    
    #This will keep the window open until user wants to close it or transition to another window
    
    reportItems=[]
    reportNumber = 0
    
    while True:
            event, values = managerWindow.read()
            
            if event == "Exit"  or event == sg.WIN_CLOSED :
                break
            elif event == "Return to Homepage":
                managerWindow.close()
                managerPage()
            elif event == "Generate Report":
                try:
                    reportGenerate = pd.DataFrame(columns=("date", "total sales", "total expense", "total profit"))
                    for x in reportItems:
                       tempRow = salesDF.loc[salesDF['date'] == x]
                       reportGenerate.loc[len(reportGenerate.index)] = [tempRow['date'][tempRow.index[0]], 
                                                                        tempRow['total sales'][tempRow.index[0]], 
                                                                        tempRow['total expense'][tempRow.index[0]], 
                                                                        tempRow['total profit'][tempRow.index[0]]]
                    reportGenerate.to_csv('report'+str(reportNumber)+'.csv', index = False)
                    reportNumber+=1
                    managerReportPopUp()
                except:
                    pass
            elif event in addButtonKeys :
                try:
                    query = event
                    stopwords = ['add', 'to', 'report']
                    querywords = query.split()
                    resultwords  = [word for word in querywords if word.lower() not in stopwords]
                    result = ' '.join(resultwords)
                    if result in reportItems:
                        pass
                    else:
                        reportItems.append(result)
                        managerWindow["-CART-"].update(reportItems)
                except:
                    pass
            elif event in removeButtonKeys:
                try:
                    query = event
                    stopwords = ['remove', 'from', 'report']
                    querywords = query.split()
                    resultwords  = [word for word in querywords if word.lower() not in stopwords]
                    result = ' '.join(resultwords)
                    reportItems.remove(result)
                    managerWindow["-CART-"].update(reportItems)
                except:
                    pass

    managerWindow.close()

def managerPage():
    layout = [
                [sg.Text("Manager Main Page", justification = "Center", font=("Calibri",25))],
                [sg.Button("Shop",size=(10, 5))],
                [sg.Button("Generate report",size=(10, 5))],
                [sg.Button("Manage Inventory",size=(10, 5))],
                [sg.Button("Close App",size=(10, 5))]
            ]
    
    
        
    mainWindow = sg.Window("Cafe Application", layout,size=(400,500),element_justification = "Center")
        
    while True:
        event, values = mainWindow.read()
            
        if event in ["Exit","Close App", sg.WIN_CLOSED] :
             break
        elif event == "Shop":
            mainWindow.close()
            shopPage()
            break
        elif event == "Generate report":
            mainWindow.close()
            reportPage()
            break
        elif event == "Manage Inventory":
            mainWindow.close
            stockPage()
            break
    mainWindow.close()
    
def logInPage():
    layout = [
    	[sg.Text('Email')],
    	[sg.InputText()],
    	[sg.Text('Password')],
    	[sg.InputText()],
    	[sg.Button('Log-in'),sg.Button('Sign-up')]
    
    ]
    LoginWindow = sg.Window('Log-in Page', layout, size=(500,150))
    
    while True:
        event, values = LoginWindow.read()
        if event is None or event == sg.WIN_CLOSED:
            break
        elif event == 'Sign-up':
            LoginWindow.close()
            SignupPage()
        elif event == 'Log-in':
            LoginWindow.close()
            managerPage()


def SignupPage():
    layout = [[sg.Text('Enter Email : '), sg.InputText(key='Signup1', do_not_clear=False)],
                  [sg.Text('Enter Password : '), sg.InputText(key='Signup2', password_char='*', do_not_clear=False)],
                  [sg.Text('Confirm Password : '), sg.InputText(key='Signup3', password_char='*', do_not_clear=False)],
                  [sg.Button('Sign Up')]
              ]
   
    SignupWindow = sg.Window('Sign Up', layout, size=(500, 125))
    while True:
        event, values = SignupWindow.read()
        email = str(values['Signup1'])
        passwd = str(values['Signup2'])
        CFpasswd = str(values['Signup3'])
        if event is None or event == sg.WIN_CLOSED:
            break
        elif event == 'Sign Up':
            if len(email) == 0 or len(passwd) == 0:
                sg.Popup('Empty inputs')
            elif email.endswith('@gmail.com') == False:
                sg.Popup('Invalid Email!!')
            elif (len(passwd) < 8):
                sg.Popup('Password requires a minium 8 charcters!!')
            elif (passwd != CFpasswd):
                 sg.Popup('Password do not match')
            else:
                SignupWindow.close()
                SignupQuestion()
            
        
    

def SignupQuestion():
    q1 = 'In what city were you born?'
    q2 = 'What is the name of your favorite pet?'
    q3 = 'What is your mothers maiden name?'
    q4 = 'What high school did you attend?'
    q5 = 'What is the name of your first school?'
    List = [q1, q2, q3, q4, q5]
    
    layout = [[sg.Text('Security Questions!\n')],
              [sg.Text('You must enter the following questions in order to create account!\n')],
              [sg.Text('First Question : '), sg.OptionMenu(List, key='q1')],
              [sg.Text('Enter Answer : '), sg.InputText(key='Ans1')],
              [sg.Text('Second Question : '), sg.OptionMenu(List, key='q2')],
              [sg.Text('Enter Answer : '), sg.InputText(key='Ans2')],
              [sg.Text('Third Question : '), sg.OptionMenu(List, key='q3')],
              [sg.Text('Enter Answer : '), sg.InputText(key='Ans3')],
              [sg.Button(' Submit ')]]

    SignupQuestionWindow = sg.Window('Security Questions', layout, size=(500,300))
    
    while True:
        event, values = SignupQuestionWindow.read()
        if event is None or event == sg.WIN_CLOSED:
            break
        elif event == 'submit':
            if len(values['q1']) == 0 or len(values['q2']) == 0 or len(values['q3']) == 0:
                sg.Popup('Please select the questions!')
            elif len(values['Ans1']) == 0 or len(values['Ans2']) == 0 or len(values['Ans3']) == 0:
                sg.Popup('Please answer the questions!')
            elif (values['q1'] == values['q2'] or values['q2'] == values['q3'] or values['q3'] == values['q1']):
                  sg.Popup('Can not select the same question!')
            elif (values['Ans1'] == values['Ans'] or values['Ans2'] == values['Ans3'] or values['Ans3'] == values['Ans1']):
                  sg.Popup('The answers can not be the same!')
            else:
                SignupQuestionWindow.close()
                logInPage()
                  
                 
        
logInPage()     
        
        