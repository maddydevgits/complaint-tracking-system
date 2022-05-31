from flask import Flask,render_template,redirect,request,session
from web3 import Web3, HTTPProvider
import json
from ca import *
import random

blockchainAddress='http://127.0.0.1:8545'

def createComplaintId():
    while True:
        k=random.randint(1,9999)
        f=open('ids.txt','r')
        a=f.readlines()
        f.close()
        a=[int(i) for i in a]
        f.close()
        if k not in a:
            f=open('ids.txt','a')
            f.write(str(k)+'\n')
            f.close()
            break
    return(k)

def connect_with_register_blockchain(acc):
    web3=Web3(HTTPProvider(blockchainAddress))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc

    artifact_path='../build/contracts/register.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
    
    contract=web3.eth.contract(address=registerAddress,abi=contract_abi)
    print('Connected with Register Contract')
    return contract,web3

def connect_with_complaint_blockchain(acc):
    web3=Web3(HTTPProvider(blockchainAddress))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc

    artifact_path='../build/contracts/complaint.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
    
    contract=web3.eth.contract(address=complaintAddress,abi=contract_abi)
    print('Connected with Complaint Contract')
    return contract,web3

app=Flask(__name__)
app.secret_key='m@keskilled'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/admin')
def updateComplaint():
    return render_template('updateComplaint.html')

@app.route('/unlockForm',methods=['POST','GET'])
def unlockForm():
    unlockid=request.form['unlockid']
    if(int(unlockid)==100):
        contract,web3=connect_with_register_blockchain(0)
        _users,_names,_passwords,_emails=contract.functions.viewUsers().call()

        contract,web3=connect_with_complaint_blockchain(0)
        _users1,_ids,_complaints,_statuses=contract.functions.listComplaints().call()
        data=[]
        for i in range(len(_complaints)):
            if _statuses[i]!=2:
                dummy=[]
                dummy.append(_ids[i])
                data.append(dummy)
        l=len(data)
        return render_template('updateComp.html',len=l,dashboard_data=data)
    else:
        return redirect('/admin')

@app.route('/dashboard')
def dashboardPage():
    contract,web3=connect_with_register_blockchain(session['walletaddr'])
    _users,_names,_passwords,_emails=contract.functions.viewUsers().call()

    contract,web3=connect_with_complaint_blockchain(session['walletaddr'])
    _users,_ids,_complaints,_statuses=contract.functions.listComplaints().call()
    data=[]
    for i in range(len(_complaints)):
        if _users[i]==session['walletaddr']:
            dummy=[]
            dummy.append(_ids[i])
            dummy.append(_complaints[i])
            userIndex=_users.index(session['walletaddr'])
            dummy.append(_names[userIndex])
            if(_statuses[i]==0):
                dummy.append('Not Started')
            elif (_statuses[i]==1):
                dummy.append('In Progress')
            elif (_statuses[i]==2):
                dummy.append('Ticket Closed')
            
            data.append(dummy)

    l=len(data)
    return render_template('dashboard.html',len=l,dashboard_data=data)

@app.route('/updateCompForm',methods=['POST','GET'])
def updateCompForm():
    complaintId=int(request.form['complaintId'])
    complaintStatus=int(request.form['complaintStatus'])
    print(complaintId,complaintStatus)
    contract,web3=connect_with_complaint_blockchain(0)
    tx_hash=contract.functions.updateComplaint(complaintId,complaintStatus).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    
    contract,web3=connect_with_register_blockchain(0)
    _users,_names,_passwords,_emails=contract.functions.viewUsers().call()

    contract,web3=connect_with_complaint_blockchain(0)
    _users1,_ids,_complaints,_statuses=contract.functions.listComplaints().call()
    data=[]
    for i in range(len(_complaints)):
        if _statuses[i]!=2:
            dummy=[]
            dummy.append(_ids[i])
            data.append(dummy)
    l=len(data)
    return render_template('updateComp.html',len=l,dashboard_data=data)

@app.route('/createComplaint')
def createComplaintPage():
    return render_template('createComplaint.html')

@app.route('/createComplaintForm',methods=['POST','GET'])
def createComplaintFormPage():
    complaint=request.form['complaint']
    walletaddr=session['walletaddr']
    id=createComplaintId()
    contract,web3=connect_with_complaint_blockchain(walletaddr)
    tx_hash=contract.functions.addComplaint(walletaddr,id,complaint).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/dashboard')


@app.route('/logout')
def logoutPage():
    return render_template('index.html')

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    walletaddr=request.form['walletaddr']
    name=request.form['name']
    password=request.form['password']
    email=request.form['email']
    print(walletaddr,name,password,email)
    contract,web3=connect_with_register_blockchain(walletaddr)
    tx_hash=contract.functions.registerUser(walletaddr,name,int(password),email).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(redirect('/login'))

@app.route('/loginUser',methods=['POST','GET'])
def loginUser():
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    print(walletaddr,password)
    contract,web3=connect_with_register_blockchain(walletaddr)
    state=contract.functions.loginUser(walletaddr,password).call()
    if state==True:
        session['walletaddr']=walletaddr
        return(redirect('/dashboard'))
    else:
        return redirect('/login')

if(__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5000)