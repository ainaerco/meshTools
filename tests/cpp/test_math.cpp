#include <gtest/gtest.h>
#include <geometry/math.h>
#include <geometry/vector.h>
#include <cmath>

using namespace meshTools::Geometry;

class MathTest : public ::testing::Test {
protected:
    Vector v1{1.0f, 2.0f, 3.0f};
};

// Epsilon tests
TEST_F(MathTest, EpsilonTestTrue) {
    EXPECT_TRUE(math::epsilonTest(0.0f, 0.0f));
    EXPECT_TRUE(math::epsilonTest(0.0000001f, 0.0f));
    EXPECT_TRUE(math::epsilonTest(1.0f, 1.0f + 0.0000001f));
}

TEST_F(MathTest, EpsilonTestFalse) {
    EXPECT_FALSE(math::epsilonTest(0.0f, 1.0f));
    EXPECT_FALSE(math::epsilonTest(0.0f, 0.001f, 0.0001f));
}

TEST_F(MathTest, EpsilonTestCustomEpsilon) {
    EXPECT_TRUE(math::epsilonTest(0.0f, 0.05f, 0.1f));
    EXPECT_FALSE(math::epsilonTest(0.0f, 0.2f, 0.1f));
}

// Lerp tests
TEST_F(MathTest, LerpStart) {
    EXPECT_FLOAT_EQ(math::lerp(0.0f, 1.0f, 5.0f), 1.0f);
}

TEST_F(MathTest, LerpEnd) {
    EXPECT_FLOAT_EQ(math::lerp(1.0f, 1.0f, 5.0f), 5.0f);
}

TEST_F(MathTest, LerpMiddle) {
    EXPECT_FLOAT_EQ(math::lerp(0.5f, 0.0f, 10.0f), 5.0f);
}

TEST_F(MathTest, LerpNegative) {
    EXPECT_FLOAT_EQ(math::lerp(0.5f, -10.0f, 10.0f), 0.0f);
}

// Fit tests
TEST_F(MathTest, FitMiddle) {
    float result = math::fit(5.0f, 0.0f, 10.0f, 0.0f, 100.0f);
    EXPECT_FLOAT_EQ(result, 50.0f);
}

TEST_F(MathTest, FitStart) {
    float result = math::fit(0.0f, 0.0f, 10.0f, 0.0f, 100.0f);
    EXPECT_FLOAT_EQ(result, 0.0f);
}

TEST_F(MathTest, FitEnd) {
    float result = math::fit(10.0f, 0.0f, 10.0f, 0.0f, 100.0f);
    EXPECT_FLOAT_EQ(result, 100.0f);
}

TEST_F(MathTest, FitInvertedRange) {
    float result = math::fit(5.0f, 0.0f, 10.0f, 100.0f, 0.0f);
    EXPECT_FLOAT_EQ(result, 50.0f);
}

// Min/Max tests
TEST_F(MathTest, MaxFirstLarger) {
    EXPECT_FLOAT_EQ(math::max(5.0f, 3.0f), 5.0f);
}

TEST_F(MathTest, MaxSecondLarger) {
    EXPECT_FLOAT_EQ(math::max(3.0f, 5.0f), 5.0f);
}

TEST_F(MathTest, MaxEqual) {
    EXPECT_FLOAT_EQ(math::max(5.0f, 5.0f), 5.0f);
}

TEST_F(MathTest, MaxNegative) {
    EXPECT_FLOAT_EQ(math::max(-5.0f, -3.0f), -3.0f);
}

TEST_F(MathTest, MinFirstSmaller) {
    EXPECT_FLOAT_EQ(math::min(3.0f, 5.0f), 3.0f);
}

TEST_F(MathTest, MinSecondSmaller) {
    EXPECT_FLOAT_EQ(math::min(5.0f, 3.0f), 3.0f);
}

TEST_F(MathTest, MinEqual) {
    EXPECT_FLOAT_EQ(math::min(5.0f, 5.0f), 5.0f);
}

TEST_F(MathTest, MinNegative) {
    EXPECT_FLOAT_EQ(math::min(-5.0f, -3.0f), -5.0f);
}

