#include <gtest/gtest.h>
#include <geometry/transform.h>
#include <geometry/vector.h>
#include <cmath>

using namespace meshTools::Geometry;

class TransformTest : public ::testing::Test {
protected:
    Transform identity;
    Vector unitX{1.0f, 0.0f, 0.0f};
    Vector unitY{0.0f, 1.0f, 0.0f};
    Vector unitZ{0.0f, 0.0f, 1.0f};
    Vector v1{1.0f, 2.0f, 3.0f};
};

TEST_F(TransformTest, DefaultConstructorIsIdentity) {
    // Check diagonal is 1
    EXPECT_FLOAT_EQ(identity.m[0][0], 1.0f);
    EXPECT_FLOAT_EQ(identity.m[1][1], 1.0f);
    EXPECT_FLOAT_EQ(identity.m[2][2], 1.0f);
    EXPECT_FLOAT_EQ(identity.m[3][3], 1.0f);
    
    // Check off-diagonal is 0
    EXPECT_FLOAT_EQ(identity.m[0][1], 0.0f);
    EXPECT_FLOAT_EQ(identity.m[0][2], 0.0f);
    EXPECT_FLOAT_EQ(identity.m[0][3], 0.0f);
    EXPECT_FLOAT_EQ(identity.m[1][0], 0.0f);
    EXPECT_FLOAT_EQ(identity.m[1][2], 0.0f);
    EXPECT_FLOAT_EQ(identity.m[1][3], 0.0f);
}

TEST_F(TransformTest, IdentityMethod) {
    Transform t = identity.translate(1.0f, 2.0f, 3.0f);
    Transform id = t.identity();
    EXPECT_FLOAT_EQ(id.m[0][0], 1.0f);
    EXPECT_FLOAT_EQ(id.m[1][1], 1.0f);
    EXPECT_FLOAT_EQ(id.m[2][2], 1.0f);
    EXPECT_FLOAT_EQ(id.m[3][3], 1.0f);
}

