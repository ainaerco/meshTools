#ifndef _MESHTOOLS_TR_H
#define _MESHTOOLS_TR_H
#include <cstring>
#include <string>
namespace meshTools {
namespace Geometry {
class Vector;

class Transform {
  public:
    Transform() {
        m[0][0] = m[1][1] = m[2][2] = m[3][3] = 1.0f;
        m[0][1] = m[0][2] = m[0][3] = m[1][0] = m[1][2] = m[1][3] = m[2][0] =
            m[2][1] = m[2][3] = m[3][0] = m[3][1] = m[3][2] = 0.0f;
    }
    Transform(const Vector &v1, const Vector &v2, const Vector &v3);
    Transform(const Vector &v1, const Vector &v4);

    float m[4][4];

    std::string toString() const;
    Transform identity() const;
    Transform lookAt(const Vector &pos, const Vector &look,
                     const Vector &up) const;
    Transform invert() const;
    Transform translate(const Vector &v) const;
    Transform translate(const float &x, const float &y, const float &z) const;
    Transform scale(const Vector &v) const;
    Transform scale(const float &x, const float &y, const float &z) const;
    Transform scaleLocal(float factor, const Vector &origin,
                         const Vector &direction) const;
    Transform rotateX(float angle) const;
    Transform rotateY(float angle) const;
    Transform rotateZ(float angle) const;
    Transform transpose() const;
    Transform rotateAxis(float angle, const Vector &axis) const;
    Transform orthographic(float znear, float zfar) const;
    Transform perspective(float fov, float n, float f) const;
    float determinant() const;
    Vector getEuler() const;
    Vector getTranslate() const;

    friend const Transform operator*(const Transform &left,
                                     const Transform &right) {
        Transform r;
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r.m[i][j] = left.m[i][0] * right.m[0][j] +
                            left.m[i][1] * right.m[1][j] +
                            left.m[i][2] * right.m[2][j] +
                            left.m[i][3] * right.m[3][j];
        return r;
    }

    Transform &operator=(const Transform &other) {
        memcpy(&m, &other.m, sizeof(m));
        return *this;
    }

    Transform &operator*=(const Transform &other) {
        float r[4][4];
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r[i][j] = m[i][0] * other.m[0][j] + m[i][1] * other.m[1][j] +
                          m[i][2] * other.m[2][j] + m[i][3] * other.m[3][j];
        memcpy(&m, &r, sizeof(m));
        return (*this);
    }

    float *operator[](const size_t &index) { return m[index]; }
    const float *operator[](const size_t &index) const { return m[index]; }
};

} // namespace Geometry
} // namespace meshTools

#endif