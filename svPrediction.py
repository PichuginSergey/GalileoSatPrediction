from math import sin, cos, sqrt, atan, atan2, pi
import Galileo
import datetime
import service

def svAngles(xyz, sat):
    dneu = [0, 0, 0]
    dxyz = [0, 0, 0]
    T = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        dxyz[i] = sat[i] - xyz[i] 
        
    clat = cos(xyz[3])
    slat = sin(xyz[3])
    clon = cos(xyz[4])
    slon = sin(xyz[4])

    T[0] = [-slat*clon,	-slat*slon, clat]
    T[1] = [-slon,  clon, 0]
    T[2] = [clat*clon,	clat*slon, slat]

    for i in range(3):
        dneu[i] = T[i][0] * dxyz[0] + T[i][1] * dxyz[1] + T[i][2] * dxyz[2]

    tmp =  sqrt(dneu[0]**2 + dneu[1]**2)
    elv = atan2(dneu[2], tmp)
    azi = atan2(dneu[1], dneu[0])
    if (azi<0):
        azi += 2*pi;
    return (azi, elv)

def angelsPrediction(curDateTime, galAlm, xyz):
    ang = Galileo.GalAngles()
    (wk, sec) = service.utc_to_gps(curDateTime)
    for idx in range(Galileo.NUMGAL):
        if galAlm.alm[idx].valid == True:
            sat = galAlm.getPos(idx, sec, wk)
            ang.alm[idx].azi, ang.alm[idx].elv = svAngles(xyz, sat)
            ang.alm[idx].valid = True
    return ang

    
def dayPrediction(galAlm, xyz, outFile, elvMask):

    MINUIES_IN_DAY = 1439
    MINUIES_IN_HOUR = 60
    STEP = 1
    
    fid = open(outFile, "w")
    out = ""
    hh = 0
    mm = 0
    for t in range (MINUIES_IN_DAY):
        mm += STEP
        if mm == MINUIES_IN_HOUR:
            mm = 0
            hh += STEP
        curDateTime = datetime.datetime.today()
        curDateTime = curDateTime.replace(hour = hh, minute = mm, second = 0)
        ang = angelsPrediction(curDateTime, galAlm, xyz)
        out = str(hh*MINUIES_IN_HOUR + mm) + ' '
        for idx in range(Galileo.NUMGAL):
            if ang.alm[idx].valid == True and ang.alm[idx].elv*180.0/pi > elvMask:
                out += str(galAlm.alm[idx].data['SVID']) + " "
            else:
                out += "nan "      
        fid.write(out + "\n")
    fid.close()
    print('Done')    

def nowTimePrediction(galAlm, xyz, elvMask):
    
    curDateTime = datetime.datetime.today()
    ang = angelsPrediction(curDateTime, galAlm, xyz)
    for idx in range(Galileo.NUMGAL):
        if ang.alm[idx].valid == True and ang.alm[idx].elv*180.0/pi > elvMask:
            print (galAlm.alm[idx].data["SVID"], ang.alm[idx].azi*180.0/pi, ang.alm[idx].elv*180.0/pi)

# xyz, elvMask, almGalFile, mode, outFile
def prediction(GalAlms, config):
    xyz =  config[0]
    elvMask = config[1]
    mode = config[3]
    outFile = config[4]
    if mode == 'Off':
        nowTimePrediction(GalAlms, xyz, elvMask)
    else:
        dayPrediction(GalAlms, xyz, outFile, elvMask)
