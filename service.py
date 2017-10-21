from math import sin, cos, sqrt, atan, atan2, pi

def xyz2blh(xyz):
    major_radius = 6378137.0
    e = 0.0818191908426E0 ** 2
    ee = float(e)/(1.0 - e)
    b = major_radius * sqrt(1 - e)
    p = sqrt(xyz[0]**2 + xyz[1]**2)
    tetha = atan(float(xyz[2])/(p*sqrt(1 - e)))
    stet = sin(tetha)
    ctet = cos(tetha)
    numerator = xyz[2] + ee*b*stet**3
    denumenat = p - e * major_radius * ctet**3
    lat = atan( float(numerator)/denumenat)
    sinLat = sin(lat)
    N = float(major_radius)/sqrt(1 - e*sinLat**2);
    blh = [lat, atan2(xyz[1], xyz[0]), float(p)/cos(lat)- N]
    return blh

def utc_to_gps(curDateTime):
    doy = ( 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    NUM_DAYS_IN_WEEK = 7
    mounth = curDateTime.month
    ye = curDateTime.year - 1980
    lpdays = ye/4 + 1
    if ( ((ye%4) == 0) and ((mounth) <= 2) ):
        lpdays -= 1
    de = ye*365 + doy[(mounth)-1] + curDateTime.day + lpdays - 6
    wk = de / NUM_DAYS_IN_WEEK
    sec = (de%NUM_DAYS_IN_WEEK)*86400.0 + (curDateTime.hour)*3600.0 + (curDateTime.minute)*60.0 + (curDateTime.second)

    while(sec < 0.0):
        wk -= 1
        sec += 604800.0
    while(sec >= 604800.0):
        wk += 1
        sec -= 604800.0
    sec -= 3 * 3600
    return (wk, sec)

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

def getCfgParam(name):
    xyz = [0, 0, 0]
    name = "config.cfg"
    fid = open(name, "r")
    for i in range(len(xyz)):
        cmd = fid.readline()
        xyz[i] = float(cmd[cmd.find("=")+1:-1])
    cmd = fid.readline()
    elv = float(cmd[cmd.find("=")+1:-1])
    cmd = fid.readline()
    alm = cmd[cmd.find("=")+1:-1]
    cmd = fid.readline()
    dayPrediction = bool(cmd[cmd.find("=")+1:-1])
    fid.close()
    return (xyz, elv, alm, dayPrediction)
