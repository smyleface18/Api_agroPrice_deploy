from email.message import EmailMessage;
import ssl;
import smtplib;

def alert_email(receptor,text):

    email_emisor ='cacosta@itilpn.edu.co';
    email_receptor = receptor;
    email_password = 'quga avee ajor eprs';

    asunto = text;
    cuerpo = ' ';

    em = EmailMessage();
    em['From'] = email_emisor;
    em['To'] = email_receptor;
    em['Subject'] = asunto;
    em.set_content(cuerpo);

    contexto = ssl.create_default_context();
        
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465, context = contexto) as smtp:
        smtp.login(email_emisor,email_password);
        smtp.sendmail(email_emisor,email_receptor, em.as_string())

