import almPars
import Galileo
import service
import datetime

cfgParam = service.getCfgParam("config.cfg")

#Reference point
xyz = [0 for _ in range(6)]
xyz[0:3] = cfgParam[0]
xyz[3:] = service.xyz2blh(xyz)

# Elevation mask
elvMask = cfgParam[1]

parser = almPars.GalAlmParser()
res = parser.parse(cfgParam[2])
GalAlms = Galileo.GalAlmanachs()
GalAlms.initByRinex(res)

fid = open("res.txt", "w")
out = ""
hh = 0
mm = 0
for t in range (1439):
    mm += 1
    if mm == 60:
        mm = 0
        hh += 1
    curDateTime = datetime.datetime.today()
    curDateTime = curDateTime.replace(hour = hh, minute = mm, second = 0)
    (wk, sec) = service.utc_to_gps(curDateTime)
    out = str(hh*3600 + mm*60) + ' '
    for idx in range(GalAlms.NGAL):
        if GalAlms.alm[idx].valid == True:
            sat = GalAlms.getPos(idx, sec, wk)
            (azi, elv) = service.svAngles(xyz, sat)
            if elv > 0.0:
                out += str(GalAlms.alm[idx].data['SVID']) + " "
            else:
                out += "nan "
    fid.write(out + "\n")
fid.close()
