#include "curves.h"

#include <boost/array.hpp>
#include <boost/python/object.hpp>
#include <boost/python.hpp>
#include <boost/python/overloads.hpp>
#include <boost/python/return_internal_reference.hpp>

template <class T>
struct vectorToPyList
{
	static PyObject* convert(std::vector<T> const& vectorToConvert)
	{
		boost::python::list convertedList;
		for (unsigned int i = 0; i < vectorToConvert.size(); ++i)
		{
			convertedList.append(vectorToConvert.at(i));
		}

		return boost::python::incref(convertedList.ptr());
	}
};

template <class T>
struct vectorFromPyList
{
	vectorFromPyList()
	{
		boost::python::converter::registry::push_back(
			&convertible,
			&construct,
			boost::python::type_id< std::vector<T> >());
	}

	static void* convertible(PyObject* obj_ptr)
	{
		if (!PyList_Check(obj_ptr)) return 0;
		return obj_ptr;
	}

	static void construct(
		PyObject* obj_ptr,
		boost::python::converter::rvalue_from_python_stage1_data* data)
	{
		using namespace boost::python;

		extract<list> x(obj_ptr);
		if (!x.check()) throw_error_already_set();

		list l = x();

		void* storage = (
			(converter::rvalue_from_python_storage< std::vector<T> >*)
			data)->storage.bytes;
		new (storage)std::vector<T>();

		std::vector<T>& v = *reinterpret_cast<std::vector<T>*>(storage);

		for (int idx = 0; idx < len(l); ++idx)
		{
			extract<T> ext(l[idx]);
			if (!ext.check())
			{
				v.std::vector<T>::~vector();
				throw_error_already_set();
			}

			v.push_back(ext());
		}

		data->convertible = storage;
	}
};

void exportBezier()
{
	using namespace boost::python;

	class_<curves::Bezier>("Bezier")
		.def(init<>())
		.def(init<std::vector<float> >())
		.def("interpolate", &curves::Bezier::interpolate)
		;
}

void exportLagrange()
{
	using namespace boost::python;

	class_<curves::Lagrange>("Lagrange")
		.def(init<>())
		.def(init<std::vector<float> >())
		.def("interpolate", &curves::Lagrange::interpolate)
		;
}

void exportSpline()
{
	using namespace boost::python;
	class_<curves::Spline>("Spline")
		.def(init<>())
		.def(init<std::vector<float> >())
		.def("interpolate", &curves::Spline::interpolate)
		;
}

BOOST_PYTHON_MODULE(pybezier)
{
 	exportBezier();
 	exportLagrange();
 	exportSpline();
 	boost::python::to_python_converter<std::vector<float>, vectorToPyList<float> >();
 	vectorFromPyList<float>();

}
