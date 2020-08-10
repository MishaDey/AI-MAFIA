import os
import ssl
import smtplib
import getpass
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def create_message_template(ext_message_file_path):
    message_template_file=open(ext_message_file_path,mode='w',encoding='utf-8')
    message_template_file.write(input("Enter your message:"))
    message_template_file.close()    
    
def create_recipents_list(ext_contacts_file_path):
    recipents=open(ext_contacts_file_path,mode='w',encoding='utf-8')
    rescipent_no=input("Enter the no. of rescipents:")
    for i in range(rescipent_no):
        recipent_list=input("Enter your Recipents address: ")
        recipents.write(recipents_list+'\n')
    recipents.close()

def extract_recipents_ext_file(ext_contacts_file_path):
    recipent_name=[]
    email_id=[]
    with open(ext_contacts_file_path, mode='r' , encoding ='utf-8') as ext_cont_file:
        for contact in ext_cont_file:
            recipent_name.append(contact.split()[0])
            email_id.append(contact.split()[1])
    return recipent_name,email_id

def extract_message_template(ext_message_file_path):
    with open(ext_message_file_path,'r',encoding='utf-8') as message_template_file:
        extracted_message=message_template_file.read()
    return extracted_message

def send_personalized_email(user_Address,recipent_mail,extracted_message,subject,file_to_attach,attachment,filename):
    message=MIMEMultipart()
    message['From']=user_Address
    message['To']=recipent_mail
    message['Subject']=subject
    message_body=MIMEText(extracted_message,'plain')
    message.attach(message_body)
    attach_f=MIMEBase('application','octet-stream')
    attach_f.set_payload((attachment).read())
    encoders.encode_base64(attach_f)
    attach_f.add_header('Content-Disposition',"attachment; filename =%s" % filename)
    message.attach(attach_f)
    return message  

def set_SMPT_server(smtp_server,port,user_Address,User_Password,ext_contacts_file_path,ext_message_file_path):
    subject=input("Enter Subject: ")
    #create_recipents_list(ext_contacts_file_path)
    create_message_template(ext_message_file_path)
    extracted_message=extract_message_template(ext_message_file_path)
    print(extracted_message)
    recipent_name,res_email_ids=extract_recipents_ext_file(ext_contacts_file_path)
    print(recipent_name,res_email_ids)
    context = ssl.create_default_context()
    file_to_attach=input("Enter the complete file path you wish to attach :")
    attachment=open(file_to_attach,"rb")
    filename=input("Rename the File: ")
    with smtplib.SMTP(smtp_server, port) as server:
        #server=server.smtplib.SMTP(host_Address,port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user_Address,User_Password)
        print("Congratulations!! Connection established!")
        recipent_details=zip(recipent_name,res_email_ids)
        for recipent_name,recipent_mail in recipent_details:
            message=send_personalized_email(user_Address,recipent_mail,extracted_message,subject,file_to_attach,attachment,filename)
            server.send_message(message)
            print("MESSAGE DELIVERED to {} !!".format(recipent_mail))
        server.quit()    

def main():
    directory_base_path=input("Enter the working directory path:")
    ext_contacts_file_name=input("Enter the filename containing recipents list:")
    ext_contacts_file_path=os.path.join(directory_base_path,ext_contacts_file_name)
    ext_message_file_name=input("Enter the filename containing the message :")
    ext_message_file_path=os.path.join(directory_base_path,ext_message_file_name)
    host_Address=input("Enter the smtp server Address:")
    port=int(input("Enter the port number:"))
    user_Address=input("Enter User Email Address:") 
    print("Enter User Password: ")
    User_Password=getpass.getpass()
    set_SMPT_server(host_Address,port,user_Address,User_Password,ext_contacts_file_path,ext_message_file_path)
  

if __name__ == '__main__':
   try:
       main()
       print("THANK YOU. \n")
   except:
        print("Sorry!! Failed to send email!!")



