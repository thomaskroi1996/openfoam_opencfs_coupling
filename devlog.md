- UpdateResults() never calls UpdateResult() because actContext.functor is false
  BUT
  only the case for first acouPressure on internal, all other regions work, also second acouPressure on internal has actContext.functor, see:

we are in UpdateResults() for loop of ResultHandler.cc, line 251
result: acouPressure
actContext.functor: 0
actContext.result: internal
UR: name = acouPressure dofs 1

---

we are in UpdateResults() for loop of ResultHandler.cc, line 251
result: acouPressure
actContext.functor: 0x5555635b0d50
actContext.result: prop
UR: name = acouPressure dofs 1

---

we are in UpdateResults() for loop of ResultHandler.cc, line 251
result: acouPressure
actContext.functor: 0x5555635b0d50
actContext.result: internal
UR: name = acouPressure dofs 1

- This leads to WARNING: Result acouPressure not provided on internal.

- in SimOutputHDF5.cc -> somehow code gets stuck there and crashes then. (tries to access vector of size 0 at index 0)

- From here: figure out why we have 2 times acouPressure on internal? maybe XML issue?
