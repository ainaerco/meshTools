#include "meshMaya.h"
#include <maya/MSelectionList.h>
#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>


namespace tfx
{
namespace MeshMaya
{
    
    
std::string 
test_geo(std::string dag)
{
    std::cout << dag << '\n';
    MString node(dag.c_str());
    MStatus stat; 
    MObject MObj;
    MSelectionList selList;
    selList.add(node,true);
    selList.getDependNode(0,MObj);
    MDagPath path;
    selList.getDagPath (0, path, MObj);
    
    
    std::cout << "Full path: " << path.fullPathName().asChar() << '\n';
 
    return std::string(path.fullPathName().asChar());
}


    
}    
}

