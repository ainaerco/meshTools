#include <gtest/gtest.h>
#include <bezier/curves.h>
#include <cmath>

using namespace curves;

class CurvesTest : public ::testing::Test {
protected:
    // Control points for Bezier curves need 4 + 3*n points for n segments
    // (7 points minimum for one complete segment plus partial second)
    std::vector<float> bezierPoints = {
        0.0f, 0.0f,   // P0
        1.0f, 2.0f,   // P1
        2.0f, 2.0f,   // P2
        3.0f, 0.0f,   // P3
        4.0f, 1.0f,   // P4
        5.0f, 1.0f,   // P5
        6.0f, 0.0f    // P6
    };
    
    // More control points for longer curves
    std::vector<float> longerPoints = {
        0.0f, 0.0f,
        1.0f, 2.0f,
        2.0f, 2.0f,
        3.0f, 0.0f,
        4.0f, 1.0f,
        5.0f, 1.0f,
        6.0f, 0.0f,
        7.0f, 0.0f
    };
};

// B-spline blending function tests
TEST_F(CurvesTest, BFunctionBelowRange) {
    EXPECT_FLOAT_EQ(b(-3.0f), 0.0f);
}

TEST_F(CurvesTest, BFunctionAboveRange) {
    EXPECT_FLOAT_EQ(b(3.0f), 0.0f);
}

TEST_F(CurvesTest, BFunctionAtZero) {
    float result = b(0.0f);
    // B-spline basis at 0 should be positive
    EXPECT_GT(result, 0.0f);
}

TEST_F(CurvesTest, BFunctionSymmetry) {
    // B-spline basis function should be symmetric around 0
    EXPECT_NEAR(b(-1.5f), b(1.5f), 1e-6);
    EXPECT_NEAR(b(-0.5f), b(0.5f), 1e-6);
}

TEST_F(CurvesTest, BFunctionContinuity) {
    // Check values at boundaries are continuous
    float atMinus1 = b(-1.0f);
    float atMinus1Plus = b(-1.0f + 0.0001f);
    EXPECT_NEAR(atMinus1, atMinus1Plus, 0.01f);
}

// Blending function B tests
TEST_F(CurvesTest, BlendingFunctionB1) {
    float result = B(1, 0.5f);
    // B1 should return a valid value
    EXPECT_TRUE(std::isfinite(result));
}

TEST_F(CurvesTest, BlendingFunctionB2) {
    float result = B(2, 0.5f);
    EXPECT_TRUE(std::isfinite(result));
}

TEST_F(CurvesTest, BlendingFunctionB3) {
    float result = B(3, 0.5f);
    EXPECT_TRUE(std::isfinite(result));
}

TEST_F(CurvesTest, BlendingFunctionB4) {
    float result = B(4, 0.5f);
    EXPECT_TRUE(std::isfinite(result));
}

TEST_F(CurvesTest, BlendingFunctionDefault) {
    // Invalid n should return 0
    float result = B(5, 0.5f);
    EXPECT_FLOAT_EQ(result, 0.0f);
}

// Bezier class tests
TEST_F(CurvesTest, BezierDefaultConstructor) {
    Bezier bezier;
    // Just verify it doesn't crash
}

TEST_F(CurvesTest, BezierConstructorWithPoints) {
    Bezier bezier(bezierPoints);
    // Verify construction doesn't crash
}

TEST_F(CurvesTest, BezierInterpolate) {
    Bezier bezier(bezierPoints);
    std::vector<float> result = bezier.interpolate(10);
    
    // Result should have points (x,y pairs)
    EXPECT_GT(result.size(), 0u);
    EXPECT_EQ(result.size() % 2, 0u);  // Should be even (x,y pairs)
}

TEST_F(CurvesTest, BezierInterpolateEndpoints) {
    Bezier bezier(bezierPoints);
    std::vector<float> result = bezier.interpolate(10);
    
    // First point should be close to first control point
    EXPECT_NEAR(result[0], bezierPoints[0], 0.1f);
    EXPECT_NEAR(result[1], bezierPoints[1], 0.1f);
    
    // Last point should be close to last control point
    size_t lastIdx = result.size() - 2;
    size_t lastCtrlIdx = bezierPoints.size() - 2;
    EXPECT_NEAR(result[lastIdx], bezierPoints[lastCtrlIdx], 0.1f);
    EXPECT_NEAR(result[lastIdx + 1], bezierPoints[lastCtrlIdx + 1], 0.1f);
}

// Lagrange class tests
TEST_F(CurvesTest, LagrangeDefaultConstructor) {
    Lagrange lagrange;
    // Verify construction doesn't crash
}

TEST_F(CurvesTest, LagrangeConstructorWithPoints) {
    Lagrange lagrange(longerPoints);
    // Verify construction doesn't crash
}

TEST_F(CurvesTest, LagrangeInterpolate) {
    Lagrange lagrange(longerPoints);
    std::vector<float> result = lagrange.interpolate(20);
    
    // Result should have points
    EXPECT_GT(result.size(), 0u);
    EXPECT_EQ(result.size() % 2, 0u);  // Should be even (x,y pairs)
}

// Spline class tests
TEST_F(CurvesTest, SplineDefaultConstructor) {
    Spline spline;
    // Verify construction doesn't crash
}

TEST_F(CurvesTest, SplineConstructorWithPoints) {
    Spline spline(longerPoints);
    // Verify construction doesn't crash
}

TEST_F(CurvesTest, SplineInterpolate) {
    Spline spline(longerPoints);
    std::vector<float> result = spline.interpolate(20);
    
    // Result should have points
    EXPECT_GT(result.size(), 0u);
    EXPECT_EQ(result.size() % 2, 0u);  // Should be even (x,y pairs)
}

TEST_F(CurvesTest, SplineInterpolateSmoothness) {
    Spline spline(longerPoints);
    std::vector<float> result = spline.interpolate(50);
    
    // Check that consecutive points don't jump wildly
    for (size_t i = 2; i < result.size(); i += 2) {
        float dx = result[i] - result[i-2];
        float dy = result[i+1] - result[i-1];
        float dist = std::sqrt(dx*dx + dy*dy);
        // Distance between consecutive points should be reasonable
        EXPECT_LT(dist, 2.0f);
    }
}

// Spline1 class tests
TEST_F(CurvesTest, Spline1Interpolate) {
    Spline1 spline1;
    size_t numPoints = 20;
    float* points = new float[longerPoints.size()];
    for (size_t i = 0; i < longerPoints.size(); i++) {
        points[i] = longerPoints[i];
    }
    
    float* result = spline1.interpolate(points, longerPoints.size(), numPoints);
    
    // Result should be valid
    EXPECT_NE(result, nullptr);
    
    // Clean up
    delete[] points;
    delete[] result;
}

// Edge cases
TEST_F(CurvesTest, BezierMinimalPoints) {
    // Bezier needs at least 7 control points (14 floats for x,y pairs)
    std::vector<float> minPoints = {
        0.0f, 0.0f,
        1.0f, 1.0f,
        2.0f, 0.0f,
        3.0f, 1.0f,
        4.0f, 0.0f,
        5.0f, 1.0f,
        6.0f, 0.0f
    };
    Bezier bezier(minPoints);
    std::vector<float> result = bezier.interpolate(5);
    EXPECT_GT(result.size(), 0u);
}
