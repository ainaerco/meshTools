#include <gtest/gtest.h>
#include <geometry/vector.h>
#include <cmath>

using namespace meshTools::Geometry;

class VectorTest : public ::testing::Test {
protected:
    Vector v1{1.0f, 2.0f, 3.0f};
    Vector v2{4.0f, 5.0f, 6.0f};
    Vector zero{0.0f, 0.0f, 0.0f};
    Vector unitX{1.0f, 0.0f, 0.0f};
    Vector unitY{0.0f, 1.0f, 0.0f};
    Vector unitZ{0.0f, 0.0f, 1.0f};
};

// Constructor tests
TEST_F(VectorTest, DefaultConstructor) {
    Vector v;
    EXPECT_FLOAT_EQ(v.x, 0.0f);
    EXPECT_FLOAT_EQ(v.y, 0.0f);
    EXPECT_FLOAT_EQ(v.z, 0.0f);
}

TEST_F(VectorTest, ParameterizedConstructor) {
    EXPECT_FLOAT_EQ(v1.x, 1.0f);
    EXPECT_FLOAT_EQ(v1.y, 2.0f);
    EXPECT_FLOAT_EQ(v1.z, 3.0f);
}

TEST_F(VectorTest, VectorFromStdVector) {
    std::vector<float> values = {7.0f, 8.0f, 9.0f};
    Vector v(values);
    EXPECT_FLOAT_EQ(v.x, 7.0f);
    EXPECT_FLOAT_EQ(v.y, 8.0f);
    EXPECT_FLOAT_EQ(v.z, 9.0f);
}

TEST_F(VectorTest, VectorFromArray) {
    float arr[3] = {10.0f, 11.0f, 12.0f};
    Vector v(arr);
    EXPECT_FLOAT_EQ(v.x, 10.0f);
    EXPECT_FLOAT_EQ(v.y, 11.0f);
    EXPECT_FLOAT_EQ(v.z, 12.0f);
}

// Operator tests
TEST_F(VectorTest, AdditionOperator) {
    Vector result = v1 + v2;
    EXPECT_FLOAT_EQ(result.x, 5.0f);
    EXPECT_FLOAT_EQ(result.y, 7.0f);
    EXPECT_FLOAT_EQ(result.z, 9.0f);
}

TEST_F(VectorTest, SubtractionOperator) {
    Vector result = v2 - v1;
    EXPECT_FLOAT_EQ(result.x, 3.0f);
    EXPECT_FLOAT_EQ(result.y, 3.0f);
    EXPECT_FLOAT_EQ(result.z, 3.0f);
}

TEST_F(VectorTest, ScalarMultiplicationRight) {
    Vector result = v1 * 2.0f;
    EXPECT_FLOAT_EQ(result.x, 2.0f);
    EXPECT_FLOAT_EQ(result.y, 4.0f);
    EXPECT_FLOAT_EQ(result.z, 6.0f);
}

TEST_F(VectorTest, ScalarMultiplicationLeft) {
    Vector result = 2.0f * v1;
    EXPECT_FLOAT_EQ(result.x, 2.0f);
    EXPECT_FLOAT_EQ(result.y, 4.0f);
    EXPECT_FLOAT_EQ(result.z, 6.0f);
}

TEST_F(VectorTest, ScalarDivision) {
    Vector result = v1 / 2.0f;
    EXPECT_FLOAT_EQ(result.x, 0.5f);
    EXPECT_FLOAT_EQ(result.y, 1.0f);
    EXPECT_FLOAT_EQ(result.z, 1.5f);
}

TEST_F(VectorTest, NegationOperator) {
    Vector result = -v1;
    EXPECT_FLOAT_EQ(result.x, -1.0f);
    EXPECT_FLOAT_EQ(result.y, -2.0f);
    EXPECT_FLOAT_EQ(result.z, -3.0f);
}

