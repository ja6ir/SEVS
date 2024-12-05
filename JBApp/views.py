from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image
from reportlab.lib.units import inch
import qrcode
from io import BytesIO
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from django.shortcuts import render
from django.utils import timezone


from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import pagesizes
import pytz
from django.http import HttpResponseRedirect
from django.urls import reverse
from nacl.signing import SigningKey
from phe import paillier
from collections import defaultdict
from django.db.models import Q
import json
import os
from django.conf import settings
from reportlab.lib.pagesizes import A4


# Create your views here.

def Index(request):
    elec_count= Election.objects.count()
    voters= Student.objects.count
    return render(request,'index.html',{"e":elec_count, "v":voters})



def login(request):
    if request.POST:
        usname = request.POST["username"]
        pasw = request.POST["password"]
        check_cust_user = authenticate(username=usname,password = pasw)
        if check_cust_user is not None:
                
                
                
                if check_cust_user.is_superuser == True:
                    messages.info(request,"Login successfull")
                    return redirect("/admin_home")
                elif check_cust_user.usertype == "hod":
                    
                   
                    
                    chef = HOD.objects.get(email = usname)
                    request.session['uid'] = chef.id
                    messages.info(request,"Login successfull")
                    return redirect("/hod_home")
                    
                elif check_cust_user.usertype == "faculty":
                    du = Faculty.objects.get(email = usname)
                    request.session['uid'] = du.id
                    messages.info(request,"Login successfull")
                    return redirect("/fac_home")
                elif check_cust_user.usertype == "student":
                    user = Student.objects.get(email = usname)
                    request.session['uid'] = user.id
                    messages.info(request,"Login successfull")
                    return redirect("/stud_home")
        elif CustomUser.objects.filter(username = usname):
            cust = CustomUser.objects.get(username = usname)
            if cust.is_active == 0:
                messages.info(request,"User not approved")
            else:
                messages.info(request,"Password not matching")
        else:
            messages.info(request,"User dosent exist")
    return render(request,'login.html')
def validate_otp(request):

    return render(request,'otp.html')


def admin_home(request):
    return render(request,'admin_home.html')

from django.shortcuts import get_object_or_404

def adm_hod(request):
    if request.method == "POST":

        if 'delete_hod' in request.POST:
            hod_id = request.POST["hod_id"]
            hod = get_object_or_404(HOD, id=hod_id)
            hod.usr_con.delete()
            hod.delete()
            messages.info(request, "HOD deleted successfully")
            return redirect('adm_hod')

        else:

            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            contact =  request.POST["contact"]
            email = request.POST["email"]
            username = email
            password = generate_otp(8, True)
            address = request.POST["address"]
            department = request.POST["department"]
            dptmnt = get_object_or_404(Department, id=department)

            if HOD.objects.filter(dptmnt__department=dptmnt.department).exists():
                messages.info(request, "HOD already exists in this department")
            else:
                data_to_user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    is_active=1,
                    usertype="hod"
                )
                data_to_user.save()
                data_to_reg = HOD.objects.create(
                    name=first_name,
                    contact=contact,
                    address=address,
                    email=email,
                    usr_con=data_to_user,
                    dptmnt=dptmnt
                )
                data_to_reg.save()
                messages.info(request, "HOD added successfully. Login credentials have been sent to the registered email")
                send_email(f"Hello {first_name}, Welcome to JB election. Please use these login credentials to log on to the portal. Email: {email} Password: {password}", email)
                return redirect('adm_hod')
        
    data = Department.objects.all()
    hods = HOD.objects.all()
    return render(request, 'adm_hod.html', {"data": data, "hods": hods})

