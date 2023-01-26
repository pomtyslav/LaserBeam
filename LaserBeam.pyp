<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>MyPythonPartsScripts\LaserBeam.py</Name>
        <Title>CreatePolyhedron1</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Dimensions</Text>

        <Parameter>
            <Name>Color4</Name>
            <Text>Color</Text>
            <Value>22</Value>
            <ValueType>Color</ValueType>
        </Parameter>

        <Parameter>
            <Name>Path4Y1</Name>
            <Text>Length</Text>
            <Value>12000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>x4</Name>
            <Text>Width</Text>
            <Value>160.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>z5</Name>
            <Text>Height</Text>
            <Value>780.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>Separator4_1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>hole_height</Name>
            <Text>Hole Height</Text>
            <Value>450</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>hole_depth</Name>
            <Text>Hole Depth</Text>
            <Value>350</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator4_1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>rotation_angle</Name>
            <Text>Rotation Angle</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator4_1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>Polyhedron4</Name>
            <Text>Create polyhedron</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>