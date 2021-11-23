# -*- coding: mbcs -*-
#
# copyright - metaengineeringconsultants@gmail.com
# how to do bulging simulation ?
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=260.6875, 
    height=126.414352416992)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
mdb.saveAs(pathName='C:/temp/cylinder_bulging')
#: The model database has been saved to "C:\temp\cylinder_bulging.cae".
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, 4.5))
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, 5.0))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=100.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=168.214, 
    farPlane=274.374, width=126.769, height=61.4799, viewOffsetX=7.06207, 
    viewOffsetY=-1.34766)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Hyperelastic(
    materialType=ISOTROPIC, testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA, table=((1.0, 0.0), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='Material-1', thickness=None)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=170.175, 
    farPlane=272.413, width=113.319, height=54.9569, viewOffsetX=9.93733, 
    viewOffsetY=0.913316)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=176.752, 
    farPlane=265.836, width=68.2719, height=33.1102, viewOffsetX=15.2017, 
    viewOffsetY=7.26939)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
v1, e, d1 = p.vertices, p.edges, p.datums
p.PartitionCellByPlaneThreePoints(point1=v1[2], point2=v1[0], point3=v1[1], 
    cells=pickedCells)
session.viewports['Viewport: 1'].view.setValues(nearPlane=177.032, 
    farPlane=265.556, width=58.9891, height=28.6083, viewOffsetX=15.7768, 
    viewOffsetY=8.13754)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
v2, e1, d2 = p.vertices, p.edges, p.datums
p.PartitionCellByPlaneThreePoints(cells=pickedCells, point1=p.InterestingPoint(
    edge=e1[10], rule=MIDDLE), point2=p.InterestingPoint(edge=e1[15], 
    rule=MIDDLE), point3=p.InterestingPoint(edge=e1[14], rule=MIDDLE))
session.viewports['Viewport: 1'].view.setValues(nearPlane=163.362, 
    farPlane=279.225, width=158.505, height=76.8708, viewOffsetX=-12.3734, 
    viewOffsetY=0.884426)
mdb.save()
#: The model database has been saved to "C:\temp\cylinder_bulging.cae".
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=164.87, 
    farPlane=277.717, width=149.593, height=72.5488, viewOffsetX=22.747, 
    viewOffsetY=-0.408381)
mdb.models['Model-1'].StaticRiksStep(name='Step-1', previous='Initial', 
    maxNumInc=1000, initialArcInc=0.01, maxArcInc=1.0, nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=162.259, 
    farPlane=280.328, width=167.796, height=81.3767, viewOffsetX=34.4426, 
    viewOffsetY=4.41614)
session.viewports['Viewport: 1'].view.setValues(nearPlane=189.449, 
    farPlane=330.981, width=195.913, height=95.0131, cameraPosition=(109.055, 
    129.297, -150.636), cameraUpVector=(-0.9097, -0.350028, -0.223443), 
    cameraTarget=(15.3434, 45.7715, 31.6067), viewOffsetX=40.2142, 
    viewOffsetY=5.15616)
session.viewports['Viewport: 1'].view.setValues(nearPlane=209.486, 
    farPlane=310.944, width=38.3095, height=18.5791, viewOffsetX=42.7819, 
    viewOffsetY=33.7783)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#c5258 ]', ), )
e1 = a.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#80000000 ]', ), )
region = a.Set(edges=edges1, faces=faces1, name='Set-1')
mdb.models['Model-1'].PinnedBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=202.07, 
    farPlane=318.359, width=89.373, height=43.3437, viewOffsetX=37.4472, 
    viewOffsetY=21.5973)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=146.358, 
    farPlane=257.622, width=38.8656, height=18.8489, viewOffsetX=3.24305, 
    viewOffsetY=-2.43818)
session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
del mdb.models['Model-1'].boundaryConditions['BC-1']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-1']
mdb.models['Model-1'].PinnedBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].view.setValues(nearPlane=180.492, 
    farPlane=262.095, width=42.5217, height=20.622, viewOffsetX=-16.5853, 
    viewOffsetY=-12.487)
session.viewports['Viewport: 1'].view.setValues(nearPlane=185.826, 
    farPlane=297.863, width=43.7784, height=21.2314, cameraPosition=(-36.316, 
    73.8237, 277.515), cameraUpVector=(-0.661841, 0.468574, -0.585154), 
    cameraTarget=(-8.06157, 9.21177, 67.7579), viewOffsetX=-17.0754, 
    viewOffsetY=-12.856)
session.viewports['Viewport: 1'].view.setValues(nearPlane=176.909, 
    farPlane=306.781, width=106.299, height=51.5526, viewOffsetX=-17.8799, 
    viewOffsetY=-12.769)
