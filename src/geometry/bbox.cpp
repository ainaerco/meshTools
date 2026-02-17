#include <cstring>
#include <geometry/bbox.h>
#include <geometry/math.h>
#include <geometry/transform.h>
#include <iostream>
namespace meshTools {
namespace Geometry {

void Bbox::fromPointSet(std::vector<Vector> pointset) {
    std::vector<Vector> sorted_pointset;
    sorted_pointset = sortedVectorArray(pointset, 0);
    min.x = sorted_pointset.front().x;
    max.x = sorted_pointset.back().x;
    sorted_pointset = sortedVectorArray(pointset, 1);
    min.y = sorted_pointset.front().y;
    max.y = sorted_pointset.back().y;
    sorted_pointset = sortedVectorArray(pointset, 2);
    min.z = sorted_pointset.front().z;
    max.z = sorted_pointset.back().z;
    calcCenter();
}
void swap(float first[3], float second[3]) { std::swap(first, second); }
void Bbox::obbFromPointSet(std::vector<Vector> pointset) {
    Vector means;
    size_t pointset_size = pointset.size();
    for (size_t i = 0; i < pointset_size; i++) {
        means += pointset[i];
    }
    means /= static_cast<float>(pointset_size);
    float m[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
    float mc[3][3];
    float factor;
    m[2][2] = 1;
    for (int x = 0; x < 3; x++)
        for (int y = 0; y < 3; y++) {
            for (int i = 0; i < pointset_size; i++) {
                m[x][y] +=
                    (means[x] - pointset[i][x]) * (means[y] - pointset[i][y]);
            }
            m[x][y] /= pointset_size;
        }
    float a, b, c, d;
    a = -1;
    b = m[0][0] + m[1][1] + m[2][2];
    c = -m[0][0] * m[1][1] - m[0][0] * m[2][2] - m[1][1] * m[2][2] +
        m[0][1] * m[1][0] + m[1][2] * m[2][1] + m[0][2] * m[2][0];
    d = m[0][0] * m[1][1] * m[2][2] - m[0][1] * m[1][0] * m[2][2] -
        m[1][2] * m[2][1] * m[0][0] - m[0][2] * m[2][0] * m[1][1] +
        m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1];
    Vector roots = math::solveCubic(a, b, c, d);
    for (int i = 0; i < 3; i++) {
        memcpy(&mc, &m, sizeof(m));
        mc[0][0] -= roots[i];
        mc[1][1] -= roots[i];
        mc[2][2] -= roots[i];

        /*std::cout<<"\n";
        std::cout<<"1\n";
        std::cout<<mc[0][0]<<" "<<mc[0][1]<<" "<<mc[0][2]<<"\n";
        std::cout<<mc[1][0]<<" "<<mc[1][1]<<" "<<mc[1][2]<<"\n";
        std::cout<<mc[2][0]<<" "<<mc[2][1]<<" "<<mc[2][2]<<"\n";
        std::cout<<"\n";*/

        if (mc[0][0] == 0) {
            swap(mc[0], mc[2]);
        } else {
            factor = mc[2][0] / mc[0][0];
            mc[2][0] += -mc[0][0] * factor;
            mc[2][1] += -mc[0][1] * factor;
            mc[2][2] += -mc[0][2] * factor;
        }

        if (mc[0][0] == 0) {
            swap(mc[0], mc[1]);
        } else {
            factor = mc[1][0] / mc[0][0];
            mc[1][0] += -mc[0][0] * factor;
            mc[1][1] += -mc[0][1] * factor;
            mc[1][2] += -mc[0][2] * factor;
        }

        if (mc[1][1] == 0) {
            swap(mc[1], mc[2]);
        } else {
            factor = mc[2][1] / mc[1][1];
            mc[2][0] += -mc[1][0] * factor;
            mc[2][1] += -mc[1][1] * factor;
            mc[2][2] += -mc[1][2] * factor;
        }

        axis[i] = Vector(mc[0]).cross(Vector(mc[1])).normalize();
    }
    axis[2] = axis[0].cross(axis[1]);

    min = Vector(0, 0, 0);
    max = Vector(0, 0, 0);
    for (size_t i = 0; i < pointset_size; i++) {

        const Vector &v =
            Vector(axis[0].dot(pointset[i]), axis[1].dot(pointset[i]),
                   axis[2].dot(pointset[i]));
        if (i == 0) {
            max = v;
            min = v;
            continue;
        }
        min.x = std::min(min.x, v.x);
        min.y = std::min(min.y, v.y);
        min.z = std::min(min.z, v.z);
        max.x = std::max(max.x, v.x);
        max.y = std::max(max.y, v.y);
        max.z = std::max(max.z, v.z);

        // std::cout << "p" << v << "\n";
    }
    center = (min + max) * 0.5;
    const Vector &rt = Vector(axis[0].x, axis[1].x, axis[2].x);
    const Vector &ru = Vector(axis[0].y, axis[1].y, axis[2].y);
    const Vector &rf = Vector(axis[0].z, axis[1].z, axis[2].z);
    center = Vector(center.dot(rt), center.dot(ru), center.dot(rf));
    // std::cout << "min" << min << "\n";
    // std::cout << "max" << max << "\n";
}

void Bbox::calcCenter() {
    center.x = (min.x + max.x) / 2;
    center.y = (min.y + max.y) / 2;
    center.z = (min.z + max.z) / 2;
}

} // namespace Geometry
} // namespace meshTools