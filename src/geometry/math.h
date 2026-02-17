/**
 * @file math.h
 * @brief Mathematical utility functions for geometric calculations
 */

#ifndef _MESHTOOLS_MATH_H
#define _MESHTOOLS_MATH_H

#include <geometry/vector.h>

#define EPSILON 0.00001 ///< Small epsilon value for floating-point comparisons

namespace meshTools {
namespace Geometry {
/**
 * @namespace meshTools::Geometry::math
 * @brief Mathematical utility functions
 */
namespace math {

/**
 * @brief Test if a value is within epsilon of another value
 * @param value The value to test
 * @param test The value to compare against (default 0)
 * @param eps The epsilon tolerance (default 0.000001)
 * @return True if the difference is within epsilon, false otherwise
 */
bool epsilonTest(float value, float test = 0, float eps = 0.000001);

/**
 * @brief Linear interpolation between two values
 * @param t Interpolation factor (0.0 to 1.0)
 * @param a Start value
 * @param b End value
 * @return Interpolated value
 */
float lerp(float t, float a, float b);

/**
 * @brief Remap a value from one range to another
 * @param p Value to remap
 * @param oldmin Minimum of old range
 * @param oldmax Maximum of old range
 * @param newmin Minimum of new range
 * @param newmax Maximum of new range
 * @return Remapped value
 */
float fit(float p, float oldmin, float oldmax, float newmin, float newmax);

/**
 * @brief Solve a cubic equation ax^3 + bx^2 + cx + d = 0
 * @param a Coefficient of x^3
 * @param b Coefficient of x^2
 * @param c Coefficient of x
 * @param d Constant term
 * @return Vector containing the three roots
 */
Vector solveCubic(float a, float b, float c, float d);

/**
 * @brief Test if a point is inside a polygon
 * @param point The point to test
 * @param poly Vector of vertices defining the polygon
 * @return True if point is inside the polygon, false otherwise
 */
bool pointInPoly(const Vector &point, const std::vector<Vector> &poly);

/**
 * @brief Interpolate using cubic Bezier curve
 * @param t Interpolation parameter (0.0 to 1.0)
 * @param p0 First control point
 * @param p1 Second control point
 * @param p2 Third control point
 * @param p3 Fourth control point
 * @return Interpolated value
 */
float interpolateBezier(float t, float p0, float p1, float p2, float p3);

/**
 * @brief Interpolate using Catmull-Rom spline
 * @param t Interpolation parameter (0.0 to 1.0)
 * @param p0 First control point
 * @param p1 Second control point
 * @param p2 Third control point
 * @param p3 Fourth control point
 * @return Interpolated value
 */
float interpolateCatmullRom(float t, float p0, float p1, float p2, float p3);

/**
 * @brief Calculate barycentric coordinates of a point relative to a triangle
 * @param p The point to calculate coordinates for
 * @param a First vertex of the triangle
 * @param b Second vertex of the triangle
 * @param c Third vertex of the triangle
 * @return Barycentric coordinates as a vector
 */
Vector getBarycentric(const Vector &p, const Vector &a, const Vector &b,
                      const Vector &c);
} // namespace math
} // namespace Geometry
} // namespace meshTools

#endif