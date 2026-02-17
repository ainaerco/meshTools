/**
 * @file vector.h
 * @brief 3D vector class with geometric operations
 */

#pragma once

// Forward declarations for stream operators (avoid pulling <iostream>/<ostream>
// into this header).
#include <iosfwd>
#include <string>
#include <vector>

namespace meshTools {
namespace Geometry {
class Transform;

/**
 * @class Vector
 * @brief A 3D vector class for geometric operations
 *
 * This class represents a 3D vector with x, y, z components and provides
 * various geometric operations including vector arithmetic, transformations,
 * and interpolations.
 */
class Vector {
  public:
    /** @brief Default constructor, initializes vector to (0, 0, 0) */
    Vector() : x(0.0), y(0.0), z(0.0) {}

    /**
     * @brief Construct from std::vector
     * @param a Vector containing at least 3 float values
     */
    Vector(const std::vector<float> &a) : x(a[0]), y(a[1]), z(a[2]) {}

    /**
     * @brief Construct from float array
     * @param a Array of at least 3 floats
     */
    Vector(float a[3]) : x(a[0]), y(a[1]), z(a[2]) {}

    /**
     * @brief Construct from three float values
     * @param a X component
     * @param b Y component
     * @param c Z component
     */
    Vector(float a, float b, float c) : x(a), y(b), z(c) {}

    /**
     * @brief Convert vector to std::vector<float>
     * @return Vector components as a list [x, y, z]
     */
    std::vector<float> toList() const;

    /**
     * @brief Convert vector to string representation
     * @return String representation of the vector
     */
    std::string toString() const;

    /**
     * @brief Set the length of the vector
     * @param length Desired length
     * @return New vector with the specified length in the same direction
     */
    Vector setLength(float length) const;

    /**
     * @brief Normalize the vector to unit length
     * @return Normalized vector
     */
    Vector normalize() const;

    /**
     * @brief Check if vector is null (all components are zero)
     * @return True if vector is null, false otherwise
     */
    bool isNull() const;

    /**
     * @brief Test if vector is approximately zero
     * @return True if vector is approximately zero, false otherwise
     */
    bool zeroTest() const;

    /**
     * @brief Calculate the squared length of the vector
     * @return Squared length (magnitude) of the vector
     */
    float lengthSquared() const;

    /**
     * @brief Calculate the length of the vector
     * @return Length (magnitude) of the vector
     */
    float length() const;

    /**
     * @brief Calculate angle between this vector and another
     * @param other The other vector
     * @return Angle in radians between the two vectors
     */
    float angle(const Vector &other) const;

    /**
     * @brief Calculate dot product with another vector
     * @param other The other vector
     * @return Dot product result
     */
    float dot(const Vector &other) const;

    /**
     * @brief Calculate cross product with another vector
     * @param other The other vector
     * @return Cross product result (perpendicular vector)
     */
    Vector cross(const Vector &other) const;

    /**
     * @brief Linear interpolation between this vector and another
     * @param other The target vector
     * @param factor Interpolation factor (0.0 to 1.0)
     * @return Interpolated vector
     */
    Vector lerp(const Vector &other, float factor) const;

    /**
     * @brief Spherical linear interpolation between this vector and another
     * @param other The target vector
     * @param factor Interpolation factor (0.0 to 1.0)
     * @return Interpolated vector
     */
    Vector slerp(const Vector &other, float factor) const;

    /**
     * @brief Project this vector onto another vector
     * @param other The vector to project onto
     * @return Projected vector
     */
    Vector project(const Vector &other) const;

    /**
     * @brief Reflect this vector across another vector
     * @param other The vector to reflect across (should be normalized)
     * @return Reflected vector
     */
    Vector reflect(const Vector &other) const;

    /**
     * @brief Rotate this vector around an axis
     * @param axis The rotation axis
     * @param angle Rotation angle in radians
     * @return Rotated vector
     */
    Vector rotateAround(const Vector &axis, float angle) const;

    /**
     * @brief Apply a transformation matrix to this vector
     * @param t The transformation matrix
     * @return Transformed vector
     */
    Vector applyTransform(const Transform &t) const;

    float x; ///< X component of the vector
    float y; ///< Y component of the vector
    float z; ///< Z component of the vector