def adm_elec(request):
    if request.POST:
        title = request.POST["title"]
        election_date = request.POST["election_date"]
        eroll_date = request.POST["eroll_date"]
        obj_date = request.POST["obj_date"]
        nomi_Sdate = request.POST["nomi_Sdate"]
        nomi_Edate = request.POST["nomi_Edate"]
        nomiwithraw_Ldate = request.POST["nomiwithraw_Ldate"]
        camp_Sdate = request.POST["camp_Sdate"]
        camp_Edate = request.POST["camp_Edate"]
        result_date = request.POST["result_date"]
        public_key, private_key = paillier.generate_paillier_keypair()
        private_key_dict = {'p': private_key.p, 'q': private_key.q}
        dataToReg = Election.objects.create(title = title,
                                            erollAddDate = eroll_date,
                                            objectionAcceptDate = obj_date,
                                            nomination_StartDate = nomi_Sdate,
                                            nomination_LastDate = nomi_Edate,
                                            nomiWithdrawDate = nomiwithraw_Ldate,
                                            campaignDate = camp_Sdate,
                                            campaignEndDate = camp_Edate,
                                            resultPublishingDate = result_date,
                                            election_date = election_date,
                                            public_key_n=str(public_key.n),
                                            private_key=json.dumps(private_key_dict))
        dataToReg.save()
        messages.info(request,"Election added")
    data = Election.objects.all()
    return render(request,'adm_elec.html',{"data":data})

def adm_liveElec(request):
    id = request.GET.get('id')
    election = Election.objects.get(id = id)
    if Election.objects.filter(status = "Live").exists():
        messages.info(request,"Already an election in progress, please mark it as completed and try again")
    else:
        election.status = "Live"
        election.save()
    return redirect('/adm_elec')

def adm_completeElec(request):
    id = request.GET.get('id')
    election = Election.objects.get(id = id)
    election.status = "Completed"
    election.save()
    return redirect('/adm_elec')

def adm_eroll(request):
    election = Election.objects.get(status = "Live")
    data = ERoll.objects.filter(Q(election__id = election.id) & Q(hodsign = "Approved"))
    return render(request,'adm_eroll.html',{"data":data})

def adm_obj(request):
    # uid = request.session["uid"]
    election = Election.objects.get(status = "Live")
    data = Objection.objects.filter(election__id = election.id)
    return render(request,'adm_obj.html',{"data":data})

def adm_nomi(request):
    election = Election.objects.get(status = "Live")
    data = Nomination.objects.filter(Q(hod_status = "Approved") & Q(election__id = election.id) & Q(fac_status = "Approved"))
    return render(request,'adm_nomi.html',{"data":data})

def view_paper_trails(request):
    # Path to the paper trails folder
    paper_trail_folder = os.path.join(settings.BASE_DIR, 'static', 'papertrails')
    
    # Collect file info in a list of dictionaries
    files = []
    for filename in os.listdir(paper_trail_folder):
        if filename.endswith('.pdf'):
            file_path = os.path.join('static', 'papertrails', filename)
            # You can include more details as needed (e.g., upload date, uploader)
            files.append({
                'file': file_path,
                'filename': filename,
                'date': timezone.now(),  # Placeholder; replace with actual upload date if available
                # 'faculty': 'Some Faculty Name',  # Add real data if available
                # 'department': 'Department Name', # Add real data if available
            })

    context = {'data': files}
    return render(request, 'adm_paper.html', context)

def hod_home(request):
    return render(request,'hod_home.html')

def hod_faculty(request):
    uid = request.session["uid"]
    hod = HOD.objects.get(id = uid)
    dptmnt = Department.objects.get(id = hod.dptmnt.id)
    if request.POST:
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        contact =  request.POST["contact"]
        email = request.POST["email"]
        username = email
        password = generate_otp(8, True)
        address = request.POST["address"]
        print(password)
        dataToUser = CustomUser.objects.create_user(first_name = first_name,
                                        last_name = last_name,
                                        username = username,
                                        email = email,
                                        password = password,
                                        is_active = 1,
                                        usertype = "faculty")
        dataToUser.save()
        dataToReg = Faculty.objects.create(name = first_name,
                                        contact = contact,
                                        address = address,
                                        email = email,
                                        usr_con = dataToUser,
                                        dptmnt = dptmnt)
        dataToReg.save()
        messages.info(request, "Faculty added successfully. Login credentials have been sent to the registered email ")
        send_email(f"Hello {first_name}, Welcome to JB election. Please use these login credentials to log on to the portal. Email: {email} Password: {password}", email)
    data = Faculty.objects.filter(dptmnt__id = dptmnt.id)
    return render(request,'hod_faculty.html',{"data":data})

