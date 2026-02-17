#ifndef _MESHTOOLS_RAY_H
#define _MESHTOOLS_RAY_H

#include <vector>

#include <geometry/vector.h>

namespace meshTools {
namespace Geometry {

class Ray {
  public:
    Ray(const Vector &o, const Vector &d) : origin(o), direction(d) {}

    Vector origin;
    Vector direction;

    bool pointPlaneSide(const Vector &point) const;
    float pointDistance(const Vector &point) const;
    Vector pointProjection(const Vector &point) const;
    Vector triangleRayHit(const Vector triangle[3]) const;
    Vector segmentPlaneHit(const Vector &segment0,
                           const Vector &segment1) const;
    Vector intersectRayLine(const Vector &p1, const Vector &p2) const;
};

} // namespace Geometry
} // namespace meshTools

#endif