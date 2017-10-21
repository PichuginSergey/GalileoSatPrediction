import almPars
import Galileo
import service
import svPrediction

# Load cfg parameters
config = service.getCfgParam("config.cfg")

# Get Galileo almanac
parser = almPars.GalAlmParser()
res = parser.parse(config[2])
GalAlms = Galileo.GalAlmanachs()
GalAlms.initByRinex(res)

# Predict satellites
svPrediction.prediction(GalAlms, config)