def hod_eroll(request):
    uid = request.session["uid"]
    hod = HOD.objects.get(id = uid)
    data = ERoll.objects.filter(Q(faculty__dptmnt__id = hod.dptmnt.id) & Q(hodsign = "Not approved") | Q(hodsign = "Approved"))
    return render(request,'hod_eroll.html',{"data":data})

def delete(request):
    id=request.GET.get('id')
    action = request.GET.get('action')
    if action=='delete_fac':
        data=Faculty.objects.get(id=id)
        user = data.usr_con
        user.delete()
        messages.info(request,"Faculty Removed")
        return redirect("/hod_faculty")
    elif action=='delete_stud':
        data = Student.objects.get(id=id)
        user = data.usr_con
        user.delete()
        messages.info(request,"Student Removed")
        return redirect("/fac_stud")
    else:
        messages.info(request,"Unable to remove")

        return redirect("/login")
def hod_approveEroll(request):
    uid = request.session["uid"]
    id = request.GET.get('id')
    action = request.GET.get('action')
    data = ERoll.objects.get(id = id)
    if action == "approve":
        data.hodsign = "Approved"
        data.save()
        messages.info(request,"E-Roll approved")
        return redirect("/hod_eroll")
    elif action == "reject":
        data.delete()
        messages.info(request,"E-Roll rejected")
        return redirect("/hod_eroll")
    elif action == "adm_reject":
        data.delete()
        messages.info(request,"E-Roll rejected")
        return redirect("/adm_eroll")

def hod_obj(request):
    uid = request.session["uid"]
    hod = HOD.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    data = Objection.objects.filter(election__id = election.id)
    return render(request,'hod_obj.html',{"data":data})

def hod_nomi(request):
    uid = request.session["uid"]
    faculty = HOD.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    data = Nomination.objects.filter(Q(student__dptmnt__id = faculty.dptmnt.id) & Q(election__id = election.id) & Q(fac_status = "Approved"))
    return render(request,'hod_nomi.html',{"data":data})

def fac_home(request):
    return render(request,'fac_home.html')

def fac_stud(request):
    uid = request.session["uid"]
    hod = Faculty.objects.get(id = uid)
    dptmnt = Department.objects.get(id = hod.dptmnt.id)
    if request.POST:
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        contact =  request.POST["contact"]
        email = request.POST["email"]
        gender= request.POST["gender"]
        username = email
        password ="123" #generate_otp(8, True)
        address = request.POST["address"]
        rollno = request.POST["rollno"]
        batch = request.POST["batch"]
        if Student.objects.filter(rollno = rollno , batch= batch).exists():
            messages.info(request,"Admission no already exists")
        else:

            signing_key = SigningKey.generate()
            verify_key = signing_key.verify_key

            dataToUser = CustomUser.objects.create_user(first_name = first_name,
                                            last_name = last_name,
                                            username = username,
                                            email = email,
                                            password = password,
                                            is_active = 1,
                                            usertype = "student")
            dataToUser.save()

            dataToReg = Student.objects.create(name = first_name,
                                            contact = contact,
                                            address = address,
                                            email = email,
                                            rollno = rollno,
                                            gender= gender,
                                            batch = batch,
                                            usr_con = dataToUser,
                                            dptmnt = dptmnt,
                                            signing_key=signing_key.encode().hex(),
                                            verify_key=verify_key.encode().hex())
            dataToReg.save()
            messages.info(request, "Student added successfully. Login credentials have been sent to the registered email")
            send_email(f"Hello {first_name}, Welcome to JB election. Please use these login credentials to log on to the portal. Email: {email} Password: {password}", email)
    data = Student.objects.filter(dptmnt__id = dptmnt.id)

    
    return render(request,'fac_stud.html',{"data":data})

