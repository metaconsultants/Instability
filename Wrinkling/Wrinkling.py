# -*- coding: mbcs -*-
#
# 
# copyright - metaengineeringconsultants@gmail.com
# 
# Parameters
X = 1.0
#L = 10*X
#Bs = 0.75*X
#Bf = X/20
Hf = 0.05*X
Hi = 0.55*X
Hs = 0.45*X
L = 10*X
H = Hs+Hi+Hf
H1 = Hs + Hi


Es = 1
Ef = 1E2
Ei = 1
Nu = 0.475
E = Es + Ef + Ei

# Abaqus library
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=200,  height=100)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)

# Parts library
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=10)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)

s.rectangle(point1=(0.0, H), point2=(L, 0.0))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()

f = p.faces
t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

s.Line(point1=(0, Hs), point2=(L, Hs))
s.HorizontalConstraint(entity=g[6], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[6], addUndoState=False)
s.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
s.CoincidentConstraint(entity1=v[5], entity2=g[5], addUndoState=False)

s.Line(point1=(0, H1), point2=(L, H1))
s.HorizontalConstraint(entity=g[7], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[7], addUndoState=False)
s.CoincidentConstraint(entity1=v[6], entity2=g[3], addUndoState=False)
s.CoincidentConstraint(entity1=v[7], entity2=g[5], addUndoState=False)

pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
s.unsetPrimaryObject()

# Material Assignment
 

# film    
mdb.models['Model-1'].Material(name='film')
mdb.models['Model-1'].materials['film'].Elastic(table=((Ef, Nu), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='film', 
    material='film', thickness=None)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(faces=faces, name='Set-1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='film', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)    
    
# substrate       
mdb.models['Model-1'].Material(name='substrate')
mdb.models['Model-1'].materials['substrate'].Elastic(table=((Es, Nu), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='substrate', 
    material='substrate', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(name='substrate', 
    material='substrate', thickness=None)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
region = p.Set(faces=faces, name='Set-2')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='substrate', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)  
    
# intermediate       
mdb.models['Model-1'].Material(name='intermediate')
mdb.models['Model-1'].materials['intermediate'].Elastic(table=((Ei, Nu), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='intermediate', 
    material='intermediate', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(name='intermediate', 
    material='intermediate', thickness=None)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#4 ]', ), )
region = p.Set(faces=faces, name='Set-3')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='intermediate', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)      
 
#Assembly 
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a2 = mdb.models['Model-1'].rootAssembly
a2.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a2.Instance(name='Part-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
#BUCKLE    
#mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=10, vectors=8)
#mdb.models['Model-1'].steps['Step-1'].setValues(maxIterations=1000)
#RIKS    
mdb.models['Model-1'].StaticRiksStep(name='Step-1', previous='Initial', initialArcInc=0.01, nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    
# meshing
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#7 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=0.05, deviationFactor=0.4, minSizeFactor=0.1)
elemType1 = mesh.ElemType(elemCode=CPE4R, elemLibrary=STANDARD, 
    hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#8 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=8, constraint=FINER)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#200 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=10, constraint=FINER)
f = p.faces
pickedEdges = e.getSequenceFromMask(mask=('[#4 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=400, constraint=FINER)
faces = f.getSequenceFromMask(mask=('[#7 ]', ), )
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()  

# BC
a3 = mdb.models['Model-1'].rootAssembly
e1 = a3.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#228 ]', ), )
region = a3.Set(edges=edges1, name='Set-1')
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
    region=region, u1=0.0, u2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

a3 = mdb.models['Model-1'].rootAssembly
e1 = a3.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#40 ]', ), )
region = a3.Set(edges=edges1, name='Set-2')
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=UNSET, u2=0.0, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)
 
a3 = mdb.models['Model-1'].rootAssembly
e1 = a3.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#182 ]', ), )
region = a3.Set(edges=edges1, name='Set-3')
mdb.models['Model-1'].DisplacementBC(name='BC-3', createStepName='Step-1', 
    region=region, u1=-2.0, u2=0, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)
    
# interaction (to avoid self contact)   
mdb.models['Model-1'].ContactProperty('IntProp-1')
mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
#: The interaction property "IntProp-1" has been created.
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
region=a.Surface(side1Edges=side1Edges1, name='Surf-1')
mdb.models['Model-1'].SelfContactStd(name='Int-1', createStepName='Step-1', 
    surface=region, interactionProperty='IntProp-1', thickness=ON)  
    
#Job submission
mdb.Job(name='wrinkling_finite', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
mdb.jobs['wrinkling_finite'].setValues(numCpus=8, numDomains=8)   
#mdb.jobs['wrinkling_finite'].submit(consistencyChecking=OFF)     
