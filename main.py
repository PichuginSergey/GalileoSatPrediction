import almPars
import Galileo
import service
import datetime

# Load cfg param. xyz - Reference point [x,y,z,b,l,h]
xyz, elvMask, almGalFile, mode, outFile = service.getCfgParam("config.cfg")

# Get Galileo almanac
parser = almPars.GalAlmParser()
res = parser.parse(almGalFile)
GalAlms = Galileo.GalAlmanachs()
GalAlms.initByRinex(res)

if mode == 'False':
    service.nowTimePredication(GalAlms, xyz, elvMask)
else:
    service.dayPrediction(GalAlms, xyz, outFile, elvMask)
    