def fac_eroll(request):
    uid = request.session["uid"]
    faculty = Faculty.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    

    if request.POST:
        eroll_exists = ERoll.objects.filter(faculty=faculty, election=election).exists()
        if not eroll_exists:
            batch = request.POST["batch"]
            
            department_name = faculty.dptmnt.department
            
            title_text ="JaiBharath Arts And Science College, Arackappady"
            sbtitle_text = "Election Roll"
            sbsbtitle_text = f"Department: {department_name}, Batch: {batch}"
            c_datetime= datetime.today()
            date=c_datetime.date()
            datetext = f"Published on : {date}"

            # PDF Creation setup
            uniqid=generate_otp()
            pdf_path = f"static/media/students_table_{uniqid}.pdf"
            pdf = SimpleDocTemplate(pdf_path,
            pagesize=pagesizes.letter, 
            leftMargin=72, 
            rightMargin=72, 
            topMargin=72, 
            bottomMargin=72
             )

            # Draw the title
            styles = getSampleStyleSheet()
            title = Paragraph(title_text, styles['Title'])
            sbtitle = Paragraph(sbtitle_text, styles['Heading1'])
            sbsbtitle = Paragraph(sbsbtitle_text, styles['Heading2'])
            datet = Paragraph(datetext, styles['Heading2'])

            # Table data
            table_data = [['Name', 'Gender', 'Roll No']]  # Add other headers as needed
            students = Student.objects.filter(Q(dptmnt__id = faculty.dptmnt.id)& Q(batch = batch))
            # Populate the table with student data
            for student in students:
                table_data.append([student.name, student.gender, student.rollno])

            # Create Table object
            table = Table(table_data)
            # Define your page width and margins
            page_width = pagesizes.letter[0]
            left_margin, right_margin = 72, 72  # One inch each for default
            # Define column widths - equally distributed across the page width
            number_of_columns = len(table_data[0])
            column_width = (page_width - (left_margin + right_margin)) / number_of_columns

            # Set up table object with column widths
            table = Table(table_data, colWidths=[column_width] * number_of_columns)


            # Define Table Style
            table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 1), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
             ])

            table.setStyle(table_style)

            # Build the PDF with title and table
            elements = [title, sbtitle,sbsbtitle, datet, table]
            pdf.build(elements)

            print(f"PDF created with title at {pdf_path}")
            file = pdf_path
            dataToReg = ERoll.objects.create(faculty = faculty,
                                         election = election,
                                        file = file)
            dataToReg.save()
            messages.info(request,"E-Roll added")
            return HttpResponseRedirect(reverse('fac_eroll'))  # Redirect to the same view after POST
        elif eroll_exists: 
            messages.info(request,"E-Roll already exists")
            return HttpResponseRedirect(reverse('fac_eroll'))
    
    data = ERoll.objects.filter(faculty__id = uid)
    fac = get_object_or_404(Faculty, id=uid)
    return render(request,'fac_eroll.html',{"data": data, "fac": fac})

def fac_nomi(request):
    uid = request.session["uid"]
    faculty = Faculty.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    data = Nomination.objects.filter(Q(student__dptmnt__id = faculty.dptmnt.id) & Q(election__id = election.id))
    
    return render(request,'fac_nomi.html',{"data": data})

def fac_approvNomi(request):
    id = request.GET.get('id')
    action = request.GET.get('action')
    data = Nomination.objects.get(id = id)
    if action == "approve":
        data.fac_status = "Approved"
        data.save()
        messages.info(request,"Nomination approved")
        return redirect("/fac_nomi")
    elif action == "reject":
        data.fac_status = "Rejected"
        data.save()
        messages.info(request,"Nomination rejected")
        return redirect("/fac_nomi")
    elif action == "hodapprove":
        data.hod_status = "Approved"
        data.save()
        messages.info(request,"Nomination approved")
        return redirect("/hod_nomi")
    elif action == "hodreject":
        data.hod_status = "Rejected"
        data.save()
        messages.info(request,"Nomination rejected")
        return redirect("/hod_nomi")
    elif action == "admapprove":
        data.admin_status = "Approved"
        data.save()
        messages.info(request,"Nomination approved")
        return redirect("/adm_nomi")
    elif action == "admreject":
        data.admin_status = "Rejected"
        data.save()
        messages.info(request,"Nomination rejected")
        return redirect("/adm_nomi")
    elif action == "studWithdraw":
        data.delete()
        messages.info(request,"Nomination withdrawn")
        return redirect("/stude_nomi")

def stud_home(request):
    uid = request.session["uid"]
    student = Student.objects.get(id = uid)
    name = student.usr_con.first_name + " " + student.usr_con.last_name 
    return render(request,'stud_home.html',{"name":name})

