
#include <cmath>
#include <sstream>
#include <geometry/math.h>
#include <geometry/vector.h>
#include <geometry/transform.h>

namespace meshTools
{
namespace Geometry
{

bool 
sortVectorArray(std::vector<Vector> &v,int axis)
{
	bool done = false;
	while(!done)
	{
		done = true;
		for(int i =0;i<v.size()-1;i++)
		{
			if(v[i][axis]>v[i+1][axis])
			{
				done = false;
				std::swap(v[i],v[i+1]);
			}
		}
	}
	return done;
}


std::vector<Vector> 
sortedVectorArray(std::vector<Vector> v,int axis)
{
	bool done = false;
	while(!done)
	{
		done = true;
		for(int i =0;i<v.size()-1;i++)
		{
			if(v[i][axis]>v[i+1][axis])
			{
				done = false;
				std::swap(v[i],v[i+1]);
			}
		}
	}
	return v;
}

Vector 
Vector::applyTransform(Transform t)
{
	float xp = t.m[0][0]*x+t.m[0][1]*y+t.m[0][2]*z+t.m[0][3];
	float yp = t.m[1][0]*x+t.m[1][1]*y+t.m[1][2]*z+t.m[1][3];
	float zp = t.m[2][0]*x+t.m[2][1]*y+t.m[2][2]*z+t.m[2][3];
	float wp = t.m[3][0]*x+t.m[3][1]*y+t.m[3][2]*z+t.m[3][3];
	if(wp==1)
	{return Vector(xp,yp,zp);}
	else
	{return Vector(xp,yp,zp)/wp;}
}

std::vector<float> 
Vector::toList()
{
	std::vector<float> ret;
	ret.push_back(x);
	ret.push_back(y);
	ret.push_back(z);
	return ret;
}

std::string 
Vector::toString()
{
	std::stringstream ss;
	ss << "[" << x << "," << y << ","  << z  << "]";
	return ss.str();
}

bool
Vector::isNull()
{
	return (x+y+z) == 0;
}

bool
Vector::zeroTest()
{
	return math::epsilonTest(x) && math::epsilonTest(y) && math::epsilonTest(z);
}

Vector
Vector::setLength(float length)
{
	return normalize()*length;
}

Vector
Vector::normalize()
{
	float l = length();
	if(l!=0)
	{
		return *this/length();
	}
	return Vector();
}

float 
Vector::lengthSquared()
{
	return x*x+y*y+z*z;
}

float 
Vector::length()
{
	return sqrt(lengthSquared());
}

float
Vector::angle(Vector other)
{
	float n1=length();
	float n2=other.length();
	if(n1==0||n2==0){return 0;}
	float costheta = dot(other)/(n1*n2);
	costheta = math::min(costheta,1);
	costheta = math::max(costheta,-1);
	return acos(costheta);
}

float
Vector::dot(const Vector& other)
{
	return x*other.x+y*other.y+z*other.z;
}

Vector
Vector::cross(const Vector& other)
{
	return Vector(y*other.z-z*other.y,z*other.x-x*other.z,x*other.y-y*other.x);
}

Vector 
Vector::lerp(Vector other, float factor)
{
	float beta = 1-factor;
	return Vector(beta*x+factor*other.x,beta*y+factor*other.y,beta*z+factor*other.z);
}

Vector 
Vector::slerp(Vector other, float factor)
{
	float theta = angle(other);
	if (math::epsilonTest(theta)){ return *this; }
	float s1 = sin((1-factor)*theta);
	float s2 = sin(factor*theta);
	float s3 = 1/sin(theta);
	return Vector((s1*x+s2*other.x)*s3,(s1*y+s2*other.y)*s3,(s1*z+s2*other.z)*s3);
}

Vector 
Vector::project(Vector other)
{
	Vector n = other.normalize();
	return dot(n)*n;
}

Vector 
Vector::reflect(Vector other)
{
	return 2*(dot(other)*other-*this);
}

Vector 
Vector::rotateAround(Vector axis,float angle)
{
	float r2 = axis.lengthSquared();
	float r = sqrt(r2);
	float ct = cos(angle);
	float st = sin(angle);
	float dt = dot(axis)*(1-ct)/r2;
	return Vector(axis.x*dt+x*ct+(-axis.z*y+axis.y*z)*st,axis.y*dt+y*ct+(axis.z*x-axis.x*z)*st,axis.z*dt+z*ct+(-axis.y*x+axis.x*y)*st);
}

}
}