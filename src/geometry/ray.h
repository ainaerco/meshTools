/**
 * @file ray.h
 * @brief Ray class for ray-geometry intersection tests
 */

#ifndef _MESHTOOLS_RAY_H
#define _MESHTOOLS_RAY_H

#include <vector>

#include <geometry/vector.h>

namespace meshTools {
namespace Geometry {

/**
 * @class Ray
 * @brief A ray class for geometric intersection tests
 *
 * This class represents a ray defined by an origin point and a direction
 * vector, providing methods for various geometric intersection and projection
 * calculations.
 */
class Ray {
  public:
    /**
     * @brief Construct a ray from origin and direction
     * @param o Origin point of the ray
     * @param d Direction vector of the ray
     */
    Ray(const Vector &o, const Vector &d) : origin(o), direction(d) {}

    Vector origin;    ///< Origin point of the ray
    Vector direction; ///< Direction vector of the ray

    /**
     * @brief Determine which side of the ray plane a point lies on
     * @param point The point to test
     * @return True if point is on the positive side of the plane, false
     * otherwise
     */
    bool pointPlaneSide(const Vector &point) const;

    /**
     * @brief Calculate the distance from a point to the ray
     * @param point The point to measure distance from
     * @return Distance from the point to the ray
     */
    float pointDistance(const Vector &point) const;

    /**
     * @brief Project a point onto the ray
     * @param point The point to project
     * @return Projected point on the ray
     */
    Vector pointProjection(const Vector &point) const;

    /**
     * @brief Calculate ray-triangle intersection point
     * @param triangle Array of 3 vertices defining the triangle
     * @return Intersection point, or null vector if no intersection
     */
    Vector triangleRayHit(const Vector triangle[3]) const;

    /**
     * @brief Calculate segment-plane intersection point
     * @param segment0 First endpoint of the segment
     * @param segment1 Second endpoint of the segment
     * @return Intersection point, or null vector if no intersection
     */
    Vector segmentPlaneHit(const Vector &segment0,
                           const Vector &segment1) const;

    /**
     * @brief Calculate ray-line intersection point
     * @param p1 First point on the line
     * @param p2 Second point on the line
     * @return Intersection point, or null vector if no intersection
     */
    Vector intersectRayLine(const Vector &p1, const Vector &p2) const;
};

} // namespace Geometry
} // namespace meshTools

#endif