def stude_eroll(request):
    today=date.today()
    uid = request.session["uid"]
    student = Student.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    faculty = Faculty.objects.get(dptmnt=student.dptmnt)
    objLDate = election.objectionAcceptDate
    data = ERoll.objects.filter(Q(election__id = election.id) & Q(hodsign = "Approved"))
    if request.POST:
        description = request.POST["objection"]
        objection = Objection.objects.create(student = student,
                                    election = election,
                                    description = description)
        objection.save()
        messages.info(request,"E-Objection added")
    return render(request,'stude_eroll.html',{"data":data,"today":today,"lastDate":objLDate})

def stude_nomi(request):
    uid = request.session["uid"]
    student = Student.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    today=date.today()
    objSDate = election.nomination_StartDate
    objLDate = election.nomination_LastDate
    withdraw = election.nomiWithdrawDate
    if request.POST:
        attendance = request.POST["attendance"]
        sem = request.POST["sem"]
        criminalcase = request.POST["criminalcase"]
        university = request.POST["university"]
        ugpg = request.POST["ugpg"]
        age1 = request.POST["age"]
        age = int(age1)
        proposer = request.POST["proposer"]
        seconder = request.POST["seconder"]
        file = request.FILES["file"]
        if student.gender == "male":
            cand_type="male"
        elif student.gender == "female":
            cand_type="female"
        else : messages.info(request,"Please specify your correct gender")

        
        if attendance == "no":
            messages.info(request,"More than 75 percent of attendance is mandatory for nomination")
        elif sem == "no":
            messages.info(request,"No backlogs allowed for nomination")
        elif criminalcase == "yes":
            messages.info(request,"Criminal background is not encouraged for nomination")
        elif university == "yes":
            messages.info(request,"University disciplinary actions found, not eligible")
        elif proposer == seconder:
            messages.info(request,"Proposer and seconder cannot be the same")
        elif Nomination.objects.filter(Q(election__status = "Live") & Q(proposer = proposer)).exists():
            messages.info(request,"One student cannot be proposer for more than one candidate")
        elif Nomination.objects.filter(Q(election__status = "Live") & Q(seconder = seconder)).exists():
            messages.info(request,"One student cannot be seconder for more than one candidate")
        elif student.email == proposer or student.email == seconder:
            messages.info(request,"Yourself cannot be a proposer or seconder")
        elif Student.objects.filter(email = proposer).exists():
            if Student.objects.filter(email = seconder).exists():
                if ugpg == "ug":
                    if age < 21:
                        messages.info(request,"UG candidates age should be greater than or equal to 21")
                    else:
                        objection = Nomination.objects.create(student = student,
                                                            election = election,
                                                            file = file,
                                                            proposer = proposer,
                                                            seconder = seconder,
                                                            cand_type = cand_type)
                        objection.save()
                        messages.info(request,"Nomination requested")
                elif ugpg == "pg":
                    if age < 25:
                        messages.info(request,"UG candidates age should be greater than or equal to 25")
                    else:
                        objection = Nomination.objects.create(student = student,
                                                            election = election,
                                                            file = file,
                                                            proposer = proposer,
                                                            seconder = seconder,
                                                            cand_type = cand_type)
                        objection.save()
                        messages.info(request,"Nomination requested")
            else:
                messages.info(request,"Seconders email id should be registered in college")
        else:
            messages.info(request,"Proposers email id should be registered in college")
    if Nomination.objects.filter(Q(student__id = uid) & Q(election__id = election.id)).exists():
        data = Nomination.objects.filter(Q(student__id = uid) & Q(election__id = election.id))
    else:
        data = None
    return render(request,'stude_nomi.html',{"today":today,"lastDate":objLDate,"startDate":objSDate,"data":data,"withdraw":withdraw})

def stude_cand(request):
    today=date.today()
    uid = request.session["uid"]
    student = Student.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    campaignDate = election.campaignDate
    campaignEndDate = election.campaignEndDate
    data = Nomination.objects.filter(Q(election__id = election.id) & Q(hod_status = "Approved")& Q(fac_status = "Approved")& Q(admin_status = "Approved"))
    return render(request,'stude_cand.html',{"data":data,"today":today,"campaignDate":campaignDate,"campaignEndDate":campaignEndDate})

