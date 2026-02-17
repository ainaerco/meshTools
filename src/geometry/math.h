#ifndef _MESHTOOLS_MATH_H
#define _MESHTOOLS_MATH_H

#include <geometry/vector.h>

#define EPSILON 0.00001

namespace meshTools {
namespace Geometry {
namespace math {

bool epsilonTest(float value, float test = 0, float eps = 0.000001);
float lerp(float t, float a, float b);
float max(float a, float b);
float min(float a, float b);
float fit(float p, float oldmin, float oldmax, float newmin, float newmax);
Vector solveCubic(float a, float b, float c, float d);
bool pointInPoly(const Vector &point, std::vector<Vector> poly);
float interpolateBezier(float t, float p0, float p1, float p2, float p3);
float interpolateCatmullRom(float t, float p0, float p1, float p2, float p3);
Vector getBarycentric(const Vector &p, const Vector &a, const Vector &b,
                      const Vector &c);
} // namespace math
} // namespace Geometry
} // namespace meshTools

#endif