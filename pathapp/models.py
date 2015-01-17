from django.db import models

# Create your models here.


class Beneficiary(models.Model):
    	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
    	date = models.DateTimeField(auto_now_add=True)
    	message_id = models.CharField(max_length=64)
    	question = models.CharField(max_length=255)
	answer = models.CharField(max_length=255)
    	identity = models.CharField(max_length=100)
    	authenticated = models.BooleanField()
	authen_time = models.DateTimeField(null=True)
	
	def __unicode__(self):
		return self.message_id

	
class Path(models.Model):
	beneficiary_id = models.ForeignKey(Beneficiary, null=True)
	balance = models.FloatField()
	created = models.DateTimeField()
	identity = models.CharField(max_length=255)



class History(models.Model):
	#beneficiary_id = models.ForeignKey(Beneficiary)
	#path_id = models.ForeignKey(Path)
	date = models.DateTimeField()
	message = models.TextField()
	identity = models.CharField(max_length=100)
	confirmation_code = models.FloatField()



class Survey(models.Model):
	date = models.DateTimeField()
	question_one = models.CharField(max_length=255)
	question_two = models.CharField(max_length=255)
	question_three = models.CharField(max_length=255)
	answer_one = models.CharField(max_length=100)
	answer_two = models.CharField(max_length=100)
	answer_three = models.CharField(max_length=100)
	identity= models.CharField(max_length=100)

#id=message.connection.identity,
            #fname=entry[1],
            #lname=entry[2],
            #question="What is the name of your first Pet?",
            #answer="rex",
            #authenticated=False).save()
        #message.respond("Saving...")



    #def __unicode__(self):
        #return self.identity[:]
