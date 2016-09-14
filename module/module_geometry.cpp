#include <boost/array.hpp>
#include <boost/python/object.hpp>
#include <boost/python.hpp>
#include <boost/python/overloads.hpp>
#include <boost/python/return_internal_reference.hpp>

#include <geometry/math.h>
#include <geometry/Ray.h>
#include <geometry/Vector.h>
#include <geometry/Bbox.h>
#include <geometry/Transform.h>
#include <geometry/Polygon.h>
#include <module/pyUtils.h>
namespace meshTools
{
namespace Geometry
{

BOOST_PYTHON_FUNCTION_OVERLOADS(zeroTest_overloads, math::epsilonTest, 1, 3);

void exportMath()
{
	using namespace boost::python;
	
	def("epsilonTest", math::epsilonTest,
					zeroTest_overloads(
						args("value", "test", "eps"), "This is zeroTest's docstring"
					));
	def("pointInPoly", &math::pointInPoly);
	def("interpolateBezier", &math::interpolateBezier);
	def("interpolateCatmullRom", &math::interpolateCatmullRom);
	def("lerp",&math::lerp);
	def("solveCubic",&math::solveCubic);
	def("fit", &math::fit);
	def("min", &math::min);
	def("max", &math::max);
	def("getBarycentric", &math::getBarycentric);
}

template<class T, class B>
T getitem(B &v, size_t index)
{
	return v[index];
}
/*
template<typename Source>
static void vector_set(Source& self, const float val) { self.x= static_cast<float>(val); }
*/
void exportVector()
{
	using namespace boost::python;
	//def("sortVectorArray",&tfx::Geometry::sortVectorArray,return_internal_reference<>());
	def("sortedVectorArray",&sortedVectorArray);
	class_<Vector>("Vector")
		.def(init<>())
		.def(init< std::vector<float> >())
		.def(init< float, float, float >())
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
		.def(self + self)
		.def(self += self)
		.def(self - self)
		.def(self -= self)
		.def(self * float())
		.def(self *= float())
		.def(float() * self)
		.def(self / float())
		.def(self == self)
		.def(self != self)
		.def("__getitem__", &getitem<float,Vector>)
		.add_property("x",  &Vector::x,  &Vector::x)
		.add_property("y",  &Vector::y,  &Vector::y)
		.add_property("z",  &Vector::z,  &Vector::z)
	;
}

void exportRay()
{
	using namespace boost::python;
	
	class_<Ray>("Ray", init< Vector, Vector >())
		.def("pointPlaneSide", &Ray::pointPlaneSide)
		.def("pointDistance",  &Ray::pointDistance)
		//.def("segmentPlaneHit", &Ray::segmentPlaneHit)
		.def("intersectRayLine", &Ray::intersectRayLine)
		.add_property("origin", &Ray::origin)
		.add_property("direction", &Ray::direction)
	;
}

void exportPolygon()
{
	using namespace boost::python;
	
	class_<Polygon>("Polygon", init< const std::vector<Vector>&, std::vector<int>, Vector >())
		.def("triangulate", &Polygon::triangulate)
	;
}

void exportBbox()
{
	using namespace boost::python;
	
	class_<Bbox>("BBox")
		.def(init<>())
		.def(init<Vector, Vector>())
		.def(init<Vector, Vector, Vector>())
		.def("fromPointSet", &Bbox::fromPointSet)
		.def("obbFromPointSet", &Bbox::obbFromPointSet)
		.def("calcCenter", &Bbox::calcCenter)
		.def("__getitem__", &getitem<Vector,Bbox>)
		.add_property("axis",  &Bbox::axis)
		.add_property("min",  &Bbox::min)
		.add_property("max",  &Bbox::max)
		.add_property("center", &Bbox::center)
	;
}

Transform (Transform::*translate_float)(const float&,const float&,const float&)    = &Transform::translate;
Transform (Transform::*translate_Vector)(const Vector&)                 = &Transform::translate;
Transform (Transform::*scale_Vector) (const Vector&  v)                 = &Transform::scale;              
Transform (Transform::*scale_double) (const float &x,const float &y,const float &z) = &Transform::scale;  

void exportTransform()
{
	using namespace boost::python;
	
	class_<Transform>("Transform")
		.def(init<>())
		.def(init<Vector, Vector>())
		.def(init<Vector, Vector, Vector>())
		.def("lookAt", &Transform::lookAt)
        .def("translate", translate_float)
        .def("translate",translate_Vector)
        .def("scale", scale_Vector)
        .def("scale", scale_double)
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
		.def(self *= self)
		.def(self * self)
		//.def("__getitem__", &getitem<float,tfx::Geometry::Transform>)
		.add_property("m",  &Transform::m)
		//.add_property("mi", &tfx::Geometry::Transform::mi)
	;
}

BOOST_PYTHON_MODULE(_geometry)
{
	exportMath();
	exportVector();
	exportRay();
	exportBbox();
	exportTransform();
	exportPolygon();
	
	boost::python::to_python_converter<std::vector<int>, meshTools::stdVectorToPythonList<int> >();
	meshTools::stdVectorFromPythonList<int>();
	//boost::python::to_python_converter<std::vector<float>, meshTools::stdVectorToPythonList<float> >();
	//meshTools::stdVectorFromPythonList<float>();
	boost::python::to_python_converter<std::vector<Vector>, meshTools::stdVectorToPythonList<Vector> >();
	meshTools::stdVectorFromPythonList<Vector>();
    
    boost::python::to_python_converter< Vector[3], meshTools::array3ToPythonList< Vector[3] > >();
}

}
}
