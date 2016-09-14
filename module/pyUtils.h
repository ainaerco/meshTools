#include <boost/python.hpp>
#include <vector>

namespace meshTools
{
    
template <class T>
struct array3ToPythonList
{
        static PyObject* convert( T const& array)
        {
                boost::python::list convertedList;
                for(unsigned int i = 0; i < 3; ++i)
                {
                        convertedList.append(array[i]);
                }

                return boost::python::incref(convertedList.ptr());
        }
};

////////////////////////////////////////////////////////////////////////////////////
/// Structures for std::vector to convert from/to python::list object
template <class T>
struct stdVectorToPythonList
{
        static PyObject* convert(std::vector<T> const& vectorToConvert)
        {
                boost::python::list convertedList;
                for(size_t i = 0; i < vectorToConvert.size(); ++i)
                {
                        convertedList.append(vectorToConvert.at(i));
                }

                return boost::python::incref(convertedList.ptr());
        }
};

template <class T>
struct stdVectorFromPythonList
{
    stdVectorFromPythonList()
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
            new (storage) std::vector<T>();

            std::vector<T>& v = *reinterpret_cast< std::vector<T>* >(storage);

            for (size_t idx = 0; idx < static_cast<size_t>(len(l)); ++idx)
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
////////////////////////////////////////////////////////////////////////////////////

}