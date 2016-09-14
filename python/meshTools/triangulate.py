from geometry import *
from copy import copy

class Polygon():
    def __init__(self,vertices,polygon,normal):
        self.vertex = vertices
        self.indices = []
        self.vertex_count = len(polygon)
        for i in xrange(self.vertex_count):
            self.indices.append(i)
        self.normal = normal
        self.orig_polygon = copy(polygon)
        self.orig_vertex_count = int(self.vertex_count)

    def triangulateIndices(self):
        triangles=[]
        old_count=self.orig_vertex_count-2
        while self.vertex_count>3 and old_count>0:
            old_count-=1
            i=1
            while i<self.vertex_count-1:
                test = self.convexTest(i)
                #convex
                if test==1:
                    if not self.isAnyPointInside(i):
                        triangles.append([self.indices[i-1],self.indices[i],self.indices[i+1]])
                        self.removeVertex(i)
                #concave
                #elif test==0:pass
                #degenerate
                #elif test==-1:pass
                i+=1
        
        # self.orig_edges=[]
        # self.interior_edges=[]
        # for i in xrange(0,self.orig_vertex_count-1):
        #     self.orig_edges.append([self.orig_polygon[i],self.orig_polygon[i+1]])

        triangles.append(self.indices)
        for i in xrange(len(triangles)):
            triangles[i][0]=self.orig_polygon[triangles[i][0]]
            triangles[i][1]=self.orig_polygon[triangles[i][1]]
            triangles[i][2]=self.orig_polygon[triangles[i][2]]
        #print self.indices
        #print self.triangles
        #for i in xrange(0,len(self.triangles)):
        #    for j in xrange(2):
        #        if not [self.triangles[i][j],self.triangles[i][j+1]] in self.orig_edges:
        #            self.interior_edges.append([self.triangles[i][j],self.triangles[i][j+1]])

        #print self.orig_edges
        #print self.interior_edges
        return triangles
        
    def removeVertex(self,i):
        for j in xrange(i+1,self.vertex_count):
            self.indices[j-1]=self.indices[j]
        self.indices.pop(self.vertex_count-1)
        self.vertex_count-=1

    def isAnyPointInside(self,i):
        for j in xrange(self.vertex_count):
            if i!=j and self.isPointInside(self.vertex[self.indices[j]],self.vertex[self.indices[i+1]]):
                return True
        return False

    def isPointInside(self,point,q):
        pmq = point-q
        ntmp = pmq.cross(self.e1)

        b0 = self.mn.dot(ntmp)
        if b0<=0: return False

        ntmp = self.e0.cross(pmq)

        b1 = self.mn.dot(ntmp)
        if b1<=0: return False
        if self.ma-b0-b1>0: return True
        else: return False

    def convexTest(self,i):
        self.e0 = self.vertex[self.indices[i-1]]-self.vertex[self.indices[i+1]]
        self.e1 = self.vertex[self.indices[i]]-self.vertex[self.indices[i+1]]
        self.mn = self.e0.cross(self.e1)
        self.ma = self.mn.lengthSquared()
        #degenerate
        if -EPSILON<self.ma and self.ma<EPSILON:return-1
        #concave
        if self.mn.dot(self.normal)<0:return 0
        #convex
        else: return 1