TEST_F(VectorTest, EqualityOperator) {
    Vector v1Copy{1.0f, 2.0f, 3.0f};
    EXPECT_TRUE(v1 == v1Copy);
    EXPECT_FALSE(v1 == v2);
}

TEST_F(VectorTest, InequalityOperator) {
    Vector v1Copy{1.0f, 2.0f, 3.0f};
    EXPECT_FALSE(v1 != v1Copy);
    EXPECT_TRUE(v1 != v2);
}

TEST_F(VectorTest, IndexOperator) {
    EXPECT_FLOAT_EQ(v1[0], 1.0f);
    EXPECT_FLOAT_EQ(v1[1], 2.0f);
    EXPECT_FLOAT_EQ(v1[2], 3.0f);
}

TEST_F(VectorTest, IndexOperatorOutOfRange) {
    EXPECT_THROW(v1[3], const char*);
}

TEST_F(VectorTest, PlusEqualsOperator) {
    Vector v = v1;
    v += v2;
    EXPECT_FLOAT_EQ(v.x, 5.0f);
    EXPECT_FLOAT_EQ(v.y, 7.0f);
    EXPECT_FLOAT_EQ(v.z, 9.0f);
}

TEST_F(VectorTest, MinusEqualsOperator) {
    Vector v = v2;
    v -= v1;
    EXPECT_FLOAT_EQ(v.x, 3.0f);
    EXPECT_FLOAT_EQ(v.y, 3.0f);
    EXPECT_FLOAT_EQ(v.z, 3.0f);
}

TEST_F(VectorTest, TimesEqualsOperator) {
    Vector v = v1;
    v *= 2.0f;
    EXPECT_FLOAT_EQ(v.x, 2.0f);
    EXPECT_FLOAT_EQ(v.y, 4.0f);
    EXPECT_FLOAT_EQ(v.z, 6.0f);
}

TEST_F(VectorTest, DivideEqualsOperator) {
    Vector v = v1;
    v /= 2.0f;
    EXPECT_FLOAT_EQ(v.x, 0.5f);
    EXPECT_FLOAT_EQ(v.y, 1.0f);
    EXPECT_FLOAT_EQ(v.z, 1.5f);
}

// Method tests
TEST_F(VectorTest, Length) {
    EXPECT_FLOAT_EQ(unitX.length(), 1.0f);
    EXPECT_FLOAT_EQ(v1.length(), std::sqrt(14.0f));
}

TEST_F(VectorTest, LengthSquared) {
    EXPECT_FLOAT_EQ(v1.lengthSquared(), 14.0f);
}

TEST_F(VectorTest, Normalize) {
    Vector normalized = v1.normalize();
    EXPECT_NEAR(normalized.length(), 1.0f, 1e-6);
}

TEST_F(VectorTest, NormalizeZeroVector) {
    Vector normalized = zero.normalize();
    EXPECT_FLOAT_EQ(normalized.x, 0.0f);
    EXPECT_FLOAT_EQ(normalized.y, 0.0f);
    EXPECT_FLOAT_EQ(normalized.z, 0.0f);
}

TEST_F(VectorTest, SetLength) {
    Vector result = v1.setLength(5.0f);
    EXPECT_NEAR(result.length(), 5.0f, 1e-6);
}

TEST_F(VectorTest, IsNull) {
    EXPECT_TRUE(zero.isNull());
    EXPECT_FALSE(v1.isNull());
}

TEST_F(VectorTest, ZeroTest) {
    Vector almostZero{0.0000001f, 0.0000001f, 0.0000001f};
    EXPECT_TRUE(zero.zeroTest());
    EXPECT_TRUE(almostZero.zeroTest());
    EXPECT_FALSE(v1.zeroTest());
}

TEST_F(VectorTest, DotProduct) {
    float dot = v1.dot(v2);
    EXPECT_FLOAT_EQ(dot, 32.0f);  // 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
}

