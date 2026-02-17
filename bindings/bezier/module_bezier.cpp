#include <cstddef>
#include <cstdint>

#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

#include "curves.h"

namespace nb = nanobind;

void exportBezierModule(nb::module_ &m) {
    nb::class_<curves::Bezier>(m, "Bezier")
        .def(nb::init<>())
        .def(nb::init<std::vector<float>>())
        .def("interpolate", &curves::Bezier::interpolate);

    nb::class_<curves::Lagrange>(m, "Lagrange")
        .def(nb::init<>())
        .def(nb::init<std::vector<float>>())
        .def("interpolate", &curves::Lagrange::interpolate);

    nb::class_<curves::Spline>(m, "Spline")
        .def(nb::init<>())
        .def(nb::init<std::vector<float>>())
        .def("interpolate", &curves::Spline::interpolate);
}

NB_MODULE(_bezier, m) { exportBezierModule(m); }
