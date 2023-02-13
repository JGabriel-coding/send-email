from playwright.sync_api import sync_playwright,Playwright,expect
import smtplib,os
import email
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders


sites = ["http://localhost"]





def run(playwright:Playwright)-> None:
    contador = 0
    for ip in sites:
        contador += 1
        print(contador)
        navegador = playwright.chromium.launch(headless=False)#Abre o navegador do bot
        contexto = navegador.new_context()#Começa um novo navegador
        pagina=contexto.new_page()

        pagina.goto(ip)
        pagina.wait_for_timeout(1000)#esperando a pagina carregar
        pagina.fill("#LogBox",'initpass')
        pagina.locator("#LogBox").press("Enter")
        pagina.wait_for_timeout(3000)
        pagina.get_by_role("link", name="Maintenance Information").click()
        pagina.wait_for_timeout(3000)
        pagina.emulate_media(media="screen")
        pagina.wait_for_timeout(3000)
        pagina.pdf(path=f"contador00{contador}.pdf")
        
        contexto.close()
        navegador.close()


with sync_playwright() as playwright:
    run(playwright)


server = smtplib.SMTP_SSL('smtp.hostinger.com',465)



from_address = 'youremail@exemplo.com'
to_address = 'destinationemail@exemplo.com'
assunto = 'submit'


body = 'Bom dia!\n\nAqui o Body do email a ser enviado.\n\nAtenciosamente\n'

msg = MIMEMultipart()
msg['Subject']=assunto
msg['From']=from_address
msg['To']=to_address

msg.attach(MIMEText(body))

pdf_files = [f for f in os.listdir(r"Caminho dos pdfs dentro das pastas") if f.endswith('.pdf')]
for pdf_file in pdf_files:
    with open(pdf_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((f).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={pdf_file}')
        msg.attach(part)

server.login(msg['From'],'senha (password)')

server.sendmail(msg['From'],msg['To'],msg.as_string())

server.quit()
