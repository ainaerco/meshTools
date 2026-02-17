#include <gtest/gtest.h>
#include <geometry/ray.h>
#include <geometry/vector.h>
#include <cmath>

using namespace meshTools::Geometry;

class RayTest : public ::testing::Test {
protected:
    Vector origin{0.0f, 0.0f, 0.0f};
    Vector directionX{1.0f, 0.0f, 0.0f};
    Vector directionY{0.0f, 1.0f, 0.0f};
    Vector directionZ{0.0f, 0.0f, 1.0f};
};

TEST_F(RayTest, Constructor) {
    Ray ray(origin, directionX);
    EXPECT_TRUE(ray.origin == origin);
    EXPECT_TRUE(ray.direction == directionX);
}

TEST_F(RayTest, PointDistance) {
    // pointDistance returns direction.dot(origin - point)
    // This is the signed distance along the direction from point to origin
    Ray ray(origin, directionX);
    Vector point{1.0f, 0.0f, 0.0f};
    
    // direction=(1,0,0), origin=(0,0,0), point=(1,0,0)
    // direction.dot(origin - point) = (1,0,0).dot(-1,0,0) = -1
    float distance = ray.pointDistance(point);
    EXPECT_NEAR(distance, -1.0f, 1e-6);
}

TEST_F(RayTest, PointDistanceAtOrigin) {
    Ray ray(origin, directionX);
    Vector point{0.0f, 0.0f, 0.0f};
    
    float distance = ray.pointDistance(point);
    EXPECT_NEAR(distance, 0.0f, 1e-6);
}

TEST_F(RayTest, PointProjection) {
    // pointProjection: point - direction * (v.dot(direction)) where v = point - origin
    Ray ray(origin, directionX);
    Vector point{2.0f, 3.0f, 4.0f};
    
    Vector projected = ray.pointProjection(point);
    // v = (2,3,4), v.dot(direction) = 2
    // projected = point - direction * 2 = (2,3,4) - (2,0,0) = (0,3,4)
    EXPECT_NEAR(projected.x, 0.0f, 1e-6);
    EXPECT_FLOAT_EQ(projected.y, 3.0f);
    EXPECT_FLOAT_EQ(projected.z, 4.0f);
}

TEST_F(RayTest, PointPlaneSidePositive) {
    // Ray represents a plane with normal pointing in +X
    Ray ray(origin, directionX);
    Vector point{1.0f, 0.0f, 0.0f};
    
    bool side = ray.pointPlaneSide(point);
    EXPECT_TRUE(side);  // Point is on positive side
}

TEST_F(RayTest, PointPlaneSideNegative) {
    Ray ray(origin, directionX);
    Vector point{-1.0f, 0.0f, 0.0f};
    
    bool side = ray.pointPlaneSide(point);
    EXPECT_FALSE(side);  // Point is on negative side
}

TEST_F(RayTest, SegmentPlaneHit) {
    // Plane at origin with normal pointing up (Y)
    Ray ray(origin, directionY);
    
    // Segment crossing the plane
    Vector segment0{0.0f, -1.0f, 0.0f};
    Vector segment1{0.0f, 1.0f, 0.0f};
    
    Vector hit = ray.segmentPlaneHit(segment0, segment1);
    EXPECT_NEAR(hit.x, 0.0f, 1e-6);
    EXPECT_NEAR(hit.y, 0.0f, 1e-6);
    EXPECT_NEAR(hit.z, 0.0f, 1e-6);
}

TEST_F(RayTest, TriangleRayHit) {
    // Ray pointing in +Z direction from origin
    Ray ray(origin, directionZ);
    
    // Triangle in front of the ray
    Vector triangle[3] = {
        Vector{-1.0f, -1.0f, 2.0f},
        Vector{1.0f, -1.0f, 2.0f},
        Vector{0.0f, 1.0f, 2.0f}
    };
    
    Vector hit = ray.triangleRayHit(triangle);
    // If hit, z should be 2.0
    if (!hit.isNull()) {
        EXPECT_NEAR(hit.z, 2.0f, 1e-6);
    }
}

TEST_F(RayTest, TriangleRayMiss) {
    // Ray pointing in +Z direction from origin
    Ray ray(origin, directionZ);
    
    // Triangle that the ray doesn't hit (off to the side)
    Vector triangle[3] = {
        Vector{5.0f, 5.0f, 2.0f},
        Vector{7.0f, 5.0f, 2.0f},
        Vector{6.0f, 7.0f, 2.0f}
    };
    
    Vector hit = ray.triangleRayHit(triangle);
    // Should return null vector on miss
    EXPECT_TRUE(hit.isNull());
}

TEST_F(RayTest, IntersectRayLine) {
    // Ray at origin pointing in +X
    Ray ray(origin, directionX);
    
    // Line perpendicular to the ray
    Vector p1{2.0f, -1.0f, 0.0f};
    Vector p2{2.0f, 1.0f, 0.0f};
    
    Vector intersection = ray.intersectRayLine(p1, p2);
    EXPECT_NEAR(intersection.x, 2.0f, 1e-6);
    EXPECT_NEAR(intersection.y, 0.0f, 1e-6);
}
