from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    usertype = models.CharField(max_length = 20)
class Department(models.Model):
    department = models.CharField(max_length=25)

class HOD(models.Model):
    usr_con = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=80)
    email = models.EmailField(max_length=20)
    dptmnt = models.ForeignKey(Department,on_delete=models.CASCADE,null = True)

class Faculty(models.Model):
    usr_con = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=80)
    email = models.EmailField(max_length=20)
    dptmnt = models.ForeignKey(Department,on_delete=models.CASCADE,null = True)

class Student(models.Model):
    usr_con = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=15)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=80)
    rollno = models.CharField(max_length=80)
    batch = models.CharField(max_length=80)
    gender = models.CharField(max_length=80,null = True)
    email = models.EmailField(max_length=20)
    dptmnt = models.ForeignKey(Department,on_delete=models.CASCADE,null = True)
    signing_key = models.CharField(max_length=64,null = True)  # 64 characters for the hexadecimal signing key
    verify_key = models.CharField(max_length=64, null = True) 

class Election(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=40)
    status = models.CharField(max_length=20,default = "Upcoming")
    election_date = models.DateField(null = True)
    erollAddDate = models.DateField(null = True)
    objectionAcceptDate = models.DateField(null = True)#to this date,like end date
    nomination_StartDate = models.DateField(null = True)
    nomination_LastDate = models.DateField(null = True)
    nomiWithdrawDate = models.DateField(null = True)
    campaignDate = models.DateField(null = True)
    campaignEndDate = models.DateField(null = True)
    resultPublishingDate = models.DateField(null = True)
    public_key_n = models.TextField(null = True)
    private_key = models.TextField(null = True)

class ERoll(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE,null = True)
    file = models.FileField()
    date = models.DateField(auto_now_add=True)
    hodsign = models.CharField(max_length=20,default = "Not approved")#Approved#reject

class Objection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE,null = True)
    description = models.CharField(max_length=400)
    date = models.DateField(auto_now_add=True)

class Nomination(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE,null = True)
    file = models.FileField()#candidate image
    proposer = models.EmailField(max_length=30,null = True)
    seconder = models.EmailField(max_length=30,null = True)
    cand_type= models.CharField(max_length=15,null = True)
    date = models.DateField(auto_now_add=True)
    fac_status = models.CharField(max_length=20,default = "Not approved")
    hod_status = models.CharField(max_length=20,default = "Not approved")
    admin_status = models.CharField(max_length=20,default = "Not approved")
    noOfVotes = models.IntegerField(null=True,default = 0)#percentage of votes
    noOfVotesNo = models.IntegerField(null=True,default = 0)#no of votes

class Vote(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    encrypted_vote = models.TextField(null = True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    signature = models.TextField(null = True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE,null = True)




