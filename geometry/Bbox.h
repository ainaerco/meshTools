#ifndef _MESHTOOLS_BBOX_H
#define _MESHTOOLS_BBOX_H

#include <geometry/Vector.h>

namespace meshTools
{
namespace Geometry
{

class Bbox
{
public:

	Bbox()	{	}
	Bbox(Vector mn,Vector mx)
	: min(mn),max(mx)
	{	}
	Bbox(Vector mn,Vector mx,Vector c)
	: min(mn),max(mx),center(c)
	{	}
	Vector min;
	Vector max;
	Vector center;
	Vector axis[3];
	void fromPointSet(std::vector<Vector> pointset);
	void obbFromPointSet(std::vector<Vector> pointset);
	void calcCenter();

	Vector operator[](const size_t& index) 
	{
		if (index==0){return min;}
		else if (index==1){return max;}
		else if (index==2){return center;}
		else {throw "Index out of range";}
	}
};

	
	
}
}


#endif 