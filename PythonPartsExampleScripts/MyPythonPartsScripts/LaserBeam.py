"""
Script for the usage of the CreatePolyhedron function
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


print('Load LaserBeam.py')

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = CreatePolyhedron(doc)

    return element.create(build_ele)

def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """
    build_ele.change_property(handle_prop, input_pnt)
    return create_element(build_ele, doc)

class CreatePolyhedron():
    """
    Definition of class CreatePolyhedron
    """

    def __init__(self, doc):
        """
        Initialisation of class CreatePolyhedron

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self._length = build_ele.Path4Y1.value
        self._height = build_ele.z5.value
        self._width = build_ele.x4.value / 2
        self._hole_height = build_ele.hole_height.value
        self._hole_depth = build_ele.hole_depth.value
        self._rotation_angle = build_ele.rotation_angle.value

        self.create_polyhedron(build_ele)
        self.create_handles()

        return (self.model_ele_list, self.handle_list)


    def create_polyhedron(self, build_ele):
        """
        Create the polyhedron by a 2D base polygon, a reference point and a path

        Args:
            build_ele:  the building element.
        """

        if not build_ele.Polyhedron4.value:
            return

        #----------------- create the base polygon

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, 0, 0)
        base_pol += AllplanGeo.Point3D((self._width+160), 0, 0)
        base_pol += AllplanGeo.Point3D((self._width+160), 0, 153.)
        base_pol += AllplanGeo.Point3D(self._width, 0, 313.)
        base_pol += AllplanGeo.Point3D(self._width, 0, self._height)
        base_pol += AllplanGeo.Point3D((self._width+220), 0, (self._height+220))
        base_pol += AllplanGeo.Point3D((self._width+220), 0, (self._height+220+55))
        base_pol += AllplanGeo.Point3D((self._width+160), 0, (self._height+220+55))
        base_pol += AllplanGeo.Point3D((self._width+160), 0, (self._height+220+55+45))
        base_pol += AllplanGeo.Point3D(-(self._width+160), 0, (self._height+220+55+45))
        base_pol += AllplanGeo.Point3D(-(self._width+160), 0, (self._height+220+55))
        base_pol += AllplanGeo.Point3D(-(self._width+220), 0, (self._height+220+55))
        base_pol += AllplanGeo.Point3D(-(self._width+220), 0, (self._height+220))
        base_pol += AllplanGeo.Point3D(-(self._width), 0, self._height)
        base_pol += AllplanGeo.Point3D(-(self._width), 0, 313.)
        base_pol += AllplanGeo.Point3D(-(self._width+160), 0, 153.)
        base_pol += AllplanGeo.Point3D(-(self._width+160), 0, 0)
        base_pol += AllplanGeo.Point3D(0,0,0)

        if not GeometryValidate.is_valid(base_pol):
            return

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_ele.Color4.value
        com_prop.Stroke = 2


        #----------------- create the path

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, self._length, 0)
        path += AllplanGeo.Point3D(0, 0, 0)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if not GeometryValidate.polyhedron(err):
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, base_pol))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, path))
            return
        com_prop.Stroke = 1

        hole1_cyl = AllplanGeo.Cylinder3D(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-(self._width), self._hole_depth, self._hole_height),
                                       AllplanGeo.Vector3D(0, 0, 1),
                                       AllplanGeo.Vector3D(1, 0, 0)),
            45.5, 45.5,
            AllplanGeo.Point3D(0, 0, self._width*2))

        hole2_cyl = AllplanGeo.Cylinder3D(
        AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-(self._width), (self._length - self._hole_depth), self._hole_height),
                                AllplanGeo.Vector3D(0, 0, 1),
                                AllplanGeo.Vector3D(1, 0, 0)),
        45.5, 45.5,
        AllplanGeo.Point3D(0, 0, self._width*2))

        err, hole1_poly = AllplanGeo.CreatePolyhedron(hole1_cyl, 100)
        print(err)
        err, hole2_poly = AllplanGeo.CreatePolyhedron(hole2_cyl, 100)
        print(err)
        
        err, poly_sub = AllplanGeo.MakeSubtraction(polyhedron, hole1_poly)
        print(err)
        err, poly_sub = AllplanGeo.MakeSubtraction(poly_sub, hole2_poly)
        print(err)

        angle = AllplanGeo.Angle() 
        angle.Deg = self._rotation_angle
        rotation_axis = AllplanGeo.Axis3D(AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0),
                                      AllplanGeo.Point3D(0, 0, 1)
                                      ))
        poly_sub = AllplanGeo.Rotate(poly_sub, rotation_axis, angle)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, poly_sub))

    def create_handles(self):
        """
        Create the column handles
        """

        #------------------ Define handles
        origin = AllplanGeo.Point3D(0, 0, 0)

        length = AllplanGeo.Point3D(0, self._length, 0)
        height = AllplanGeo.Point3D(0, 0, self._height)
        width = AllplanGeo.Point3D(self._width, 0, 0)

        hole = AllplanGeo.Point3D(0, self._hole_depth, self._hole_height)

        handle1 = HandleProperties("Length",
                                   length,
                                   origin,
                                   [("Path4Y1", HandleDirection.y_dir)],
                                   HandleDirection.y_dir,
                                   True)

        self.handle_list.append(handle1)

        handle2 = HandleProperties("Height",
                                   height,
                                   origin,
                                   [
                                    ("z5", HandleDirection.z_dir)
                                    ],
                                   HandleDirection.z_dir,
                                   True)
        self.handle_list.append(handle2)
        
        handle3 = HandleProperties("Width",
                                   width,
                                   origin,
                                   [
                                    ("x4", HandleDirection.x_dir),
                                    ],
                                   HandleDirection.x_dir,
                                   True)
        self.handle_list.append(handle3)

        handle4 = HandleProperties("Hole",
                                   hole,
                                   origin,
                                   [
                                    ("hole_height", HandleDirection.z_dir),
                                    ("hole_depth", HandleDirection.y_dir),
                                    ],
                                   HandleDirection.yz_dir,
                                   True)
        self.handle_list.append(handle4)
