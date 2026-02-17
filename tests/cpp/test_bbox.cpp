#include <gtest/gtest.h>
#include <geometry/bbox.h>
#include <geometry/vector.h>

using namespace meshTools::Geometry;

class BboxTest : public ::testing::Test {
protected:
    Vector minV{0.0f, 0.0f, 0.0f};
    Vector maxV{1.0f, 1.0f, 1.0f};
    Vector center{0.5f, 0.5f, 0.5f};
};

TEST_F(BboxTest, DefaultConstructor) {
    Bbox bbox;
    // Default constructed vectors should be zero
    EXPECT_FLOAT_EQ(bbox.min.x, 0.0f);
    EXPECT_FLOAT_EQ(bbox.min.y, 0.0f);
    EXPECT_FLOAT_EQ(bbox.min.z, 0.0f);
}

TEST_F(BboxTest, TwoVectorConstructor) {
    Bbox bbox(minV, maxV);
    EXPECT_TRUE(bbox.min == minV);
    EXPECT_TRUE(bbox.max == maxV);
}

TEST_F(BboxTest, ThreeVectorConstructor) {
    Bbox bbox(minV, maxV, center);
    EXPECT_TRUE(bbox.min == minV);
    EXPECT_TRUE(bbox.max == maxV);
    EXPECT_TRUE(bbox.center == center);
}

TEST_F(BboxTest, IndexOperator) {
    Bbox bbox(minV, maxV, center);
    EXPECT_TRUE(bbox[0] == minV);
    EXPECT_TRUE(bbox[1] == maxV);
    EXPECT_TRUE(bbox[2] == center);
}

TEST_F(BboxTest, IndexOperatorOutOfRange) {
    Bbox bbox(minV, maxV, center);
    EXPECT_THROW(bbox[3], const char*);
}

TEST_F(BboxTest, CalcCenter) {
    Bbox bbox(minV, maxV);
    bbox.calcCenter();
    EXPECT_FLOAT_EQ(bbox.center.x, 0.5f);
    EXPECT_FLOAT_EQ(bbox.center.y, 0.5f);
    EXPECT_FLOAT_EQ(bbox.center.z, 0.5f);
}

TEST_F(BboxTest, FromPointSet) {
    std::vector<Vector> points = {
        Vector{-1.0f, -2.0f, -3.0f},
        Vector{5.0f, 6.0f, 7.0f},
        Vector{0.0f, 0.0f, 0.0f},
        Vector{2.0f, 3.0f, 4.0f}
    };
    
    Bbox bbox;
    bbox.fromPointSet(points);
    
    EXPECT_FLOAT_EQ(bbox.min.x, -1.0f);
    EXPECT_FLOAT_EQ(bbox.min.y, -2.0f);
    EXPECT_FLOAT_EQ(bbox.min.z, -3.0f);
    EXPECT_FLOAT_EQ(bbox.max.x, 5.0f);
    EXPECT_FLOAT_EQ(bbox.max.y, 6.0f);
    EXPECT_FLOAT_EQ(bbox.max.z, 7.0f);
}

TEST_F(BboxTest, FromPointSetSinglePoint) {
    std::vector<Vector> points = {
        Vector{1.0f, 2.0f, 3.0f}
    };
    
    Bbox bbox;
    bbox.fromPointSet(points);
    
    EXPECT_FLOAT_EQ(bbox.min.x, 1.0f);
    EXPECT_FLOAT_EQ(bbox.min.y, 2.0f);
    EXPECT_FLOAT_EQ(bbox.min.z, 3.0f);
    EXPECT_FLOAT_EQ(bbox.max.x, 1.0f);
    EXPECT_FLOAT_EQ(bbox.max.y, 2.0f);
    EXPECT_FLOAT_EQ(bbox.max.z, 3.0f);
}

TEST_F(BboxTest, FromPointSetWithNegatives) {
    std::vector<Vector> points = {
        Vector{-5.0f, -5.0f, -5.0f},
        Vector{-1.0f, -1.0f, -1.0f}
    };
    
    Bbox bbox;
    bbox.fromPointSet(points);
    
    EXPECT_FLOAT_EQ(bbox.min.x, -5.0f);
    EXPECT_FLOAT_EQ(bbox.min.y, -5.0f);
    EXPECT_FLOAT_EQ(bbox.min.z, -5.0f);
    EXPECT_FLOAT_EQ(bbox.max.x, -1.0f);
    EXPECT_FLOAT_EQ(bbox.max.y, -1.0f);
    EXPECT_FLOAT_EQ(bbox.max.z, -1.0f);
}