TEST_F(TransformTest, TranslateFloats) {
    Transform t = identity.translate(1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(t.m[0][3], 1.0f);
    EXPECT_FLOAT_EQ(t.m[1][3], 2.0f);
    EXPECT_FLOAT_EQ(t.m[2][3], 3.0f);
}

TEST_F(TransformTest, TranslateVector) {
    Vector translation{5.0f, 6.0f, 7.0f};
    Transform t = identity.translate(translation);
    EXPECT_FLOAT_EQ(t.m[0][3], 5.0f);
    EXPECT_FLOAT_EQ(t.m[1][3], 6.0f);
    EXPECT_FLOAT_EQ(t.m[2][3], 7.0f);
}

TEST_F(TransformTest, ScaleFloats) {
    Transform t = identity.scale(2.0f, 3.0f, 4.0f);
    EXPECT_FLOAT_EQ(t.m[0][0], 2.0f);
    EXPECT_FLOAT_EQ(t.m[1][1], 3.0f);
    EXPECT_FLOAT_EQ(t.m[2][2], 4.0f);
}

TEST_F(TransformTest, ScaleVector) {
    Vector scale{2.0f, 3.0f, 4.0f};
    Transform t = identity.scale(scale);
    EXPECT_FLOAT_EQ(t.m[0][0], 2.0f);
    EXPECT_FLOAT_EQ(t.m[1][1], 3.0f);
    EXPECT_FLOAT_EQ(t.m[2][2], 4.0f);
}

TEST_F(TransformTest, RotateX) {
    float angle = M_PI / 2.0f;  // 90 degrees
    Transform t = identity.rotateX(angle);
    
    // Apply to unitY should give unitZ
    Vector result = unitY.applyTransform(t);
    EXPECT_NEAR(result.x, 0.0f, 1e-6);
    EXPECT_NEAR(result.y, 0.0f, 1e-6);
    EXPECT_NEAR(result.z, 1.0f, 1e-6);
}

TEST_F(TransformTest, RotateY) {
    float angle = M_PI / 2.0f;  // 90 degrees
    Transform t = identity.rotateY(angle);
    
    // Apply to unitZ should give unitX
    Vector result = unitZ.applyTransform(t);
    EXPECT_NEAR(result.x, 1.0f, 1e-6);
    EXPECT_NEAR(result.y, 0.0f, 1e-6);
    EXPECT_NEAR(result.z, 0.0f, 1e-6);
}

TEST_F(TransformTest, RotateZ) {
    float angle = M_PI / 2.0f;  // 90 degrees
    Transform t = identity.rotateZ(angle);
    
    // Apply to unitX should give unitY
    Vector result = unitX.applyTransform(t);
    EXPECT_NEAR(result.x, 0.0f, 1e-6);
    EXPECT_NEAR(result.y, 1.0f, 1e-6);
    EXPECT_NEAR(result.z, 0.0f, 1e-6);
}

TEST_F(TransformTest, RotateAxis) {
    float angle = M_PI / 2.0f;  // 90 degrees
    Transform t = identity.rotateAxis(angle, unitZ);
    
    // Apply to unitX should give unitY (rotation around Z)
    Vector result = unitX.applyTransform(t);
    EXPECT_NEAR(result.x, 0.0f, 1e-6);
    EXPECT_NEAR(result.y, 1.0f, 1e-6);
    EXPECT_NEAR(result.z, 0.0f, 1e-6);
}

TEST_F(TransformTest, Multiplication) {
    Transform t1 = identity.translate(1.0f, 0.0f, 0.0f);
    Transform t2 = identity.translate(0.0f, 2.0f, 0.0f);
    Transform combined = t1 * t2;
    
    EXPECT_FLOAT_EQ(combined.m[0][3], 1.0f);
    EXPECT_FLOAT_EQ(combined.m[1][3], 2.0f);
    EXPECT_FLOAT_EQ(combined.m[2][3], 0.0f);
}

TEST_F(TransformTest, MultiplyEquals) {
    Transform t1 = identity.translate(1.0f, 0.0f, 0.0f);
    Transform t2 = identity.translate(0.0f, 2.0f, 0.0f);
    t1 *= t2;
    
    EXPECT_FLOAT_EQ(t1.m[0][3], 1.0f);
    EXPECT_FLOAT_EQ(t1.m[1][3], 2.0f);
}

TEST_F(TransformTest, Transpose) {
    Transform t = identity.translate(1.0f, 2.0f, 3.0f);
    Transform transposed = t.transpose();
    
    // m[0][3] should become m[3][0]
    EXPECT_FLOAT_EQ(transposed.m[3][0], 1.0f);
    EXPECT_FLOAT_EQ(transposed.m[3][1], 2.0f);
    EXPECT_FLOAT_EQ(transposed.m[3][2], 3.0f);
}

TEST_F(TransformTest, IndexOperator) {
    Transform t = identity.translate(1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(t[0][3], 1.0f);
    EXPECT_FLOAT_EQ(t[1][3], 2.0f);
    EXPECT_FLOAT_EQ(t[2][3], 3.0f);
}

TEST_F(TransformTest, GetTranslate) {
    Transform t = identity.translate(5.0f, 6.0f, 7.0f);
    Vector translation = t.getTranslate();
    EXPECT_FLOAT_EQ(translation.x, 5.0f);
    EXPECT_FLOAT_EQ(translation.y, 6.0f);
    EXPECT_FLOAT_EQ(translation.z, 7.0f);
}

TEST_F(TransformTest, Invert) {
    // Test that invert produces a valid matrix
    Transform t = identity.scale(2.0f, 2.0f, 2.0f);
    Transform inverted = t.invert();
    
    // For a scale matrix, inverse should have reciprocal values on diagonal
    EXPECT_NEAR(inverted.m[0][0], 0.5f, 1e-5);
    EXPECT_NEAR(inverted.m[1][1], 0.5f, 1e-5);
    EXPECT_NEAR(inverted.m[2][2], 0.5f, 1e-5);
}

TEST_F(TransformTest, Determinant) {
    // Identity matrix has determinant 1
    EXPECT_FLOAT_EQ(identity.determinant(), 1.0f);
    
    // Scale by 2 in all axes should give determinant 8
    Transform t = identity.scale(2.0f, 2.0f, 2.0f);
    EXPECT_FLOAT_EQ(t.determinant(), 8.0f);
}

TEST_F(TransformTest, ToString) {
    std::string str = identity.toString();
    EXPECT_FALSE(str.empty());
}

TEST_F(TransformTest, AssignmentOperator) {
    Transform t1 = identity.translate(1.0f, 2.0f, 3.0f);
    Transform t2;
    t2 = t1;
    
    EXPECT_FLOAT_EQ(t2.m[0][3], 1.0f);
    EXPECT_FLOAT_EQ(t2.m[1][3], 2.0f);
    EXPECT_FLOAT_EQ(t2.m[2][3], 3.0f);
}
