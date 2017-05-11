import datetime

from ia.models import CiaConsecutivo, DocRep

def consecutivo_doc(cia, tipo):
    
    numero = 0
    
    try:

        while True:
            
            ciaconsecutivo = CiaConsecutivo.objects.filter(cia_id__exact=cia, tipo_documento__exact=tipo)
            
            if ciaconsecutivo:
                numero = ciaconsecutivo.numero
                numero =numero + 1
                ciaconsecutivo.numero = numero
                ciaconsecutivo.save()
            else:
                numero = 1
                cc = ciaconsecutivo.objects.create(
                    cia=cia,
                    tipo=tipo,
                    numero=numero                
                )
                cc.save()

            registros = DocRep.objects.filter(cia_id__exact=cia, tipo_documento__exact=tipo, numero__exact=numero).count()

            if registros < 1:
                break
            
        return numero            

    except Exception as e:
        raise e
     
def strToDatetime(strFecha, fmt="%Y-%m-%d %H:%M:%S"):
    try:
        # if fmt is None:
        #     fmt = "%Y-%m-%d %H:%M:%S.%f"
    
        dt = datetime.datetime.strptime(strFecha, fmt)
        return dt
    except Exception as e:
        raise e

def strToBoolean(strValor):
    return strValor.lower() in ("yes", "true", "t", "1")  

def midivision(val1, val2):  
    return val1/val2     