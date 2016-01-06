import beyonic
from rapidsms_httprouter.models import Message, Connection
from ntds.models import Reporter
beyonic.api_key = '06709efd86fcd74fdec580fc5aac2c238bbc4cd3'
nos=["256756238704",
"256775246253",
"256756740680",
"256774084316",
"256789620021",
"256794260969",
"256774075116",
"256783186814",
"256777977055",
"256771011187",
"256756158749",
"256774077988",
"256785994363",
"256777289866",
"256775793210",
"256787150952",
"256789870003",
"256771467373",
"256778208433",
"256771469022",
"256750341391",
"256775790447",
"256750790984",
"256783613564",
"256786502123",
"256783776302",
"256785506682",
"256753946450",
"256772838329",
"256781471952"]
text="Dear parish supervisors, we have sent you airtime to send in your reports.Shortcode is 6969.Please put ntd before each message e.g ntd lf.5.5.5.5.6.6.7.4"
reporters=Reporter.objects.filter(connection__identity__in=nos)
for rep in reporters:
    connection=rep.connection_set.all()[0]
    mobile =  "+"+connection.identity
    kwargs = {'metadata.name': rep.name, 'metadata.parish': rep.parish_name}
    Message.objects.create(connection=connection,direction="O",status="Q",text=text)
    beyonic.Payment.create(phonenumber=mobile,amount='3000', currency='UGX',payment_type='airtime',description='RTI-Envision Airtime money for reporting on NTDs', **kwargs)

