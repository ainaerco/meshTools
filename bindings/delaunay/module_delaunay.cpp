#include <delaunay/delaunay.h>
#include <geometry/vector.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace meshTools {
namespace Delaunay {

void export_delaunay_module(nb::module_ &m) {
    nb::class_<Delaunay>(m, "Delaunay",
                         "3D Delaunay tetrahedralization built incrementally "
                         "from a point set.")
        .def(
            nb::init<const std::vector<Geometry::Vector> &, float>(),
            "vertices"_a, "max"_a,
            "Build from list of Vector and max value for bounding tetrahedron.")
        .def_prop_ro(
            "orig_vertices",
            [](const Delaunay &d) {
                const auto &v = d.getOrigVertices();
                nb::list L;
                for (const auto &vec : v)
                    L.append(vec);
                return L;
            },
            "Original input vertices.")
        .def_prop_ro(
            "vertices",
            [](const Delaunay &d) {
                const auto &v = d.getVertices();
                nb::list L;
                for (const auto &vec : v)
                    L.append(vec);
                return L;
            },
            "All vertices (bounding + input).")
        .def_prop_ro(
            "tetras",
            [](const Delaunay &d) {
                auto tetras = d.getTetras();
                nb::list L;
                for (const auto &t : tetras) {
                    nb::list tri;
                    for (int i : t)
                        tri.append(i);
                    L.append(tri);
                }
                return L;
            },
            "Tetrahedra as list of 4-tuples of vertex indices.");
}

} // namespace Delaunay
} // namespace meshTools

NB_MODULE(_delaunay, m) { meshTools::Delaunay::export_delaunay_module(m); }
