#ifndef _MESHTOOLS_RAY_H
#define _MESHTOOLS_RAY_H

#include <vector>

#include <geometry/Vector.h>

namespace meshTools
{
namespace Geometry
{
    
    

class Ray
{
public:
    
    Ray(Vector o, Vector d)
        : origin(o), direction(d)
    {
        
    }
    
    Vector origin;
    Vector direction;

    bool  pointPlaneSide(Vector point);
    float pointDistance(Vector point);
    Vector pointProjection(Vector point);
    Vector triangleRayHit(Vector triangle[3]);
	Vector segmentPlaneHit(Vector segment0, Vector segment1);
	Vector intersectRayLine(Vector p1, Vector p2);

};

    
    
}
}


#endif 