TEST_F(VectorTest, DotProductOrthogonal) {
    float dot = unitX.dot(unitY);
    EXPECT_FLOAT_EQ(dot, 0.0f);
}

TEST_F(VectorTest, CrossProduct) {
    Vector cross = unitX.cross(unitY);
    EXPECT_FLOAT_EQ(cross.x, 0.0f);
    EXPECT_FLOAT_EQ(cross.y, 0.0f);
    EXPECT_FLOAT_EQ(cross.z, 1.0f);
}

TEST_F(VectorTest, CrossProductAntiCommutative) {
    Vector cross1 = v1.cross(v2);
    Vector cross2 = v2.cross(v1);
    EXPECT_FLOAT_EQ(cross1.x, -cross2.x);
    EXPECT_FLOAT_EQ(cross1.y, -cross2.y);
    EXPECT_FLOAT_EQ(cross1.z, -cross2.z);
}

TEST_F(VectorTest, Angle) {
    float angle = unitX.angle(unitY);
    EXPECT_NEAR(angle, M_PI / 2.0f, 1e-6);
}

TEST_F(VectorTest, AngleZeroVector) {
    float angle = zero.angle(v1);
    EXPECT_FLOAT_EQ(angle, 0.0f);
}

TEST_F(VectorTest, Lerp) {
    Vector result = v1.lerp(v2, 0.5f);
    EXPECT_FLOAT_EQ(result.x, 2.5f);
    EXPECT_FLOAT_EQ(result.y, 3.5f);
    EXPECT_FLOAT_EQ(result.z, 4.5f);
}

TEST_F(VectorTest, LerpEndpoints) {
    Vector start = v1.lerp(v2, 0.0f);
    Vector end = v1.lerp(v2, 1.0f);
    EXPECT_TRUE(start == v1);
    EXPECT_TRUE(end == v2);
}

TEST_F(VectorTest, Project) {
    Vector result = v1.project(unitX);
    EXPECT_FLOAT_EQ(result.x, 1.0f);
    EXPECT_FLOAT_EQ(result.y, 0.0f);
    EXPECT_FLOAT_EQ(result.z, 0.0f);
}

TEST_F(VectorTest, ToList) {
    std::vector<float> list = v1.toList();
    EXPECT_EQ(list.size(), 3u);
    EXPECT_FLOAT_EQ(list[0], 1.0f);
    EXPECT_FLOAT_EQ(list[1], 2.0f);
    EXPECT_FLOAT_EQ(list[2], 3.0f);
}

TEST_F(VectorTest, ToString) {
    std::string str = v1.toString();
    EXPECT_EQ(str, "[1,2,3]");
}

// Sort tests
TEST(VectorSortTest, SortVectorArray) {
    std::vector<Vector> vectors = {
        Vector{3.0f, 1.0f, 1.0f},
        Vector{1.0f, 2.0f, 2.0f},
        Vector{2.0f, 3.0f, 3.0f}
    };
    sortVectorArray(vectors, 0);  // Sort by x-axis
    EXPECT_FLOAT_EQ(vectors[0].x, 1.0f);
    EXPECT_FLOAT_EQ(vectors[1].x, 2.0f);
    EXPECT_FLOAT_EQ(vectors[2].x, 3.0f);
}

TEST(VectorSortTest, SortedVectorArray) {
    std::vector<Vector> vectors = {
        Vector{1.0f, 3.0f, 1.0f},
        Vector{2.0f, 1.0f, 2.0f},
        Vector{3.0f, 2.0f, 3.0f}
    };
    std::vector<Vector> sorted = sortedVectorArray(vectors, 1);  // Sort by y-axis
    EXPECT_FLOAT_EQ(sorted[0].y, 1.0f);
    EXPECT_FLOAT_EQ(sorted[1].y, 2.0f);
    EXPECT_FLOAT_EQ(sorted[2].y, 3.0f);
    // Original should be unchanged
    EXPECT_FLOAT_EQ(vectors[0].y, 3.0f);
}
