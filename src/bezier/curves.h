/**
 * @file curves.h
 * @brief Curve interpolation classes (Lagrange, Bezier, and Spline)
 */

#pragma once
#include <iostream>
#include <vector>
#define EPSILON 0.00001 ///< Small epsilon value for floating-point comparisons

/**
 * @namespace curves
 * @brief Curve interpolation utilities
 */
namespace curves {

/**
 * @brief Blending function b
 * @param t Parameter value
 * @return Blending function value
 */
float b(float t);

/**
 * @brief Evaluate the blending functions for Lagrange interpolation
 * @param n Control point index (1-4)
 * @param t Parameter value
 * @return Blending function value
 */
inline float B(const int &n, float t)
{
    switch (n) {
    case 1:
        return -t * (t - 1.0f) * (t - 2.0f) / 6.0f;
        break;
    case 2:
        return (t + 1.0f) * (t - 1.0f) * (t - 2.0f) * 0.5f;
        break;
    case 3:
        return -(t + 1.0f) * t * (t - 2.0f) * 0.5f;
        break;
    case 4:
        return (t + 1.0f) * t * (t - 1.0f) / 6.0f;
        break;
    }
    return 0.0f; // default case, should never happen
}

/**
 * @class Lagrange
 * @brief Lagrange polynomial interpolation
 *
 * This class performs Lagrange polynomial interpolation on a set of control points.
 */
class Lagrange {
  public:
    /** @brief Default constructor */
    Lagrange() {}
    
    /**
     * @brief Construct from control points
     * @param points Vector of control point values
     */
    Lagrange(const std::vector<float> &points) {
        mPoints = points;
        mNumPoints = points.size();
    }
    
    /**
     * @brief Interpolate to generate a desired number of points
     * @param desired_num Number of interpolated points to generate
     * @return Vector of interpolated values
     */
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints; ///< Control points
    size_t mNumPoints;          ///< Number of control points
};

/**
 * @class Bezier
 * @brief Bezier curve interpolation
 *
 * This class performs Bezier curve interpolation on a set of control points.
 */
class Bezier {
  public:
    /** @brief Default constructor */
    Bezier() {}
    
    /**
     * @brief Construct from control points
     * @param points Vector of control point values
     */
    Bezier(const std::vector<float> &points) {
        mPoints = points;

        mNumPoints = points.size();
    };
    
    /**
     * @brief Interpolate to generate a desired number of points
     * @param desired_num Number of interpolated points to generate
     * @return Vector of interpolated values
     */
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints; ///< Control points
    size_t mNumPoints;          ///< Number of control points
};

/**
 * @class Spline
 * @brief Spline curve interpolation
 *
 * This class performs spline curve interpolation on a set of control points.
 */
class Spline {
  public:
    /** @brief Default constructor */
    Spline() {}
    
    /**
     * @brief Construct from control points
     * @param points Vector of control point values
     */
    Spline(const std::vector<float> &points) {
        mPoints = points;
        mNumPoints = points.size();
    }
    
    /**
     * @brief Interpolate to generate a desired number of points
     * @param desired_num Number of interpolated points to generate
     * @return Vector of interpolated values
     */
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints; ///< Control points
    size_t mNumPoints;          ///< Number of control points
};

/**
 * @class Spline1
 * @brief Alternative spline interpolation implementation
 *
 * This class provides an alternative spline interpolation using raw float arrays.
 */
class Spline1 {
  public:
    /** @brief Default constructor */
    Spline1() {};

    /**
     * @brief Interpolate control points
     * @param mPoints Array of control point values
     * @param mNumPoints Number of control points
     * @param numPoints Output parameter for number of interpolated points
     * @return Array of interpolated values
     */
    float *interpolate(float *mPoints, const size_t &mNumPoints,
                       size_t &numPoints);
};

} // namespace curves