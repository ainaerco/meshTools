#pragma once
#include <iostream>
#include <vector>
#define EPSILON 0.00001

namespace curves {

float b(float t);

inline float B(const int &n, float t)
/* Evaluates the blending functions for Lagrange interpolation. */
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

class Lagrange {
  public:
    Lagrange() {}
    Lagrange(const std::vector<float> &points) {
        mPoints = points;
        mNumPoints = points.size();
    }
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints;
    size_t mNumPoints;
};

class Bezier {
  public:
    Bezier() {}
    Bezier(const std::vector<float> &points) {
        mPoints = points;

        mNumPoints = points.size();
    };
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints;
    size_t mNumPoints;
};

class Spline {
  public:
    Spline() {}
    Spline(const std::vector<float> &points) {
        mPoints = points;
        mNumPoints = points.size();
    }
    std::vector<float> interpolate(const size_t &desired_num);

  private:
    std::vector<float> mPoints;
    size_t mNumPoints;
};

class Spline1 {
  public:
    Spline1() {};

    float *interpolate(float *mPoints, const size_t &mNumPoints,
                       size_t &numPoints);
};

} // namespace curves