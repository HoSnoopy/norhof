#!/usr/bin/python

import smtplib
import sys
import time
import serial
import datetime;
import os.path

if not os.path.exists('/tmp/mailsent'):
              datei = open("/tmp/mailsent","w")
              datei.write('1234 ')
              datei.close

def sendmail(message):
   to = 'u.popp@gsi.de'
   cc = 'n.petridis@gsi.de'
   gmail_user = 'Email-Server-Login'
   absender = 'Email-Adresse'
   gmail_pwd = 'Email-Server-Passwort'
   smtpserver = smtplib.SMTP("smtp-server",port)
   smtpserver.ehlo()
   smtpserver.starttls()
   smtpserver.ehlo() # extra characters to permit edit
   smtpserver.login(gmail_user, gmail_pwd)
   header = 'To:' + to + '\n' 'From: ' + absender  + '\n' + 'Subject:Kuehlfallenmeldung \n'
   msg = header + '\n' + message + '\n\n'
   smtpserver.sendmail(absender, to, msg)
   smtpserver.sendmail(absender, cc, msg)
   smtpserver.quit()


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
command = 'rm 19' + '\r\n'
ser.write(command)
out = ''
time.sleep(1)
zeit = ''
while ser.inWaiting() > 0:
            out += ser.read(1)

if out != '':
            ausgabe = out[8]+out[9]

if ausgabe == '10':
            meldung = 'Alles ok, Pumpe ist im Standby' 
            datei = open('/tmp/mailsent','w')
            datei.write('standby')
            datei.close

elif ausgabe == '18':
            meldung = 'Alles ok, Pumpe ist im Standby' 
            datei = open('/tmp/mailsent','w')
            datei.write('standby')
            datei.close

elif ausgabe == '20':
            meldung = 'Pumpe ist ausgeschaltet'
            datei = open('/tmp/mailsent','w')
            datei.write('aus')
            datei.close
 
elif ausgabe == '28':
            meldung = 'Pumpe ist ausgeschaltet'
            datei = open('/tmp/mailsent','w')
            datei.write('aus')
            datei.close

elif ausgabe == 'D0' or  ausgabe == 'D8':
            meldung = 'Dewar ist leer!!'
            sentmail = 'keine Mail gesendet'
            f = open("/tmp/mailsent","r")
            sentmail = f.read()
            f.close()
            if not sentmail == 'leer':
              sendmail(meldung)
              datei = open("/tmp/mailsent","w")
              datei.write('leer')

 
elif ausgabe == 'DA' or ausgabe == 'D2':
            meldung = 'Dewar ist fast leer!'
            sentmail = 'keine Mail gesendet'
            f = open('/tmp/mailsent','r')
            sentmail = f.read()
            f.close()
            if not sentmail == 'fastleer':
              sendmail(meldung)
              datei = open('/tmp/mailsent','w')
              datei.write('fastleer')
              datei.close
              
 
elif ausgabe == '16':
            meldung = 'Pumpe pumpt gerade'
            ts=time.time()
            zeit = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
            letztespumpen = 'Es wurde das letzte mal gepumpt: ' + zeit
            datei = open("/var/www/gasjet-data/lastpump.dat","w")
            datei.write(letztespumpen)
            datei.close
            datei = open('/tmp/mailsent','w')
            datei.write('pumpt')
            datei.close
else:
            meldung = 'Unbekannter Status ' + ausgabe
            datei = open('/tmp/mailsent','w')
            datei.write('unbekannt')
            datei.close

#print (meldung)
datei = open("/var/www/gasjet-data/kuehlfallenstatus.dat","w")
datei.write(meldung)
datei.close


