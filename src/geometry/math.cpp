/**
 * @file math.cpp
 * @brief Implementation of mathematical utility functions
 */

#include <cmath>
#include <geometry/math.h>
#include <iostream>

namespace meshTools {

namespace Geometry {

namespace math {

meshTools::Geometry::Vector getBarycentric(const Vector &p, const Vector &a,
                                           const Vector &b, const Vector &c) {
    const Vector v0 = b - a;
    const Vector v1 = c - a;
    const Vector v2 = p - a;
    const float d00 = v0.dot(v0);
    const float d01 = v0.dot(v1);
    const float d11 = v1.dot(v1);
    const float d20 = v2.dot(v0);
    const float d21 = v2.dot(v1);
    const float denom = 1.0f / (d00 * d11 - d01 * d01);
    const float v = (d11 * d20 - d01 * d21) * denom;
    const float w = (d00 * d21 - d01 * d20) * denom;
    const float u = 1.0f - v - w;
    return Vector(u, v, w);
}

bool pointInPoly(const Vector &point, const std::vector<Vector> &poly) {
    bool result = false;
    const size_t &polyCount = poly.size();
    size_t j = polyCount - 1;
    for (size_t i = 0; i < polyCount; ++i) {
        if (((poly[i].y >= point.y) != (poly[j].y >= point.y)) &&
            (point.x <= (poly[j].x - poly[i].x) * (point.y - poly[i].y) /
                                (poly[j].y - poly[i].y) +
                            poly[i].x)) {
            result = !result;
        }
        j = i;
    }
    return result;
}

bool epsilonTest(float value, float test, float eps) {
    return (value - eps <= test) && (test <= value + eps);
}

float lerp(float t, float a, float b) { return (a + (b - a) * t); }

float fit(float p, float oldmin, float oldmax, float newmin, float newmax) {
    return lerp((p - oldmin) / (oldmax - oldmin), newmin, newmax);
}

float max(float a, float b) { return (a < b) ? b : a; }

float min(float a, float b) { return (a < b) ? a : b; }

float interpolateBezier(float t, float p0, float p1, float p2, float p3) {
    const float u = 1 - t;
    const float tt = t * t;
    const float ttt = tt * t;
    const float uu = u * u;
    const float uuu = uu * u;
    return uuu * p0 + 3 * uu * t * p1 + 3 * u * tt * p2 + ttt * p3;
}

float interpolateCatmullRom(float t, float p0, float p1, float p2, float p3) {
    const float tt = t * t;
    return 0.5f *
           (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * tt +
            (-p0 + 3 * p1 - 3 * p2 + p3) * tt * t);
}

Vector solveCubic(float a, float b, float c, float d) {
    const float o3 = 1 / 3.0f;
    const float b2 = b * b;
    const float a2 = a * a;
    const float f = c / a - b2 * o3 / a2;
    const float g =
        (2 * b2 * b / (a2 * a) - 9 * b * c / a2 + 27 * d / a) / 27.0f;
    const float g2 = g * g;
    const float h = g2 * 0.25f + f * f * f / 27.0f;
    if ((f == 0) && (g == 0) && (h == 0)) {
        const float x = pow(-(d / a), o3);
        return Vector(x, x, x);
    } else if (h <= 0) {
        const float i = sqrt(g2 * 0.25f - h);
        const float j = pow(i, o3);
        const float kd3 = acos(-g * 0.5f / i) * o3;
        const float m = cos(kd3);
        const float n = sqrt(3.0f) * sin(kd3);
        const float p = -b * o3 / a;
        return Vector(2 * j * m + p, -j * (m + n) + p, -j * (m - n) + p);
    }
    return Vector();
}

} // namespace math
} // namespace Geometry
} // namespace meshTools