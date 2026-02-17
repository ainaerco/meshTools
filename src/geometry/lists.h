#ifndef _MESHTOOLS_LIST_H
#define _MESHTOOLS_LIST_H

#include <iterator>
#include <vector>

namespace meshTools {
namespace Geometry {

template <class T> class List : public std::vector<T> {
  public:
    T group_duplicates(List<T> l);
    unsigned int find(T item);
};

template <class T> T List<T>::group_duplicates(List<T> l) {}

template <class T> unsigned int List<T>::find(T item) {
    typename List<T>::iterator h = std::find(this->begin(), this->end(), item);

    return -1;
}

} // namespace Geometry
} // namespace meshTools

#endif