session.viewports['Viewport: 1'].view.setValues(nearPlane=177.945, 
    farPlane=311.019, width=106.922, height=51.8544, cameraPosition=(5.72655, 
    38.4152, 291.482), cameraUpVector=(-0.37517, 0.799866, -0.468467), 
    cameraTarget=(6.96696, 3.25859, 73.0015), viewOffsetX=-17.9846, 
    viewOffsetY=-12.8438)
session.viewports['Viewport: 1'].view.setValues(nearPlane=182, 
    farPlane=306.964, width=75.4431, height=36.588, viewOffsetX=-13.9333, 
    viewOffsetY=-9.67033)
session.viewports['Viewport: 1'].view.setValues(nearPlane=187.542, 
    farPlane=311.728, width=77.7406, height=37.7022, cameraPosition=(-17.3719, 
    -19.9154, 298.346), cameraUpVector=(-0.346335, 0.88924, -0.298838), 
    cameraTarget=(4.63497, -2.14989, 78.8659), viewOffsetX=-14.3576, 
    viewOffsetY=-9.96482)
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.493, 
    farPlane=310.778, width=73.4469, height=35.6199, viewOffsetX=-6.42648, 
    viewOffsetY=-4.97277)
session.viewports['Viewport: 1'].view.setValues(nearPlane=187.767, 
    farPlane=310.434, width=73.1639, height=35.4827, cameraPosition=(10.9798, 
    0.943445, 298.996), cameraUpVector=(-0.304744, 0.891731, -0.334584), 
    cameraTarget=(8.62172, -0.166945, 77.7167), viewOffsetX=-6.40172, 
    viewOffsetY=-4.95361)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#28120 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=1.0)
session.viewports['Viewport: 1'].view.setValues(width=77.836, height=37.7485, 
    viewOffsetX=-4.7593, viewOffsetY=-5.29453)
session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
session.viewports['Viewport: 1'].view.setValues(nearPlane=171.148, 
    farPlane=271.44, width=107.129, height=51.9551, viewOffsetX=2.29739, 
    viewOffsetY=-2.59708)
mdb.save()
#: The model database has been saved to "C:\temp\cylinder_bulging.cae".
session.viewports['Viewport: 1'].view.setValues(nearPlane=180.592, 
    farPlane=261.995, width=37.1139, height=17.9993, viewOffsetX=-20.9284, 
    viewOffsetY=-13.3197)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-1']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=UNSET, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
mdb.save()
#: The model database has been saved to "C:\temp\cylinder_bulging.cae".
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=8, 
    numDomains=8, numGPUs=0)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=147.82, 
    farPlane=256.16, width=28.6911, height=13.965, viewOffsetX=3.77161, 
    viewOffsetY=-1.40764)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
session.viewports['Viewport: 1'].view.setValues(nearPlane=169.265, 
    farPlane=273.322, width=106.501, height=51.8377, viewOffsetX=-19.5912, 
    viewOffsetY=-5.0599)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=2.5, deviationFactor=0.1, minSizeFactor=0.1)
session.viewports['Viewport: 1'].view.setValues(nearPlane=174.281, 
    farPlane=268.306, width=75.6489, height=36.821, viewOffsetX=-21.6673, 
    viewOffsetY=-12.2333)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
session.viewports['Viewport: 1'].view.setValues(nearPlane=169.016, 
    farPlane=273.571, width=120.846, height=58.8198, viewOffsetX=0.943127, 
    viewOffsetY=-18.7838)
elemType1 = mesh.ElemType(elemCode=C3D8RH, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#f ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
session.viewports['Viewport: 1'].view.setValues(nearPlane=183.286, 
    farPlane=259.301, width=23.1746, height=11.2799, viewOffsetX=-27.5534, 
    viewOffsetY=-14.4842)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#6 ]', ), )
p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#80 ]', ), )
p.seedEdgeBySize(edges=pickedEdges, size=4.0, deviationFactor=0.1, 
    minSizeFactor=0.1, constraint=FINER)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
session.viewports['Viewport: 1'].view.setValues(nearPlane=184.019, 
    farPlane=258.569, width=16.0514, height=7.81277, viewOffsetX=-27.3427, 
    viewOffsetY=-15.9651)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#6 ]', ), )
p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#80 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)
session.viewports['Viewport: 1'].view.setValues(nearPlane=184.015, 
    farPlane=258.573, width=18.1654, height=8.84176, viewOffsetX=-26.5316, 
    viewOffsetY=-16.3004)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
session.viewports['Viewport: 1'].view.setValues(nearPlane=181.81, 
    farPlane=260.778, width=35.5941, height=17.3249, viewOffsetX=-20.7259, 
    viewOffsetY=-16.6527)
mdb.save()
#: The model database has been saved to "C:\temp\cylinder_bulging.cae".
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.models['Model-1'].steps['Step-1'].setValues(maxNumInc=70)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
mdb.Job(name='cylinder-bulging', model='Model-1', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=8, 
    numDomains=8, numGPUs=0)
mdb.jobs['cylinder-bulging'].submit(consistencyChecking=OFF)