def stude_vote(request):
    uid = request.session["uid"]
    today=date.today()
    #desired_date = date(2024, 4, 7)
    #today= desired_date
    current_time = datetime.now().time()
    ist = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now()
# Convert the current time to IST
    ist_time = current_datetime.astimezone(ist)
    current_time = ist_time.time()
    print("ddd ", current_time)
    print("ddd ", today)
    time1 = datetime.strptime("06:30:00", "%H:%M:%S").time()
    time2 = datetime.strptime("23:00:00", "%H:%M:%S").time()
    # print(current_time)
    student = Student.objects.get(id = uid)
    print(student.batch)
    election = Election.objects.get(status = "Live")
    election_date = election.election_date
    id=election.title
    print(id)
    data = Nomination.objects.filter(Q(election__id = election.id) & Q(hod_status = "Approved") & Q(fac_status = "Approved") & Q(admin_status = "Approved") & Q(student__dptmnt__id = student.dptmnt.id) & Q(student__batch = student.batch))
    checking = Vote.objects.filter(Q(student__id = uid) & Q(election__id = election.id))
   
    voted_male = Vote.objects.filter(Q(student__id = uid) & Q(election__id = election.id))#& Q(nomination__cand_type='male')

    voted_female = Vote.objects.filter(Q(student__id = uid) & Q(election__id = election.id))#& Q(nomination__cand_type='female')
       
    return render(request,'stude_vote.html',{"data":data,"today":today,"current_time":current_time,"election_date":election_date,"time1":time1,"time2":time2,"checking":checking,'voted_male': voted_male,'voted_female': voted_female})

