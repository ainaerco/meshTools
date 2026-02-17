/**
 * @file transform.h
 * @brief 4x4 transformation matrix class
 */

#ifndef _MESHTOOLS_TR_H
#define _MESHTOOLS_TR_H
#include <cstring>
#include <string>
namespace meshTools {
namespace Geometry {
class Vector;

/**
 * @class Transform
 * @brief A 4x4 transformation matrix for 3D transformations
 *
 * This class represents a 4x4 homogeneous transformation matrix
 * supporting translation, rotation, scaling, and projection operations.
 */
class Transform {
  public:
    /** @brief Default constructor, initializes to identity matrix */
    Transform() {
        m[0][0] = m[1][1] = m[2][2] = m[3][3] = 1.0f;
        m[0][1] = m[0][2] = m[0][3] = m[1][0] = m[1][2] = m[1][3] = m[2][0] =
            m[2][1] = m[2][3] = m[3][0] = m[3][1] = m[3][2] = 0.0f;
    }
    
    /**
     * @brief Construct from three vectors (3x3 rotation matrix)
     * @param v1 First column vector
     * @param v2 Second column vector
     * @param v3 Third column vector
     */
    Transform(const Vector &v1, const Vector &v2, const Vector &v3);
    
    /**
     * @brief Construct from two vectors
     * @param v1 First vector
     * @param v4 Second vector
     */
    Transform(const Vector &v1, const Vector &v4);

    float m[4][4]; ///< 4x4 transformation matrix

    /**
     * @brief Convert matrix to string representation
     * @return String representation of the matrix
     */
    std::string toString() const;
    
    /**
     * @brief Return identity matrix
     * @return Identity transformation matrix
     */
    Transform identity() const;
    
    /**
     * @brief Create a look-at transformation matrix
     * @param pos Camera position
     * @param look Look-at target position
     * @param up Up direction vector
     * @return Look-at transformation matrix
     */
    Transform lookAt(const Vector &pos, const Vector &look,
                     const Vector &up) const;
    
    /**
     * @brief Compute the inverse of the transformation matrix
     * @return Inverted transformation matrix
     */
    Transform invert() const;
    
    /**
     * @brief Apply translation by a vector
     * @param v Translation vector
     * @return New transformed matrix
     */
    Transform translate(const Vector &v) const;
    
    /**
     * @brief Apply translation by x, y, z components
     * @param x Translation along X axis
     * @param y Translation along Y axis
     * @param z Translation along Z axis
     * @return New transformed matrix
     */
    Transform translate(const float &x, const float &y, const float &z) const;
    
    /**
     * @brief Apply scaling by a vector
     * @param v Scale factors for each axis
     * @return New transformed matrix
     */
    Transform scale(const Vector &v) const;
    
    /**
     * @brief Apply scaling by x, y, z components
     * @param x Scale factor along X axis
     * @param y Scale factor along Y axis
     * @param z Scale factor along Z axis
     * @return New transformed matrix
     */
    Transform scale(const float &x, const float &y, const float &z) const;
    
    /**
     * @brief Apply local scaling along a direction
     * @param factor Scale factor
     * @param origin Origin point for scaling
     * @param direction Direction vector for scaling
     * @return New transformed matrix
     */
    Transform scaleLocal(float factor, const Vector &origin,
                         const Vector &direction) const;
    
    /**
     * @brief Apply rotation around X axis
     * @param angle Rotation angle in radians
     * @return New transformed matrix
     */
    Transform rotateX(float angle) const;
    
    /**
     * @brief Apply rotation around Y axis
     * @param angle Rotation angle in radians
     * @return New transformed matrix
     */
    Transform rotateY(float angle) const;
    
    /**
     * @brief Apply rotation around Z axis
     * @param angle Rotation angle in radians
     * @return New transformed matrix
     */
    Transform rotateZ(float angle) const;
    
    /**
     * @brief Compute the transpose of the matrix
     * @return Transposed matrix
     */
    Transform transpose() const;
    
    /**
     * @brief Apply rotation around an arbitrary axis
     * @param angle Rotation angle in radians
     * @param axis Rotation axis vector
     * @return New transformed matrix
     */
    Transform rotateAxis(float angle, const Vector &axis) const;
    
    /**
     * @brief Create an orthographic projection matrix
     * @param znear Near clipping plane distance
     * @param zfar Far clipping plane distance
     * @return Orthographic projection matrix
     */
    Transform orthographic(float znear, float zfar) const;
    
    /**
     * @brief Create a perspective projection matrix
     * @param fov Field of view angle in radians
     * @param n Near clipping plane distance
     * @param f Far clipping plane distance
     * @return Perspective projection matrix
     */
    Transform perspective(float fov, float n, float f) const;
    
    /**
     * @brief Calculate the determinant of the matrix
     * @return Determinant value
     */
    float determinant() const;
    
    /**
     * @brief Extract Euler angles from the matrix
     * @return Vector containing Euler angles (x, y, z)
     */
    Vector getEuler() const;
    
    /**
     * @brief Extract translation components from the matrix
     * @return Vector containing translation (x, y, z)
     */
    Vector getTranslate() const;

    /**
     * @brief Matrix multiplication operator
     * @param left Left operand matrix
     * @param right Right operand matrix
     * @return Product of the two matrices
     */
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

    /**
     * @brief Assignment operator
     * @param other Matrix to copy from
     * @return Reference to this matrix
     */
    Transform &operator=(const Transform &other) {
        memcpy(&m, &other.m, sizeof(m));
        return *this;
    }

    /**
     * @brief Matrix multiplication assignment operator
     * @param other Matrix to multiply by
     * @return Reference to this matrix after multiplication
     */
    Transform &operator*=(const Transform &other) {
        float r[4][4];
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r[i][j] = m[i][0] * other.m[0][j] + m[i][1] * other.m[1][j] +
                          m[i][2] * other.m[2][j] + m[i][3] * other.m[3][j];
        memcpy(&m, &r, sizeof(m));
        return (*this);
    }

    /**
     * @brief Array subscript operator for non-const access
     * @param index Row index (0-3)
     * @return Pointer to the specified row
     */
    float *operator[](const size_t &index) { return m[index]; }
    
    /**
     * @brief Array subscript operator for const access
     * @param index Row index (0-3)
     * @return Const pointer to the specified row
     */
    const float *operator[](const size_t &index) const { return m[index]; }
};

} // namespace Geometry
} // namespace meshTools

#endif