// Interpolate Bezier tests
TEST_F(MathTest, InterpolateBezierStart) {
    float result = math::interpolateBezier(0.0f, 0.0f, 1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(result, 0.0f);
}

TEST_F(MathTest, InterpolateBezierEnd) {
    float result = math::interpolateBezier(1.0f, 0.0f, 1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(result, 3.0f);
}

TEST_F(MathTest, InterpolateBezierMiddle) {
    float result = math::interpolateBezier(0.5f, 0.0f, 0.0f, 1.0f, 1.0f);
    // At t=0.5, the result should be close to middle value
    EXPECT_TRUE(result > 0.0f && result < 1.0f);
}

// Interpolate Catmull-Rom tests
TEST_F(MathTest, InterpolateCatmullRomStart) {
    // At t=0, should return p1
    float result = math::interpolateCatmullRom(0.0f, 0.0f, 1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(result, 1.0f);
}

TEST_F(MathTest, InterpolateCatmullRomEnd) {
    // At t=1, should return p2
    float result = math::interpolateCatmullRom(1.0f, 0.0f, 1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(result, 2.0f);
}

// Barycentric coordinate tests
TEST_F(MathTest, GetBarycentricAtVertex) {
    Vector a{0.0f, 0.0f, 0.0f};
    Vector b{1.0f, 0.0f, 0.0f};
    Vector c{0.0f, 1.0f, 0.0f};
    
    // Point at vertex a
    Vector bary = math::getBarycentric(a, a, b, c);
    EXPECT_NEAR(bary.x, 1.0f, 1e-5);
    EXPECT_NEAR(bary.y, 0.0f, 1e-5);
    EXPECT_NEAR(bary.z, 0.0f, 1e-5);
}

TEST_F(MathTest, GetBarycentricAtCenter) {
    Vector a{0.0f, 0.0f, 0.0f};
    Vector b{3.0f, 0.0f, 0.0f};
    Vector c{0.0f, 3.0f, 0.0f};
    Vector center{1.0f, 1.0f, 0.0f};
    
    Vector bary = math::getBarycentric(center, a, b, c);
    // At center, barycentric coordinates should sum to 1
    float sum = bary.x + bary.y + bary.z;
    EXPECT_NEAR(sum, 1.0f, 1e-5);
}

// Point in polygon tests
TEST_F(MathTest, PointInPolyInside) {
    std::vector<Vector> poly = {
        Vector{0.0f, 0.0f, 0.0f},
        Vector{4.0f, 0.0f, 0.0f},
        Vector{4.0f, 4.0f, 0.0f},
        Vector{0.0f, 4.0f, 0.0f}
    };
    Vector point{2.0f, 2.0f, 0.0f};
    
    EXPECT_TRUE(math::pointInPoly(point, poly));
}

TEST_F(MathTest, PointInPolyOutside) {
    std::vector<Vector> poly = {
        Vector{0.0f, 0.0f, 0.0f},
        Vector{4.0f, 0.0f, 0.0f},
        Vector{4.0f, 4.0f, 0.0f},
        Vector{0.0f, 4.0f, 0.0f}
    };
    Vector point{5.0f, 5.0f, 0.0f};
    
    EXPECT_FALSE(math::pointInPoly(point, poly));
}

TEST_F(MathTest, PointInPolyOnEdge) {
    std::vector<Vector> poly = {
        Vector{0.0f, 0.0f, 0.0f},
        Vector{4.0f, 0.0f, 0.0f},
        Vector{4.0f, 4.0f, 0.0f},
        Vector{0.0f, 4.0f, 0.0f}
    };
    Vector point{2.0f, 0.0f, 0.0f};  // On the bottom edge
    
    // Edge case behavior may vary
    bool result = math::pointInPoly(point, poly);
    // Just verify it doesn't crash
    (void)result;
}

// Solve cubic tests
TEST_F(MathTest, SolveCubicTripleRoot) {
    // x^3 = 0 has triple root at 0
    // Equation: ax^3 + bx^2 + cx + d = 0
    // For x^3 = 0: a=1, b=0, c=0, d=0
    Vector roots = math::solveCubic(1.0f, 0.0f, 0.0f, 0.0f);
    EXPECT_NEAR(roots.x, 0.0f, 1e-5);
    EXPECT_NEAR(roots.y, 0.0f, 1e-5);
    EXPECT_NEAR(roots.z, 0.0f, 1e-5);
}

TEST_F(MathTest, SolveCubicSimple) {
    // (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6
    // a=1, b=-6, c=11, d=-6
    Vector roots = math::solveCubic(1.0f, -6.0f, 11.0f, -6.0f);
    
    // Verify roots sum to 6 (by Vieta's formulas, -b/a = 6)
    float sum = roots.x + roots.y + roots.z;
    EXPECT_NEAR(sum, 6.0f, 1e-3);
}