def stud_addvote(request):
    uid = request.session["uid"]
    student = Student.objects.get(id = uid)
    election = Election.objects.get(status = "Live")
    id = request.GET.get('id')

    # Retrieve the public key n from the database
    public_key_n = election.public_key_n
    public_key = paillier.PaillierPublicKey(n=int(public_key_n))

    
    
    # Retrieve the voter's signing key for signing the encrypted vote
    signing_key_hex = student.signing_key  # Assuming `Student` model has the `signing_key` field
    signing_key = SigningKey(bytes.fromhex(signing_key_hex))
   
    
    # Encrypt the nomination ID
    encrypted_vote = public_key.encrypt(int(id))
    # Sign the encrypted vote's ciphertext
    signature = signing_key.sign(str(encrypted_vote.ciphertext()).encode()).signature.hex()

    to_Vote = Vote.objects.create(student = student, election = election, encrypted_vote=str(encrypted_vote.ciphertext()), signature=signature)
    to_Vote.save()

    # Retrieve candidate information for the paper trail
    candidate = Nomination.objects.get(id=id)  
    department_name = student.dptmnt.department  
    batch = student.batch  

    # Set up PDF file path
    papertrail_dir = os.path.join(settings.BASE_DIR, 'static', 'papertrails')
    os.makedirs(papertrail_dir, exist_ok=True)  # Create the directory if it doesn't exist
    pdf_filename = f"PaperTrail_{election.title}_{department_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(papertrail_dir, pdf_filename)

    # Generate the PDF file
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)  # Use 'letter' or any other size
    elements = []

    # Title
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    title_style = styles["Title"]
    candidate_style = ParagraphStyle(
        'CandidateName',
        fontSize=16,
        leading=20,
        spaceAfter=0.3 * inch,
        textColor="blue"
    )

    # Add title
    title = Paragraph(f"Paper Trail for Election: {election.title}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))  # Add some space after the title
    candidate_paragraph = Paragraph(f"Candidate: {candidate.student.name}", candidate_style)
    elements.append(candidate_paragraph)
    elements.append(Spacer(1, 0.2 * inch))  # Add space after the candidate name

    # Add table headers and data
    details = [
        f"Department: {department_name}",
        f"Batch: {batch}",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]

    for detail in details:
        paragraph = Paragraph(detail, normal_style)
        elements.append(paragraph)
        elements.append(Spacer(1, 0.1 * inch))  # Space between each paragraph

    
    qr = qrcode.make(signature)
    qr_buffer = BytesIO()
    qr.save(qr_buffer)
    qr_buffer.seek(0)

    # Add QR code to the document
    qr_image = Image(qr_buffer, width=2 * inch, height=2 * inch)
    elements.append(Spacer(1, 0.2 * inch))  # Add space before the QR code
    elements.append(Paragraph("Signature:", normal_style))
    elements.append(qr_image)

    # Build and save the PDF document
    doc.build(elements)


    return redirect("/stude_vote")

def result(request):
    election = Election.objects.get(status = "Live")
    departments = Department.objects.all()

    return render(request,'result.html',{"dept":departments})

def resultProgress(request):
    # Get department ID and batch from request
    dptid = request.GET.get('dptid')
    batch = request.GET.get('batch')

    # Retrieve the active election
    election = Election.objects.get(status="Live")

    # Filter votes based on department, batch, and election status
    votes = Vote.objects.filter(
        Q(election__id=election.id) &
        Q(student__batch=batch) &
        Q(student__dptmnt__id=dptid)
    )

    # Count the total number of votes
    total_vote_count = votes.count()

    # Initialize the public key for homomorphic encryption
    public_key_n = election.public_key_n
    public_key = paillier.PaillierPublicKey(n=int(public_key_n))

    # Prepare a dictionary to hold decrypted vote counts
    vote_counts = defaultdict(int)

    # Load the private key securely (ensure this is loaded from a secure source)
    private_key_data = json.loads(election.private_key)
    private_key = paillier.PaillierPrivateKey(public_key, private_key_data['p'], private_key_data['q'])

    # Decrypt each vote and tally for each candidate
    for vote in votes:
        encrypted_vote = paillier.EncryptedNumber(public_key, int(vote.encrypted_vote))
        candidate_id = private_key.decrypt(encrypted_vote)

        # Increment the count for the decrypted candidate ID
        vote_counts[candidate_id] += 1

    # Retrieve the nominations for the active election, department, and batch
    nominations = Nomination.objects.filter(
        Q(election__id=election.id) &
        Q(student__dptmnt__id=dptid) &
        Q(student__batch=batch) &
        Q(hod_status="Approved") &
        Q(fac_status="Approved") &
        Q(admin_status="Approved")
    )

    # Calculate the percentage of votes for each nomination and update the counts
    if total_vote_count > 0:
        for nomination in nominations:
            # Get the number of votes for this candidate
            candidate_vote_count = vote_counts.get(nomination.id, 0)
            
            # Calculate the percentage
            percentage = (candidate_vote_count / total_vote_count) * 100

            # Update the nomination with the number of votes and the percentage
            nomination.noOfVotes = round(percentage, 2)
            nomination.noOfVotesNo = candidate_vote_count
            nomination.save()

    # Render the result progress page
    return render(request, 'resultProgress.html', {"nominations": nominations, "count": total_vote_count})


import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants for Gmail SMTP server
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # SSL port for SMTP
SMTP_USERNAME =  'jbelection.admi@gmail.com'
SMTP_PASSWORD = 'aktj udgv ijmy eyek'
print(SMTP_USERNAME, SMTP_PASSWORD)

def generate_otp(length=6, alphanumeric=False):
    """
    Generate a One-Time Password (OTP).
    
    :param length: Length of the OTP to generate.
    :param alphanumeric: Whether the OTP should be alphanumeric or numeric only.
    :return: A string containing the OTP.
    """
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' if alphanumeric else '0123456789'
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def send_email(content,recipient):
    """
    Send an email containing the OTP.

    :param otp: The One-Time Password to send.
    :param recipient: The email address to send the OTP to.
    :return: None
    """
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = SMTP_USERNAME
    message['To'] = recipient
    message['Subject'] = "JB Election"
    message.attach(MIMEText(content, 'plain'))

    # Establish a secure session with Gmail's outgoing SMTP server using SSL
    session = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    session.login(SMTP_USERNAME, SMTP_PASSWORD)  # Login to the server
    text = message.as_string()
    session.sendmail(SMTP_USERNAME, recipient, text)
    session.quit()
