/**
 * @file transform.cpp
 * @brief Implementation of 4x4 transformation matrix operations
 */

#include <geometry/math.h>
#include <geometry/transform.h>
#include <geometry/vector.h>

#include <cmath>
#include <sstream>

namespace meshTools {
namespace Geometry {

Transform::Transform(const Vector &v1, const Vector &v2, const Vector &v3) {
    m[0][0] = v1.x;
    m[0][1] = v1.y;
    m[0][2] = v1.z;
    m[0][3] = 0;
    m[1][0] = v2.x;
    m[1][1] = v2.y;
    m[1][2] = v2.z;
    m[1][3] = 0;
    m[2][0] = v3.x;
    m[2][1] = v3.y;
    m[2][2] = v3.z;
    m[2][3] = 0;
    m[3][0] = 0;
    m[3][1] = 0;
    m[3][2] = 0;
    m[3][3] = 1;
}

Transform::Transform(const Vector &v1, const Vector &v4) {
    Vector v2 = v4;
    v2 = v2.cross(v1).normalize();
    Vector v3 = v1;
    v3 = v3.cross(v2).normalize();
    m[0][0] = v1.x;
    m[0][1] = v1.y;
    m[0][2] = v1.z;
    m[0][3] = 0;
    m[1][0] = v2.x;
    m[1][1] = v2.y;
    m[1][2] = v2.z;
    m[1][3] = 0;
    m[2][0] = v3.x;
    m[2][1] = v3.y;
    m[2][2] = v3.z;
    m[2][3] = 0;
    m[3][0] = 0;
    m[3][1] = 0;
    m[3][2] = 0;
    m[3][3] = 1;
}

std::string Transform::toString() const {
    std::stringstream ss;
    ss << "[" << m[0][0] << "," << m[0][1] << "," << m[0][2] << "," << m[0][3]
       << "]" << "\n";
    ss << "[" << m[1][0] << "," << m[1][1] << "," << m[1][2] << "," << m[1][3]
       << "]" << "\n";
    ss << "[" << m[2][0] << "," << m[2][1] << "," << m[2][2] << "," << m[2][3]
       << "]" << "\n";
    ss << "[" << m[3][0] << "," << m[3][1] << "," << m[3][2] << "," << m[3][3]
       << "]" << "\n";
    return ss.str();
}

Transform Transform::lookAt(const Vector &pos, const Vector &look,
                            const Vector &up) const {
    Transform t;
    const Vector dir = look - pos;
    const Vector left = dir.cross(up).normalize();
    const Vector newup = dir.cross(left).normalize();
    t.m[0][0] = left.x;
    t.m[0][1] = newup.x;
    t.m[0][2] = dir.x;
    t.m[0][3] = pos.x;
    t.m[1][0] = left.y;
    t.m[1][1] = newup.y;
    t.m[1][2] = dir.y;
    t.m[1][3] = pos.y;
    t.m[2][0] = left.z;
    t.m[2][1] = newup.z;
    t.m[2][2] = dir.z;
    t.m[2][3] = pos.z;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

float subdet(const float m[4][4], int i, int j) {
    float r[9];
    int cur = 0;
    for (int k = 0; k < 4; ++k) {
        if (k == i)
            continue;
        for (int l = 0; l < 4; ++l) {
            if (l == j)
                continue;
            r[cur] = m[k][l];
            cur++;
        }
    }
    return r[0] * r[4] * r[8] + r[1] * r[5] * r[6] + r[2] * r[3] * r[7] -
           r[6] * r[4] * r[2] - r[7] * r[5] * r[0] - r[8] * r[3] * r[1];
}

Transform Transform::identity() const {
    Transform t;
    t.m[0][0] = t.m[1][1] = t.m[2][2] = t.m[3][3] = 1.0f;
    t.m[0][1] = t.m[0][2] = t.m[0][3] = t.m[1][0] = t.m[1][2] = t.m[1][3] =
        t.m[2][0] = t.m[2][1] = t.m[2][3] = t.m[3][0] = t.m[3][1] = t.m[3][2] =
            0.0f;
    return t;
}

Transform Transform::invert() const {
    Transform t;
    float det = determinant();

    if (math::epsilonTest(det)) {
        memcpy(&t.m, &m, sizeof(m));
    } else {

        det = 1 / det;
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++) {
                const float sign = 1.0f - ((i + j) % 2) * 2.0f;
                const float d = subdet(m, i, j);
                t.m[i][j] = d * det * sign;
            }
    }
    return t;
}

Transform Transform::translate(const float &x, const float &y,
                               const float &z) const {
    Transform t;
    t.m[0][0] = 1;
    t.m[0][1] = 0;
    t.m[0][2] = 0;
    t.m[0][3] = x;
    t.m[1][0] = 0;
    t.m[1][1] = 1;
    t.m[1][2] = 0;
    t.m[1][3] = y;
    t.m[2][0] = 0;
    t.m[2][1] = 0;
    t.m[2][2] = 1;
    t.m[2][3] = z;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

Transform Transform::translate(const Vector &v) const {
    return translate(v.x, v.y, v.z);
}

Transform Transform::scale(const float &x, const float &y,
                           const float &z) const {
    Transform t;
    t.m[0][0] = x;
    t.m[0][1] = 0;
    t.m[0][2] = 0;
    t.m[0][3] = 0;
    t.m[1][0] = 0;
    t.m[1][1] = y;
    t.m[1][2] = 0;
    t.m[1][3] = 0;
    t.m[2][0] = 0;
    t.m[2][1] = 0;
    t.m[2][2] = z;
    t.m[2][3] = 0;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

Transform Transform::scale(const Vector &v) const {
    return scale(v.x, v.y, v.z);
}

Transform Transform::scaleLocal(float factor, const Vector &origin,
                                const Vector &direction) const {
    Transform t;
    factor = 1 - factor;
    t.m[0][0] = 1 - factor * direction.x * direction.x;
    t.m[1][1] = 1 - factor * direction.y * direction.y;
    t.m[2][2] = 1 - factor * direction.z * direction.z;
    factor *= -1;
    t.m[0][1] = t.m[1][0] = factor * direction.x * direction.y;
    t.m[0][2] = t.m[2][0] = factor * direction.x * direction.z;
    t.m[1][2] = t.m[2][1] = factor * direction.y * direction.z;
    factor *= -(origin.x * direction.x + origin.y * direction.y +
                origin.z * direction.z);
    t.m[0][3] = factor * direction.x;
    t.m[1][3] = factor * direction.y;
    t.m[2][3] = factor * direction.z;
    return t;
}

Transform Transform::rotateX(float angle) const {
    Transform t;
    const float sin_t = sin(angle);
    const float cos_t = cos(angle);
    t.m[0][0] = 1;
    t.m[0][1] = 0;
    t.m[0][2] = 0;
    t.m[0][3] = 0;
    t.m[1][0] = 0;
    t.m[1][1] = cos_t;
    t.m[1][2] = -sin_t;
    t.m[1][3] = 0;
    t.m[2][0] = 0;
    t.m[2][1] = sin_t;
    t.m[2][2] = cos_t;
    t.m[2][3] = 0;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

Transform Transform::rotateY(float angle) const {
    Transform t;
    const float sin_t = sin(angle);
    const float cos_t = cos(angle);
    t.m[0][0] = cos_t;
    t.m[0][1] = 0;
    t.m[0][2] = sin_t;
    t.m[0][3] = 0;
    t.m[1][0] = 0;
    t.m[1][1] = 1;
    t.m[1][2] = 0;
    t.m[1][3] = 0;
    t.m[2][0] = -sin_t;
    t.m[2][1] = 0;
    t.m[2][2] = cos_t;
    t.m[2][3] = 0;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

Transform Transform::rotateZ(float angle) const {
    Transform t;
    const float sin_t = sin(angle);
    const float cos_t = cos(angle);
    t.m[0][0] = cos_t;
    t.m[0][1] = -sin_t;
    t.m[0][2] = 0;
    t.m[0][3] = 0;
    t.m[1][0] = sin_t;
    t.m[1][1] = cos_t;
    t.m[1][2] = 0;
    t.m[1][3] = 0;
    t.m[2][0] = 0;
    t.m[2][1] = 0;
    t.m[2][2] = 1;
    t.m[2][3] = 0;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

Transform Transform::transpose() const {
    Transform t;
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            t.m[j][i] = m[i][j];
    return t;
}

Transform Transform::rotateAxis(float angle, const Vector &axis) const {
    Transform t;
    const float s = sin(angle);
    const float c = cos(angle);
    t.m[0][0] = axis.x * axis.x + (1 - axis.x * axis.x) * c;
    t.m[0][1] = axis.x * axis.y * (1 - c) - axis.z * s;
    t.m[0][2] = axis.x * axis.z * (1 - c) + axis.y * s;
    t.m[0][3] = 0;
    t.m[1][0] = axis.x * axis.y * (1 - c) + axis.z * s;
    t.m[1][1] = axis.y * axis.y + (1 - axis.y * axis.y) * c;
    t.m[1][2] = axis.y * axis.z * (1 - c) - axis.x * s;
    t.m[1][3] = 0;
    t.m[2][0] = axis.x * axis.z * (1 - c) - axis.y * s;
    t.m[2][1] = axis.y * axis.z * (1 - c) + axis.x * s;
    t.m[2][2] = axis.z * axis.z + (1 - axis.z * axis.z) * c;
    t.m[2][3] = 0;
    t.m[3][0] = 0;
    t.m[3][1] = 0;
    t.m[3][2] = 0;
    t.m[3][3] = 1;
    return t;
}

float Transform::determinant() const {
    return m[0][0] * m[1][1] * m[2][2] * m[3][3] -
           m[0][0] * m[1][1] * m[2][3] * m[3][2] +
           m[0][0] * m[1][2] * m[2][3] * m[3][1] -
           m[0][0] * m[1][2] * m[2][1] * m[3][3] +
           m[0][0] * m[1][3] * m[2][1] * m[3][2] -
           m[0][0] * m[1][3] * m[2][2] * m[3][1] -
           m[0][1] * m[1][2] * m[2][3] * m[3][0] +
           m[0][1] * m[1][2] * m[2][0] * m[3][3] -
           m[0][1] * m[1][3] * m[2][0] * m[3][2] +
           m[0][1] * m[1][3] * m[2][2] * m[3][0] -
           m[0][1] * m[1][0] * m[2][2] * m[3][3] +
           m[0][1] * m[1][0] * m[2][3] * m[3][2] +
           m[0][2] * m[1][3] * m[2][0] * m[3][1] -
           m[0][2] * m[1][3] * m[2][1] * m[3][0] +
           m[0][2] * m[1][0] * m[2][1] * m[3][3] -
           m[0][2] * m[1][0] * m[2][3] * m[3][1] +
           m[0][2] * m[1][1] * m[2][3] * m[3][0] -
           m[0][2] * m[1][1] * m[2][0] * m[3][3] -
           m[0][3] * m[1][0] * m[2][1] * m[3][2] +
           m[0][3] * m[1][0] * m[2][2] * m[3][1] -
           m[0][3] * m[1][1] * m[2][2] * m[3][0] +
           m[0][3] * m[1][1] * m[2][0] * m[3][2] -
           m[0][3] * m[1][2] * m[2][0] * m[3][1] +
           m[0][3] * m[1][2] * m[2][1] * m[3][0];
}

Vector Transform::getEuler() const {
    return Vector(atan2(m[2][1], m[2][2]),
                  atan2(-m[2][0], sqrt(m[2][1] * m[2][1] + m[2][2] * m[2][2])),
                  atan2(m[1][0], m[0][0]));
}

Vector Transform::getTranslate() const {
    return Vector(m[0][3], m[1][3], m[2][3]);
}

Transform Transform::orthographic(float znear, float zfar) const {
    Transform s, t;
    s.scale(1, 1, 1 / (zfar - znear));
    t.translate(0.f, 0.f, -znear);
    t = s * t;
    return t;
}

Transform Transform::perspective(float fov, float n, float f) const {
    Transform t, s;
    t.m[2][2] = f / (f - n);
    t.m[2][3] = -f * n / (f - n);
    t.m[3][2] = 1;
    t.m[3][3] = 0;
    const float invTanAng = 1 / tanf(fov / 2);
    s = s.scale(invTanAng, invTanAng, 1);
    t = s * t;
    return t;
}

} // namespace Geometry
} // namespace meshTools
