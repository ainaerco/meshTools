
#include <geometry/math.h>
#include <geometry/ray.h>

namespace meshTools {
namespace Geometry {

bool Ray::pointPlaneSide(const Vector &point) const {
    return direction.dot(point - origin) >= 0;
}

float Ray::pointDistance(const Vector &point) const {
    return direction.dot(origin - point);
}

Vector Ray::pointProjection(const Vector &point) const {
    const Vector v = point - origin;
    return point - direction * (v.dot(direction));
}

Vector Ray::triangleRayHit(const Vector triangle[3]) const {
    Vector ret, tvec, qvec;
    const Vector edge1 = triangle[1] - triangle[0];
    const Vector edge2 = triangle[2] - triangle[0];
    const Vector pvec = direction.cross(edge2);
    float u, v, t;
    const float det = edge1.dot(pvec);
    if (det > EPSILON) {
        tvec = origin - triangle[0];
        u = tvec.dot(pvec);
        if ((u < 0) || (u > det)) {
            return ret;
        }
        qvec = tvec.cross(edge1);
        v = direction.dot(qvec);
        if ((v < 0) || (u + v > det)) {
            return ret;
        }
    } else if (det < -EPSILON) {
        tvec = origin - triangle[0];
        u = tvec.dot(pvec);
        if ((u > 0) || (u < det)) {
            return ret;
        }
        qvec = tvec.cross(edge1);
        v = direction.dot(qvec);
        if ((v > 0) || (u + v < det)) {
            return ret;
        }
    } else {
        return ret;
    }
    const float inv_det = 1 / det;
    t = edge2.dot(qvec) * inv_det;
    u = u * inv_det;
    v = v * inv_det;
    return Vector(u, v, t);
}

Vector Ray::segmentPlaneHit(const Vector &segment0,
                            const Vector &segment1) const {
    const float d = direction.dot(origin - segment0);
    const float a = direction.dot(segment1 - segment0);
    if (a == 0.0) {
        return Vector();
    }
    return segment0.lerp(segment1, d / a);
}

Vector Ray::intersectRayLine(const Vector &p1, const Vector &p2) const {
    const Vector zero;
    const Vector v1 = origin - p1;
    const Vector v2 = p2 - p1;
    const Vector v3 = Vector(-direction.y, direction.x, 0.0);
    const float d = v2.dot(v3);
    if (d == 0.0)
        return zero;
    const float t1 = (v2.x * v1.y - v2.y * v1.x) / d;
    const float t2 = v1.dot(v3) / d;
    if (t1 >= 0.0 && t2 >= 0.0 && t2 <= 1.0)
        return origin + t1 * direction;
    return zero;
}

} // namespace Geometry
} // namespace meshTools