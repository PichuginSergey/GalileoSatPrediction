import almPars
import math
import service
import datetime

NUMGAL = 30

class GalAlm():
    def __init__(self):
        self.data = {name : 0 for name in almPars.TAGS}
        self.valid = False

class GalAlmanachs():
    def __init__(self):
        self.NUMGAL = 30
        self.alm = [GalAlm() for _ in range(NUMGAL)]
        
    def initByRinex(self, data):
        # calc wna
        issueDate = data[0]
        curDateTime = datetime.datetime.today()
        issueDate = issueDate.split("-")
        curDateTime = curDateTime.replace(year = int(issueDate[0]), month = int(issueDate[1]), day = int(issueDate[2][0:2]))
        (wna, _) = service.utc_to_gps(curDateTime)
        
        data = data[1]
        num = len(data[almPars.TAGS[0]])
        for idx in range(num):
            for elm in data:
                self.alm[idx].data[elm] = float(data[elm][idx])
            self.alm[idx].valid = True
            
            self.alm[idx].data['deltai'] *= math.pi
            self.alm[idx].data['omega0'] *= math.pi
            self.alm[idx].data['omegaDot'] *= math.pi
            self.alm[idx].data['w'] *= math.pi
            self.alm[idx].data['m0'] *= math.pi
            self.alm[idx].data['wna'] = wna

    
    def getPos(self, idx, sec, wk):
        
        SECONDS_A_WEEK = 604800
        GRAV_CONSTANT_GPS = 3.986005E14
        WGS84_OE = 7.2921151467E-5;

        toa = self.alm[idx].data['t0a']
        wna = self.alm[idx].data['wna']
        e = self.alm[idx].data['ecc']
        a = 29600 * 1000 + self.alm[idx].data['aSqRoot']**2
        dwk = wk-wna
        Tk = (dwk)*SECONDS_A_WEEK + sec - toa
        n0 = math.sqrt((GRAV_CONSTANT_GPS/(a*a*a)))
        Mk = self.alm[idx].data['m0'] + n0*Tk

        Eprev = Mk + e * math.sin(Mk)
        Ek = Mk + e * math.sin(Eprev)
        zic = 0
        while ((abs((Ek - Eprev)) > 1e-13) and zic < 10):
            Eprev = Ek;
            Ek = Mk + e * math.sin(Eprev);
            zic += 1
        cek = math.cos(Ek)
        sek = math.sin(Ek)
        denom = 1-e*cek
        svk = (math.sqrt((1 - e*e))*sek )/denom
        cvk = (cek - e)/denom
        Vk = math.atan2(svk, cvk)

        if (Vk < 0.0):
            Vk = Vk + 2.0 * math.pi

        Fk = Vk + self.alm[idx].data['w']
        Uk = Fk
        Rk = denom * a
        Ik = 0.942477796076938 + self.alm[idx].data['deltai']
	
        cuk = math.cos(Uk)
        suk = math.sin(Uk)

        xpk = Rk*cuk
        ypk = Rk*suk

        omega0 = self.alm[idx].data['omega0']
        omegadot = self.alm[idx].data['omegaDot']
        omega_k  = omega0 + Tk*(omegadot - WGS84_OE) - WGS84_OE * toa

        sik = math.sin(Ik)
        cik = math.cos(Ik)
        sok = math.sin(omega_k)
        cok = math.cos(omega_k)

        sat = [0.0, 0.0, 0.0]
        sat[0] = xpk*cok - ypk*cik*sok
        sat[1] = xpk*sok + ypk*cik*cok
        sat[2] = ypk*sik
        return sat
    
class Angles():
    def __init__(self):
        self.azm = 0
        self.elv = 0
        self.valid = False

class GalAngles():
    def __init__(self):
        self.alm = [Angles() for _ in range(NUMGAL)]
