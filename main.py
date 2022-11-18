import streamlit as st
from bs4 import BeautifulSoup
import requests
import smtplib
import ssl
import datetime as dt
import datetime as date



#FUNCTION DEFINITIONS
def transform_link(date):
    link = "https://www.gkgsca.com/2022/11/the-hindu-pdf-" + date + "-free.html#AT-downloadPop"
    #https://www.gkgsca.com/2022/11/the-hindu-pdf-18-november-2022-free.html#AT-downloadPop
    return link

def scrape(URL):
    URL = link
    #defining headers
    header ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

    #getting page using requests module
    page = requests.get(URL, headers=header)

    #getting html content with proper formatting using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    return soup

def send_mail():
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = gmail_id
        receiver_email = mailing_list
        password = gmail_pass      
        FROM = f"Adhiraj's Bot"
        SUBJECT = f"{fd} : The Hindu Newspaper PDF"
        TEXT = f"""
Hey User,

Please check the below link for The Hindu Newspaper for {fd}.

{gdrive_link}

Prepare Well and Have a nice day.

Regards,
Adhiraj's Bot"""
        
        message = 'From: {}\nSubject: {}\n\n{}'.format(FROM,SUBJECT, TEXT)
        

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

def send_discord_message():
    discord_webhook_url = webhook_url
    Message = {
        "content": f"Google Drive Link for The Hindu Newspaper for {fd} : \n{gdrive_link}"
    }
    requests.post(discord_webhook_url, data=Message)



#INTERFACE
st.markdown(
'''
# Newspaper Bot

⚠️ _If you want today's newspaper try to use this app after 11:00 AM IST for proper working_
 
Features of this application:

* Get the link of The Hindu Newspaper for the today's or yesterday's date.
* Get the pdf through email
* Get the pdf through discord
* Add new email in mailing list

'''
)

#code to hide the hamburger menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

mailid = st.text_input("Enter email ID (leave empty if you are in discord channel)")

column1, column2 = st.columns(2)


column1.subheader("Select Date")

today = column1.checkbox("Today's Newspaper")

yesterday = column1.checkbox("Yesterday's Newspaper")   


column2.subheader("Select Medium")

mail = column2.checkbox("Mail")

discord = column2.checkbox("Discord")



#MAIN CODE
if column1.button("Submit"):
    if mail == 0 and discord == 0:
        st.error("Please select atleast one medium")
    elif today == 0 and yesterday == 0:
        st.error("Please select atleast one date")
    elif today == 1 and yesterday == 1:
        st.error("Please select only one date")
    else:
        
        #getting data from env variables
        webhook_url = st.secrets["webhook_url"]
        gmail_id = st.secrets["gmail_id"]
        gmail_pass = st.secrets["gmail_pass"]
        mailing_list = st.secrets["mailing_list"]

        if mailid != "":
            mailing_list.append(mailid)

        #get today's date in two formats (date = 10-october-2022 and fdate = 10-10-2022)
        date1 = date.date.today().strftime("%d-%B-%Y").lower()
        fdate1 = dt.date.today().strftime("%d-%m-%Y")

        #get the month and year from the date
        month = dt.date.today().strftime("%d-%m-%Y")[3:5]
        year = dt.date.today().strftime("%d-%m-%Y")[6:10]


        #get yesterday's date in two formats (date = 10-october-2022 and fdate = 10-10-2022)

        if yesterday:
            date2 = str(int(date1[:2]) - 1) + date1[2:]
            fdate2 = str(int(fdate1[:2]) - 1) + fdate1[2:]
            d = date2
            fd = fdate2
        
        else:
            d = date1
            fd = fdate1
        
        #transform link for today's date
        link = transform_link(d)

        #scrape the page
        a = (scrape(link))
        

        #find the download link
        gdrive_link = a.find("a", class_="button").get('href')

        if mail and discord:
            send_mail()
            send_discord_message()
            st.success("Mail and Discord Message sent")
        
        elif mail:
            send_mail()
            st.success("Mail sent")
        
        elif discord:
            send_discord_message()
            st.success("Discord Message sent")
