from rapidsms.apps.base import AppBase
import re
from models import *
from datetime import datetime
from pathapp.models import Beneficiary
from pathapp.models import Path
from pathapp.models import History
from random import randint
class App(AppBase):

    # message pattern expected: 'PATH register <fname> <lname>'
    reg_pattern = re.compile(r'^path\s+(register|reg)\s+(\S+)\s+(\S+)\s+(\S+)', re.IGNORECASE)
    add_account_pattern = re.compile(r'^path\s+(add)\s+(account)\s+(\d+)', re.IGNORECASE)
    start_pattern = re.compile(r'^path$', re.IGNORECASE)
    surv_pattern = re.compile(r'^surv$', re.IGNORECASE)
    surv_add_pattern = re.compile(r'^surv\s+(\d+)\s+(\d+)\s+(\d+)', re.IGNORECASE)
    transactions_pattern = \
    re.compile(r'^(menu|bal|bill|tfr|cred|hist|help|stop|next|auth)(\#|\*)?(\S+)?', re.IGNORECASE)

    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    ###################################
    # Custom Handler functions
    ###################################

    def menu_handler(self,accounts,entry,message):
        message.respond("Welcome to Mobile PATH.Text your menu option "+\
            "below to 132.\n\nMENU\nBAL\nPWD\nTFR\nCRED\nHIST\nHELP\nSURV")
	#return True
    #return False

    def registration_handler(self,entry,message):
        Beneficiary(
            message_id=message.connection.identity,
            fname=entry[1],
            lname=entry[2],
            question="What is the name of your first Pet?",
            answer=entry[3],
            authenticated=False).save()#(using='path')
        #message.respond("Saving...") 
	#result = Beneficiary.objects.using('path').all()[0]	
	#print result
	
    def add_account_handler(self,result,entry,message):
		print 'adding'
		print result.message_id
		print entry[2]
		time = datetime.now()
		print time
		#try:
		print 'try'
		#Beneficiary().save(using='path')
		#Beneficiary(
		#message_id=message.connection.identity,
		#fname=entry[1],
		#lname=entry[2],
		#question="What is the name of your first Pet?",
		#answer="rex",
		#authenticated=False).save(using='path')
		#Path(
		#beneficiary_id=result.message_id, 
		#balance=entry[2], 		
		#created=datetime.now()).save()#(using='path') #beneficiary_id=result.message_id balance=entry[2], created=datetime.now()
		print 'test'
		Path(balance = entry[2], created = time, identity = result.message_id).save()			
		#History().save()
		#Test().save()
		#except (RuntimeError, TypeError, NameError) as e: tfr*18769991235*50
		#print e
		print 'test'
		message.respond("Account added")

    def bal_handler(self,accounts,entry,message, result):
	#print 'inside bal'
        accts = [(acct.id,acct.balance) for acct in accounts]
        response = "Balance @ "+datetime.now().strftime("%d/%m/%y %H:%M:%S")+\
                "\n"

        acctinfo = []
        x = 1
        for acct in accts:
            acctinfo.append("PATH"+ `x` +": $"+`acct[1]`+"\n")
            x+=1

        for acct in acctinfo:
            response += acct

        response +=" Reply STOP to cancel."

        message.respond(response)

    def bill_handler(self,accounts,entry,message,result):
	print "inside bill"
        args = entry[2].split("*")
	print 'args', args
        to = args[0] 
	print "to", to
        amount = int(args[1]) #int(args[1][4:])
	print "amount", amount
	try:
		print 'try'
		acct_to = Path.objects.filter(identity=to)[0]
		print acct_to
		print 'acct to bal', acct_to.balance
	except:
		print 'not found'
		acct_to = 0	
		#print 'acct_to',acct_to
	if not acct_to:
		print 'account not found'
		msg.respond('Account does not exist')
	else:
		print 'else'
		acct_from = Path.objects.filter(identity=result.message_id)[0]
		print acct_from
		print 'balance from', acct_from.balance
		print 'amount', amount
		if amount <= acct_from.balance :
			print 'balance to',acct_to.balance
			#acct_from = Path.objects.filter(identity=acct2)[0]
	
			acct_from.balance -= amount
			acct_to.balance += amount
			acct_from.save()
			acct_to.save()
			print acct_from.identity
			con = randint(1111111111, 9999999999)
			History(identity=acct_from.identity,date=datetime.now(), message="PMT PATH"+`result.message_id`+" "+to+" - $"+\
				`amount`, confirmation_code = con).save()
			print 'saved' 
			message.respond("You have successfully paid $"+`amount`+" from PATH "+`result.message_id`+\
			"to "+to+". Confirmation \#: 123-456-789 Reply STOP to cancel")
		else:
			message.respond("You do not have sufficient funds to make this transaction. Please add credit and try again")
			#print 'low bro'
        #amount = int(args[1])
	#print 'amount',amount
        #accounts[acct-1].balance -= amount
        #accounts[acct-1].save() #using='path'
        #account = accounts[acct-1]
	print 'end'




    def tfr_handler(self,accounts,entry,message,result):
	print entry #_X
        args = entry[2].split("*")
	print 'args ', args #_X
        acct1 = int(args[0])#[4:])
	print 'account1', acct1 #_X
	#print result.message_id #_X
        acct2 = result.message_id #int(args[1][4:]) #_X
	print 'acct2',acct2 #_X 
        amount = int(args[1])
	print 'amount',amount
	try:
		acct_to = Path.objects.filter(identity=acct1)[0]
	except:
		print 'not found'
		acct_to = 0	
	#print 'acct_to',acct_to
	if not acct_to:
		print 'account not found'
		msg.respond('Account does not exist')
	else:
		acct_from = Path.objects.filter(identity=acct2)[0]
		print acct_from
		print 'balance from', acct_from.balance
		if amount <= acct_from.balance :
			print 'balance to',acct_to.balance
			#acct_from = Path.objects.filter(identity=acct2)[0]
	
			acct_from.balance -= amount
			acct_to.balance += amount
			acct_from.save()
			acct_to.save()
			print acct_from.identity
			con = randint(1111111111, 9999999999)
			#Path(balance = entry[2], created = time, identity = result.message_id).save()
			History(identity=acct_from.identity, date=datetime.now(), message="TFR PATH "+`acct1`+" to PATH "+`acct2`+\
				" - $"+`amount`,confirmation_code = con).save() #,confirmation_code = randint(1111111111, 9999999999)
			message.respond("You have successfully transferred $"+`amount`+\
			        " from PATH "+`acct1`+" to PATH "+`acct2`+".Confirmation #:" + `con` +\
			        "Reply STOP to cancel")
		else:
			message.respond("You do not have sufficient funds to make this transaction. Please add credit and try again")
			
	print 'done'
        #accounts[acct1-1].balance -= amount
        #accounts[acct2-1].balance += amount
        #accounts[acct1-1].save() #using='path'
        #accounts[acct2-1].save() #using='path'
        #account = accounts[acct-1]
        #History(identity=acct_from, date=datetime.now(),\
                #message="TFR PATH"+`acct1`+" to PATH"+`acct2`+" - $"+`amount`,confirmation_code = randint(1111111111, 9999999999))).save()#using='path') #using='path' "TFR PATH"+ acct1 +" to PATH"+acct2+" - $"+ amount



    def cred_handler(self,accounts,entry,message,result): 
        args = entry[2].split("*")
	print args
        acct = result.message_id#int(args[0][4:])
	print acct
        amount = int(args[0])
	print 'amount', amount
	print accounts[0].identity
        accounts[0].balance -= amount #accounts[acct-1].balance -= amount
	print '1'
        accounts[0].save()   #accounts[acct-1].save() #using='path'
	print '2'
	con = randint(1111111111, 9999999999)
        #account = accounts[acct-1]
        History(identity=accounts[0].identity, date=datetime.now(), message="CRED PATH"+`acct`+" - $"+`amount`, confirmation_code = con).save() #using='path'
	print 'respond fail '
        message.respond("You have successfully purchased $"+`amount`+" call credit"+\
                "from PATH"+`acct`+" Card: 123-456-789 Dial *128*1876"+\
                " <receiver's number> * <amount you want to send> # and press send")

    def hist_handler(self,accounts,entry,message,result):
	print 'hist_handler'
	print 'identity',accounts[0].identity
        histlist = History.objects.filter(identity=accounts[0].identity)
        response = "Statement @ "+datetime.now().strftime("%d/%m/%y %H:%M:%S")+\
                "\n"
        for hist in histlist:
            date = hist.date.strftime("%d/%m/%y")
            response += date+" "+hist.message

        response += " Reply NEXT for more info"
        message.respond(response)

    def help_handler(self,accounts,entry,message,result):
        args = entry[1]
        if args == "#":
            message.respond("Call 999-1234 to speak to an MLSS agent.")
        else:
            message.respond("Text menu option below to 132."+\
                "0. MENU 1. BAL 2. PMT 3. TFR"+\
                "4. CRED 5. HIST"+\
                " Reply HELP# to access live help.")

    def stop_handler(self,accounts,entry,message,result):
        args = entry[2].split("*")
        acct = int(args[0][4:])
        accounts[0].delete() #accounts[acct-1].delete()

        message.respond("Mobile Path is now deactivated for PATH "+`acct`+"."+\
                "Call 999-1234 for help")

    def auth_handler(self,result,entry,message):
	args = entry[2].split("*")
	print 'args',args
        if args[0] == result.answer:    #if entry[2] == result.answer:
		try:
			#print 'insode auth'
			#args = entry[2].split("*")
			print 'change to', args[1]
			new_auth = args[1]			
			#result.authenticated = True
			#result.authen_time = datetime.now()
			#result.save()#using='path') #using='path'
	    
			message.respond("Password Changed Succesfully.")
		except:
			print 'fail'
			new_auth = 0

		if not new_auth:
			print 'no auth'
			result.authenticated = True
			result.authen_time = datetime.now()
			message.respond("Authenticated")
			#result.save()
		else:
			result.answer = new_auth
		result.save()
	else:	
		message.respond("The password entered does not match your account, please try again.")


    def next_handler(self,accounts,entry,message,result):
        message.respond(`entry`)
    	
    def surv_handler(self, result, entry, message):
	print entry
	print result.message_id
	Survey(question_one="Did you find the system easy to use (1=Yes; 2=No)", question_two="Would you consider switching to mobile (1=Yes; 			2=No)",question_three="Would you consider switching to mobile (1=Yes; 2=No)", answer_one=entry[0], answer_two=entry[1], 
		answer_three=entry[2], date=datetime.now(),identity=result.message_id).save()
	con = randint(1111111111, 9999999999)
	History(identity=result.message_id, date=datetime.now(), message="PATH survey answered ",confirmation_code = con).save()
	message.respond("Thank you for completting our survey.")
	

    #Rapid sms Handle function
    def handle (self, message):
        response1 = self.start_pattern.findall(message.text)
        response2 = self.reg_pattern.findall(message.text)
        response3 = self.add_account_pattern.findall(message.text)
        response4 = self.transactions_pattern.findall(message.text)
	response5 = self.surv_pattern.findall(message.text)
	response6 = self.surv_add_pattern.findall(message.text)
	
        if response1:
            entry = response1[0]
            self.menu_handler([],entry,message)
        elif response2:
            entry = response2[0]
            self.registration_handler(entry,message)
            message.respond("Registration Successful!")
        else:
			try:
				
				identity = message.connection.identity		
				print 'identity',identity
				#>result = Beneficiary.objects.filter(message_id=message.connection.identity)[0]#(id=identity)[0]
				result = Beneficiary.objects.filter(message_id=identity)[0] #.using('path')
				print 'result', result	
				try:
					authentic = result.authen_time.date()
					print 'try'
				except:
					authentic = datetime.now().date()
					print 'except'
				print 'result time', authentic
				current_date = datetime.now().date()
				print 'time now ', current_date
				time_diff = current_date - authentic
				ind = str(time_diff).index(" ")
				print ind
				days_past = str(time_diff)[:ind]
				print 'days', days_past
				#ind = days_past.index(" ")
				#print ind
				print 'time difference', int(days_past)
				if int(days_past) > 1:
					print 'time'
					result.authenticated = False
					result.save()

				if result:
					boo = Beneficiary.objects.get(message_id=identity) #_X .using('path')
					auth_check = result.authenticated #_X
					print 'auth'
					print auth_check #_X
					"""if auth_check == '0': #_X
						print 'working' #_X
						auth_result = False #_X
					elif auth_check == '1': #_X
						print 'nope' #_X
						auth_result = True #_X """
					#args = entry[2].split("*")
					change = False
					if response4:
						ch = response4[0]
						print 'ch',ch
						an = ch[0]
						print an
						if an == "auth":
							args =ch[2].split("*")
							print 'here', args
							try:
								ex = args[1]
								change = True
							except:
								change = False
							print 'change',change
					if not auth_check or change:#auth_result: #result.authenticated: #_X  try changing authenticated from bool to text
						print 'response 4'  #_X 
						if response4:
							entry = response4[0]
							op = entry[0]
							print op
							if op == "auth":
								meth = '%s_handler' % op
								method = getattr(self, meth, None)
								if method is not None:
									print 'insode'
									method(result,entry,message)
							else:
								message.respond("Thanks for using Mobile PATH. Please "+ \
									"text AUTH*pin(password) ")#answer to security question below "+ \
									#"to 132.\n\n"+result.question)
						else:
							message.respond("Thanks for using Mobile PATH. Please "+ \
								"text AUTH*pin(password) ")#answer to security question below "+ \
								#"to 132.\n\n"+result.question)
					else:
						try:
							print "here now"
							#accounts = Path.objects.using('path').filter(beneficiary_id=result.message_id)
							#print accounts
							#print result.message_id
							accounts = Path.objects.filter(identity=result.message_id)
							if not accounts:
								#print 'response 3'
								print response3
								if response3:
									entry = response3[0]
									print 'inside if'
									self.add_account_handler(result,entry,message)
								else:
									message.respond("Response3 You dont have any path "+\
										"accounts. You can add one with the following"+\
										" command: path add account <initial_amount>")
							elif response4:
								print 'response 4'
								entry = response4[0]
								print entry
								op = entry[0]
								print op
								if op != "auth":
									print "inside loop"
									meth = '%s_handler' % op
									method = getattr(self, meth, None)
									print 'getattr'
									print method
									if method is not None:
										print 'inside method'
										method(accounts,entry,message,result)
								else:
									message.respond("You are already authenticated")
							elif response3:
								entry = response3[0]
								self.add_account_handler(result,entry,message)
							elif response5:
								message.respond("Please answer the following questions: \nDid you find the system 										easy to use (1=Yes; 2=No)\nWhat is your current Payment method (1=Check; 										2=Card)\nWould you consider switching to mobile (1=Yes; 2=No)\nRespond in 										the form: surv <answer for question1> <answer for question2> <answer for 										question3>")
								print 'survey time beeyocth'
							elif response6:
								entry = response6[0]
								print entry
								print "survey time"
								self.surv_handler(result, entry, message)
							else:
								message.respond("Unknown Command")
						except:
							message.respond("Except You dont have any path "+\
								"accounts. You can one with the following"+\
								" command: path add account <initial_amount>")
				else:
					message.respond("We have no record of you on our system. "+\
						"You must register to to use mobilePATH:"+\
						"path register <fname> <lname> <pin(password)>")
			except:
				message.respond("Exception We have no record of you on our system. "+\
					"You must register to to use mobilePATH:"+\
					"path register <fname> <lname> <pin(password)>")
	
	return True
