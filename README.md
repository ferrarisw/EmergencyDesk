# EmergencyDesk!
**EmergencyDesk** è un sistema che implementa le funzionalità di Computer Aided Dispatch (CAD) per missioni di soccorso in caso di emergenza. Si pone l'obiettivo di essere a tutti gli effetti un software da Centrale Operativa.

Questo sistema è ancora incompleto ed è nato per finalità di studio. Verrà quindi mantenuto in maniera sporadica.
# Environment
Il sistema pubblicato in questa repository implementa il backend che gestisce l'interfacciamento con il Database. I comandi riportati di seguito sono pensati per un ambiente Linux.

I requisiti per poterlo eseguire sono:

 - Python 3+ (il virtual environment presente è basato su Python 3.7)
 - Tutti i moduli Python presenti nel file `requirements.txt`

## Installazione di Python
Per installare Python, eseguire `sudo apt-get install python3.7 python3-pip` e, per installare i moduli necessari, invocare successivamente `sudo pip3 install -r requirements.txt`
Nel caso si scelga di utilizzare il virtualenvironment presente, semplicemente attivarlo con il comando `source venv/bin/activate`
