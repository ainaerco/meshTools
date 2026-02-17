#include <cstddef>

#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <nanobind/stl/vector.h>

#include <geometry/bbox.h>
#include <geometry/math.h>
#include <geometry/polygon.h>
#include <geometry/ray.h>
#include <geometry/transform.h>
#include <geometry/vector.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace meshTools {
namespace Geometry {

template <class T, class B> static T getitem(const B &v, size_t index) {
    return v[index];
}

// Expose Bbox::axis (Vector[3]) as a std::vector for Python indexing
static std::vector<Vector> bbox_axis(const Bbox &b) {
    return {b.axis[0], b.axis[1], b.axis[2]};
}

void export_geometry_module(nb::module_ &m) {
    // Math functions
    m.def("epsilonTest", &math::epsilonTest, "value"_a, "test"_a = 0.0f,
          "eps"_a = 0.000001f, "Floating-point equality test");
    m.def("pointInPoly", &math::pointInPoly);
    m.def("interpolateBezier", &math::interpolateBezier);
    m.def("interpolateCatmullRom", &math::interpolateCatmullRom);
    m.def("lerp", &math::lerp);
    m.def("solveCubic", &math::solveCubic);
    m.def("fit", &math::fit);
    m.def("getBarycentric", &math::getBarycentric);
    m.def("sortedVectorArray", &sortedVectorArray);

    // Vector
    nb::class_<Vector>(m, "Vector")
        .def(nb::init<>())
        .def(nb::init<std::vector<float>>())
        .def(nb::init<float, float, float>())
        .def("toList", &Vector::toList)
        .def("__repr__", &Vector::toString)
        .def("setLength", &Vector::setLength)
        .def("normalize", &Vector::normalize)
        .def("isNull", &Vector::isNull)
        .def("lengthSquared", &Vector::lengthSquared)
        .def("length", &Vector::length)
        .def("zeroTest", &Vector::zeroTest)
        .def("angle", &Vector::angle)
        .def("dot", &Vector::dot)
        .def("cross", &Vector::cross)
        .def("lerp", &Vector::lerp)
        .def("slerp", &Vector::slerp)
        .def("project", &Vector::project)
        .def("reflect", &Vector::reflect)
        .def("rotateAround", &Vector::rotateAround)
        .def("applyTransform", &Vector::applyTransform)
        .def("__getitem__", &getitem<float, Vector>)
        .def_prop_rw(
            "x", [](const Vector &v) { return v.x; },
            [](Vector &v, float x) { v.x = x; })
        .def_prop_rw(
            "y", [](const Vector &v) { return v.y; },
            [](Vector &v, float y) { v.y = y; })
        .def_prop_rw(
            "z", [](const Vector &v) { return v.z; },
            [](Vector &v, float z) { v.z = z; })
        .def(nb::self + nb::self)
        .def(nb::self += nb::self)
        .def(nb::self - nb::self)
        .def(nb::self -= nb::self)
        .def(nb::self * float())
        .def(nb::self *= float())
        .def(float() * nb::self)
        .def(nb::self / float())
        .def(nb::self == nb::self)
        .def(nb::self != nb::self);

    // Ray
    nb::class_<Ray>(m, "Ray")
        .def(nb::init<Vector, Vector>())
        .def("pointPlaneSide", &Ray::pointPlaneSide)
        .def("pointDistance", &Ray::pointDistance)
        .def("intersectRayLine", &Ray::intersectRayLine)
        .def_prop_ro("origin", [](const Ray &r) { return r.origin; })
        .def_prop_ro("direction", [](const Ray &r) { return r.direction; });

    // Polygon
    nb::class_<Polygon>(m, "Polygon")
        .def(nb::init<const std::vector<Vector> &, std::vector<int>, Vector>())
        .def("triangulate", &Polygon::triangulate);

    // BBox
    nb::class_<Bbox>(m, "BBox")
        .def(nb::init<>())
        .def(nb::init<Vector, Vector>())
        .def(nb::init<Vector, Vector, Vector>())
        .def("fromPointSet", &Bbox::fromPointSet)
        .def("obbFromPointSet", &Bbox::obbFromPointSet)
        .def("calcCenter", &Bbox::calcCenter)
        .def("__getitem__", &getitem<Vector, Bbox>)
        .def_prop_ro("axis", &bbox_axis)
        .def_prop_ro("min", [](const Bbox &b) { return b.min; })
        .def_prop_ro("max", [](const Bbox &b) { return b.max; })
        .def_prop_ro("center", [](const Bbox &b) { return b.center; });

    // Transform
    nb::class_<Transform>(m, "Transform")
        .def(nb::init<>())
        .def(nb::init<Vector, Vector>())
        .def(nb::init<Vector, Vector, Vector>())
        .def("lookAt", &Transform::lookAt)
        .def("translate",
             static_cast<Transform (Transform::*)(const float &, const float &,
                                                  const float &) const>(
                 &Transform::translate))
        .def("translate",
             static_cast<Transform (Transform::*)(const Vector &) const>(
                 &Transform::translate))
        .def("scale",
             static_cast<Transform (Transform::*)(const Vector &) const>(
                 &Transform::scale))
        .def("scale", static_cast<Transform (Transform::*)(
                          const float &, const float &, const float &) const>(
                          &Transform::scale))
        .def("identity", &Transform::identity)
        .def("invert", &Transform::invert)
        .def("transpose", &Transform::transpose)
        .def("scaleLocal", &Transform::scaleLocal)
        .def("rotateX", &Transform::rotateX)
        .def("rotateY", &Transform::rotateY)
        .def("rotateZ", &Transform::rotateZ)
        .def("rotateAxis", &Transform::rotateAxis)
        .def("getEuler", &Transform::getEuler)
        .def("getTranslate", &Transform::getTranslate)
        .def("__str__", &Transform::toString)
        .def(nb::self *= nb::self)
        .def(nb::self * nb::self)
        .def_prop_ro("m", [](const Transform &t) {
            nb::list rows;
            for (int i = 0; i < 4; ++i) {
                nb::list row;
                for (int j = 0; j < 4; ++j)
                    row.append(t.m[i][j]);
                rows.append(row);
            }
            return rows;
        });
}

} // namespace Geometry
} // namespace meshTools

NB_MODULE(_geometry, m) { meshTools::Geometry::export_geometry_module(m); }
