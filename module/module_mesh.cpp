

#include <boost/python/object.hpp>
#include <boost/python.hpp>
#include <boost/python/overloads.hpp>

#include <module/pyUtils.h>
#include <mesh/Mesh.h>

using namespace boost::python;

void exportMesh()
{
    class_<meshTools::Mesh::Mesh>("Mesh", init<>() )
        //.def("selectGroups",  &meshTools::Mesh::Mesh::selectGroups)
        //.def("selectConvert", &meshTools::Mesh::Mesh::selectConvert)
        .add_property("verts",&meshTools::Mesh::Mesh::verts)
    ;

}

void exportVert()
{
    class_<meshTools::Mesh::Vert>("Vert", init<>() )
        .def("computeNormal",&meshTools::Mesh::Vert::computeNormal)
    ;

}

BOOST_PYTHON_MODULE(_mesh)
{
    exportVert();
    exportMesh();
    
    to_python_converter<std::vector<meshTools::Mesh::Vert*>, meshTools::stdVectorToPythonList<meshTools::Mesh::Vert*> >();
    meshTools::stdVectorFromPythonList<meshTools::Mesh::Vert*>();
    

}


