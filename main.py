from fastapi import FastAPI, Request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv(override=True)

  
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  
port = 587
smtp_server = os.getenv('MAIL_SERVER')
login = os.getenv('MAIL_USERNAME')
password = os.getenv('MAIL_PASSWORD')
  
sender_email = os.getenv('MAIL_FROM_NAME')
receiver_email = os.getenv('MAIL_FROM_NAME')
message = MIMEMultipart("alternative")
message["Subject"] = "Rendez-vous"
message["From"] = "EMECI"
message["To"] = receiver_email
  
@app.get("/")
def index():
    return {"message": "Hello, World"}
  
@app.post("/send-email")
async def send_email(request: Request):
    try:
        form_data = await request.form()
        name = form_data.get("name")
        tel = form_data.get("tel")
        date = form_data.get("date")
        motif = form_data.get("motif")

        if not name or not tel or not date or not motif:
            return {"success": False, "message": "Please fill in all fields"}

        html = f"""\
            <html>
            <body>
                <h2>Rendez-vous pris par : {name}<h2>
                <p>Contact: {tel}</p>
                <p>Date: {date}</p>
                <p>Motif: {motif}</p>
            </body>
            </html>
            """
        part = MIMEText(html, "html")
        message.attach(part)
    
        server = smtplib.SMTP(smtp_server, port)
        #server.set_debuglevel(1)
        server.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
        server.login(login, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    
        return {"success": True, "message":"send mail"} #uvicorn main:app
    except Exception as e:
        return {"success": False, "message":str(e)} 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)