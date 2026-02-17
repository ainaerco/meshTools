#ifndef _MESHTOOLS_VECTOR_H
#define _MESHTOOLS_VECTOR_H

#include <iostream>
#include <string>
#include <vector>

namespace meshTools {
namespace Geometry {
class Transform;
class Vector {
  public:
    Vector()
        : x(0.0), y(0.0), z(0.0) {}
    Vector(std::vector<float> a)
        : x(a[0]), y(a[1]), z(a[2]) {}

    Vector(float a[3])
        : x(a[0]), y(a[1]), z(a[2]) {}

    Vector(float a, float b, float c)
        : x(a), y(b), z(c) {}

    std::vector<float> toList();
    std::string toString();
    Vector setLength(float length);
    Vector normalize();
    bool isNull();
    bool zeroTest();
    float lengthSquared();
    float length();
    float angle(Vector other);
    float dot(const Vector &other);
    Vector cross(const Vector &other);
    Vector lerp(Vector other, float factor);
    Vector slerp(Vector other, float factor);
    Vector project(Vector other);
    Vector reflect(Vector other);
    Vector rotateAround(Vector axis, float angle);
    Vector applyTransform(Transform t);

    float x;
    float y;
    float z;

    friend const Vector operator+(const Vector &left, const Vector &right) {
        return Vector(left.x + right.x, left.y + right.y, left.z + right.z);
    }

    Vector &operator+=(const Vector &v) {
        x += v.x;
        y += v.y;
        z += v.z;
        return (*this);
    }

    friend const Vector operator-(const Vector &left, const Vector &right) {
        return Vector(left.x - right.x, left.y - right.y, left.z - right.z);
    }

    Vector &operator-=(const Vector &v) {
        x -= v.x;
        y -= v.y;
        z -= v.z;
        return (*this);
    }

    friend const Vector operator*(const Vector &left, const float &right) {
        return Vector(left.x * right, left.y * right, left.z * right);
    }
    friend const Vector operator*(const float &left, const Vector &right) {
        return Vector(left * right.x, left * right.y, left * right.z);
    }
    Vector &operator*=(const float &v) {
        x *= v;
        y *= v;
        z *= v;
        return (*this);
    }

    friend const Vector operator/(const Vector &left, const float &right) {
        return left * (1 / right);
    }
    Vector &operator/=(float v) {
        v = 1.0f / v;
        x *= v;
        y *= v;
        z *= v;
        return (*this);
    }

    friend const bool operator==(const Vector &left, const Vector &right) {
        return (left.x == right.x) && (left.y == right.y) &&
               (left.z == right.z);
    }

    friend const bool operator!=(const Vector &left, const Vector &right) {
        return !((left.x == right.x) && (left.y == right.y) &&
                 (left.z == right.z));
    }

    Vector operator-() { return Vector(-x, -y, -z); }

    float operator[](const size_t &index) {
        if (index == 0) {
            return x;
        } else if (index == 1) {
            return y;
        } else if (index == 2) {
            return z;
        } else {
            throw "Index out of range";
        }
    }

    friend std::ostream &operator<<(std::ostream &os, const Vector &v) {
        os << "[" << v.x << "," << v.y << "," << v.z << "]";
        return os;
    }
};

bool sortVectorArray(std::vector<Vector> &v, int axis);
std::vector<Vector> sortedVectorArray(std::vector<Vector> v, int axis);

} // namespace Geometry
} // namespace meshTools

#endif