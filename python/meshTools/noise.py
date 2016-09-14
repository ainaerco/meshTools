from math import floor
from noise_tabs import *

TABMASK = 0xFF

def floor2int(val):
    return int(floor(val))

def lerp(t,a,b):
    return a+(b-a)*t

def clamp(val,low,high):
    if val<low: return low
    elif val>high: return high
    else: return val

def imod(a,b):
    n = int(a/float(b))
    a-=n*b
    if a<0:a+=b
    return a


class Noise(object):
    def __init__(self):
        self.xperiod = 1
        self.yperiod = 1
        self.zperiod = 1
        self.tperiod = 1
        self.poffset = 0

    def noise_template(self,func,*args):
        """
        noise template (2D)

        Noise template for a 2D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1 
        """
        if len(args)==2:
            x,y= args[0],args[1]
            ix,iy=floor2int(x),floor2int(y)
            rx0=x-ix
            ry0=y-iy
            rx1=rx0-1
            ry1=ry0-1
            sx=rx0*rx0*(3-2*rx0)
            sy=ry0*ry0*(3-2*ry0)
            
            g = grads2[func(ix,iy)]
            u = g[0]*rx0 + g[1]*ry0
            g = grads2[func(ix+1,iy)]
            v = g[0]*rx1 + g[1]*ry0
            a = lerp(sx,u,v)

            g = grads2[func(ix,iy+1)]
            u = g[0]*rx0 + g[1]*ry1
            g = grads2[func(ix+1,iy+1)]
            v = g[0]*rx1 + g[1]*ry1
            b = lerp(sx,u,v)

            return lerp(sy,a,b)
        """
        noise template (3D)

        Noise template for a 3D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1 
        """
        if len(args)==3:
            x,y,z= args[0],args[1],args[2]
            ix,iy,iz=floor2int(x),floor2int(y),floor2int(z)
            rx0=x-ix
            ry0=y-iy
            rz0=z-iz
            rx1=rx0-1
            ry1=ry0-1
            rz1=rz0-1
            sx=rx0*rx0*(3-2*rx0)
            sy=ry0*ry0*(3-2*ry0)
            sz=rz0*rz0*(3-2*rz0)
            
            g = grads3[func(ix,iy,iz)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz0
            g = grads3[func(ix+1,iy,iz)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz0
            a = lerp(sx,u,v)

            g = grads3[func(ix,iy+1,iz)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz0
            g = grads3[func(ix+1,iy+1,iz)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz0
            b = lerp(sx,u,v)

            c = lerp(sy,a,b)

            g = grads3[func(ix,iy,iz+1)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz1
            g = grads3[func(ix+1,iy,iz+1)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz1
            a = lerp(sx,u,v)

            g = grads3[func(ix,iy+1,iz+1)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz1
            g = grads3[func(ix+1,iy+1,iz+1)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz1
            b = lerp(sx,u,v)

            d = lerp(sy,a,b)

            return lerp(sz,c,d)
        """
        noise template (3D)

        Noise template for a 3D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1 
        """
        if len(args)==4:
            x,y,z,t= args[0],args[1],args[2],args[3]
            ix,iy,iz,it=floor2int(x),floor2int(y),floor2int(z),floor2int(t)
            rx0=x-ix
            ry0=y-iy
            rz0=z-iz
            rt0=t-it
            rx1=rx0-1
            ry1=ry0-1
            rz1=rz0-1
            rt1=rt0-1
            sx=rx0*rx0*(3-2*rx0)
            sy=ry0*ry0*(3-2*ry0)
            sz=rz0*rz0*(3-2*rz0)
            st=rt0*rt0*(3-2*rt0)
            g = grads4[func(ix,iy,iz,it)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz0 + g[3]*rt0
            g = grads4[func(ix+1,iy,iz,it)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz0 + g[3]*rt0
            a = lerp(sx,u,v)

            g = grads4[func(ix,iy+1,iz,it)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz0 + g[3]*rt0
            g = grads4[func(ix+1,iy+1,iz,it)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz0 + g[3]*rt0
            b = lerp(sx,u,v)

            c = lerp(sy,a,b)

            g = grads4[func(ix,iy,iz+1,it)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz1 + g[3]*rt0
            g = grads4[func(ix+1,iy,iz+1,it)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz1 + g[3]*rt0
            a = lerp(sx,u,v)

            g = grads4[func(ix,iy+1,iz+1,it)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz1 + g[3]*rt0
            g = grads4[func(ix+1,iy+1,iz+1,it)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz1 + g[3]*rt0
            b = lerp(sx,u,v)

            d = lerp(sy,a,b)

            e = lerp(sz,c,d)

            g = grads4[func(ix,iy,iz,it+1)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz0 + g[3]*rt1
            g = grads4[func(ix+1,iy,iz,it+1)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz0 + g[3]*rt1
            a = lerp(sx,u,v)

            g = grads4[func(ix,iy+1,iz,it+1)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz0 + g[3]*rt1
            g = grads4[func(ix+1,iy+1,iz,it+1)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz0 + g[3]*rt1
            b = lerp(sx,u,v)

            c = lerp(sy,a,b)

            g = grads4[func(ix,iy,iz+1,it+1)]
            u = g[0]*rx0 + g[1]*ry0 + g[2]*rz1 + g[3]*rt1
            g = grads4[func(ix+1,iy,iz+1,it+1)]
            v = g[0]*rx1 + g[1]*ry0 + g[2]*rz1 + g[3]*rt1
            a = lerp(sx,u,v)

            g = grads4[func(ix,iy+1,iz+1,it+1)]
            u = g[0]*rx0 + g[1]*ry1 + g[2]*rz1 + g[3]*rt1
            g = grads4[func(ix+1,iy+1,iz+1,it+1)]
            v = g[0]*rx1 + g[1]*ry1 + g[2]*rz1 + g[3]*rt1
            b = lerp(sx,u,v)

            d = lerp(sy,a,b)

            f = lerp(sz,c,d)

            return lerp(st,e,f)

    def tabindex2(self,ix,iy):
        return perm[(ix + perm[iy&TABMASK])&TABMASK]

    def tabindex3(self,ix,iy,iz):
        return perm[(ix + perm[(iy + perm[iz&TABMASK])&TABMASK])&TABMASK]

    def tabindex4(self,ix,iy,iz,it):
        return perm[(it + perm[(ix + perm[(iy + perm[iz&TABMASK])&TABMASK])&TABMASK])&TABMASK]


    def snoise(self,*args):
        # Returns a value between -1 and 1
        if len(args)==1:
            x,y,z= args[0].x,args[0].y,args[0].z
            return self.noise_template(self.tabindex3,x,y,z)
        if len(args)==2:
            x,y= args[0],args[1]
            return self.noise_template(self.tabindex2,x,y)
        if len(args)==3:
            x,y,z= args[0],args[1],args[2]
            return self.noise_template(self.tabindex3,x,y,z)
        if len(args)==4:
            x,y,z,t= args[0],args[1],args[2],args[3]
            return self.noise_template(self.tabindex4,x,y,z,t)

    def fBm(self,x,y,z,octaves,lacunarity,gain):
        res = 0
        amp = 1
        for i in xrange(octaves):
            res += amp*self.snoise(x,y,z)
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        return 0.5*(res+1.0)

    def vfBm(self,x,y,z,octaves,lacunarity,gain):
        amp = 1
        ox,oy,oz=0.0,0.0,0.0

        for i in xrange(octaves):
            v = self.vsnoise(x,y,z)
            ox += amp*v[0]
            oy += amp*v[1]
            oz += amp*v[2]
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        #ox = 0.5*(ox+1.0)
        #oy = 0.5*(oy+1.0)
        #oz = 0.5*(oz+1.0)
        return [ox,oy,oz]

    def turbulence(self,x,y,z,octaves,lacunarity,gain):
        res = 0
        amp = 1
        for i in xrange(octaves):
            res += amp*abs(self.snoise(x,y,z))
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        return 0.5*(res+1.0)

    def vturbulence(self,x,y,z,octaves,lacunarity,gain):
        amp=1.0
        ox=0.0;
        oy=0.0;
        oz=0.0;

        for i in xrange(octaves):
            v = self.vsnoise(x,y,z)
            ox += amp*abs(v[0])
            oy += amp*abs(v[1])
            oz += amp*abs(v[2])
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        #ox = 0.5*(ox+1.0)
        #oy = 0.5*(oy+1.0)
        #oz = 0.5*(oz+1.0)
        return [ox,oy,oz]

    def vsnoise(self,*args):
        if len(args)==1:
            x,y,z= args[0].x,args[0].y,args[0].z
            ox = self.noise_template(self.tabindex3,x,y,z)
            x += 10
            oy = self.noise_template(self.tabindex3,x,y,z)
            y += 10
            oz = self.noise_template(self.tabindex3,x,y,z)
            return [ox,oy,oz]
        if len(args)==2:
            x,y= args[0],args[1]
            ox = self.noise_template(self.tabindex2,x,y)
            x += 10
            oy = self.noise_template(self.tabindex2,x,y)
            return ox,oy
        if len(args)==3:
            x,y,z= args[0],args[1],args[2]
            ox = self.noise_template(self.tabindex3,x,y,z)
            x += 10
            oy = self.noise_template(self.tabindex3,x,y,z)
            y += 10
            oz = self.noise_template(self.tabindex3,x,y,z)
            return [ox,oy,oz]
        if len(args)==4:
            x,y,z,t= args[0],args[1],args[2],args[3]
            ox = self.noise_template(self.tabindex4,x,y,z,t)
            x += 10
            oy = self.noise_template(self.tabindex4,x,y,z,t)
            y += 10
            oz = self.noise_template(self.tabindex4,x,y,z,t)
            z += 10
            ot = self.noise_template(self.tabindex4,x,y,z,t)
            return [ox,oy,oz,ot]


if __name__=="__main__":
    n = Noise()
    print(n.snoise(0.2,0.2,0.1,0.8))