    /**
     * @brief Vector addition operator
     * @param left Left operand vector
     * @param right Right operand vector
     * @return Sum of the two vectors
     */
    friend const Vector operator+(const Vector &left, const Vector &right) {
        return Vector(left.x + right.x, left.y + right.y, left.z + right.z);
    }

    /**
     * @brief Vector addition assignment operator
     * @param v Vector to add
     * @return Reference to this vector after addition
     */
    Vector &operator+=(const Vector &v) {
        x += v.x;
        y += v.y;
        z += v.z;
        return (*this);
    }

    /**
     * @brief Vector subtraction operator
     * @param left Left operand vector
     * @param right Right operand vector
     * @return Difference of the two vectors
     */
    friend const Vector operator-(const Vector &left, const Vector &right) {
        return Vector(left.x - right.x, left.y - right.y, left.z - right.z);
    }

    /**
     * @brief Vector subtraction assignment operator
     * @param v Vector to subtract
     * @return Reference to this vector after subtraction
     */
    Vector &operator-=(const Vector &v) {
        x -= v.x;
        y -= v.y;
        z -= v.z;
        return (*this);
    }

    /**
     * @brief Vector-scalar multiplication operator
     * @param left Vector operand
     * @param right Scalar operand
     * @return Scaled vector
     */
    friend const Vector operator*(const Vector &left, const float &right) {
        return Vector(left.x * right, left.y * right, left.z * right);
    }

    /**
     * @brief Scalar-vector multiplication operator
     * @param left Scalar operand
     * @param right Vector operand
     * @return Scaled vector
     */
    friend const Vector operator*(const float &left, const Vector &right) {
        return Vector(left * right.x, left * right.y, left * right.z);
    }

    /**
     * @brief Vector-scalar multiplication assignment operator
     * @param v Scalar to multiply by
     * @return Reference to this vector after multiplication
     */
    Vector &operator*=(const float &v) {
        x *= v;
        y *= v;
        z *= v;
        return (*this);
    }

    /**
     * @brief Vector-scalar division operator
     * @param left Vector operand
     * @param right Scalar divisor
     * @return Scaled vector
     */
    friend const Vector operator/(const Vector &left, const float &right) {
        return left * (1 / right);
    }

    /**
     * @brief Vector-scalar division assignment operator
     * @param v Scalar to divide by
     * @return Reference to this vector after division
     */
    Vector &operator/=(float v) {
        v = 1.0f / v;
        x *= v;
        y *= v;
        z *= v;
        return (*this);
    }

    /**
     * @brief Vector equality operator
     * @param left Left operand vector
     * @param right Right operand vector
     * @return True if vectors are equal, false otherwise
     */
    friend const bool operator==(const Vector &left, const Vector &right) {
        return (left.x == right.x) && (left.y == right.y) &&
               (left.z == right.z);
    }

    /**
     * @brief Vector inequality operator
     * @param left Left operand vector
     * @param right Right operand vector
     * @return True if vectors are not equal, false otherwise
     */
    friend const bool operator!=(const Vector &left, const Vector &right) {
        return !((left.x == right.x) && (left.y == right.y) &&
                 (left.z == right.z));
    }

    /**
     * @brief Unary negation operator
     * @return Negated vector
     */
    Vector operator-() const { return Vector(-x, -y, -z); }

    /**
     * @brief Array subscript operator for const access
     * @param index Component index (0=x, 1=y, 2=z)
     * @return Component value at the specified index
     * @throws const char* if index is out of range
     */
    float operator[](const size_t &index) const {
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

    /**
     * @brief Stream output operator
     * @param os Output stream
     * @param v Vector to output
     * @return Reference to the output stream
     */
    friend std::ostream &operator<<(std::ostream &os, const Vector &v);
};

/**
 * @brief Sort an array of vectors along a specified axis
 * @param v Vector array to sort (modified in place)
 * @param axis Axis to sort along (0=x, 1=y, 2=z)
 * @return True if sorting was successful
 */
bool sortVectorArray(std::vector<Vector> &v, int axis);

/**
 * @brief Create a sorted copy of a vector array along a specified axis
 * @param v Vector array to sort
 * @param axis Axis to sort along (0=x, 1=y, 2=z)
 * @return Sorted copy of the vector array
 */
std::vector<Vector> sortedVectorArray(const std::vector<Vector> &v, int axis);

} // namespace Geometry
} // namespace meshTools
