import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.mel import eval as meval
from mesh_maya_tube import MayaTube

kPluginNodeTypeName = "tubeDeformer"

tubeDeformerId = OpenMaya.MTypeId(0x0020A52C)


class tubeDeformer(OpenMayaMPx.MPxNode):
	# class variables
	#firsttime == 1

	segments = OpenMaya.MObject()
	circleSegments = OpenMaya.MObject()
	
	curve =  OpenMaya.MObject()
	profileScale = OpenMaya.MObject()
	profileRotate = OpenMaya.MObject()
	taper = OpenMaya.MObject()
	twist = OpenMaya.MObject()
	growth = OpenMaya.MObject()
	profile  = OpenMaya.MObject()
	#output =  OpenMaya.MObject()
	outputMesh = OpenMaya.MObject()
	fixType = OpenMaya.MObject()
	cap = OpenMaya.MObject()
	scaleCorners = OpenMaya.MObject()
	evenDistribute = OpenMaya.MObject()
	reverse = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
	
	def compute(self,plug,dataBlock):
		if plug == tubeDeformer.outputMesh:
			segmentsHandle = dataBlock.inputValue( self.segments )
			segmentsValue = segmentsHandle.asInt()

			circleSegmentsHandle = dataBlock.inputValue( self.circleSegments )
			circleSegmentsValue = circleSegmentsHandle.asInt()
			if circleSegmentsValue<2: circleSegmentsValue=0

			fixHandle = dataBlock.inputValue( self.fixType )
			fixValue = fixHandle.asInt()

			capHandle = dataBlock.inputValue( self.cap )
			capValue = capHandle.asShort()
			scaleCornersHandle = dataBlock.inputValue( self.scaleCorners )
			scaleCornersValue = scaleCornersHandle.asShort()
			evenDistributeHandle = dataBlock.inputValue( self.evenDistribute )
			evenDistributeValue = evenDistributeHandle.asShort()
			reverseHandle = dataBlock.inputValue( self.reverse )
			reverseValue = reverseHandle.asShort()

			profileScaleHandle = dataBlock.inputValue( self.profileScale )
			profileScaleValue = profileScaleHandle.asDouble()

			profileRotateHandle = dataBlock.inputValue( self.profileRotate )
			profileRotateValue = profileRotateHandle.asDouble()

			taperHandle = dataBlock.inputValue( self.taper )
			taperValue = taperHandle.asDouble()

			twistHandle = dataBlock.inputValue( self.twist )
			twistValue = twistHandle.asDouble()

			growthHandle = dataBlock.inputValue( self.growth )
			growthValue = growthHandle.asDouble()

			curveHandle = dataBlock.inputValue( self.curve )
			curveObject = curveHandle.asNurbsCurve()
			curve_fn = OpenMaya.MFnNurbsCurve(curveObject)

			profileHandle = dataBlock.inputValue( self.profile )

			
			
			if profileHandle.data().hasFn(OpenMaya.MFn.kMesh):
				profileObject = profileHandle.asMesh()
				profile_fn = OpenMaya.MFnMesh(profileObject)
				circleSegmentsValue = 0
			elif profileHandle.data().hasFn(OpenMaya.MFn.kNurbsCurve):
				profileObject = profileHandle.asNurbsCurve()
				profile_fn = OpenMaya.MFnNurbsCurve(profileObject)
				circleSegmentsValue = 0
			else:
				profile_fn = 0
				circleSegmentsValue = max(circleSegmentsValue,2)
			outputHandle = dataBlock.outputValue(self.outputMesh)
			dataCreator = OpenMaya.MFnMeshData()
			newOutputData = dataCreator.create()

			tube = MayaTube(curveFn = curve_fn, scale = profileScaleValue, profileFn = profile_fn, parent= newOutputData, scale_corners = 1-scaleCornersValue,\
			segments=segmentsValue, cylinder_segments= circleSegmentsValue, fix =fixValue, rotate = profileRotateValue,taper = taperValue,twist = twistValue,\
			cap = capValue, even = evenDistributeValue, growth = growthValue, reverse = reverseValue)

			outputHandle.setMObject(newOutputData)
			dataBlock.setClean(plug)
		else:
			return OpenMaya.kUnknownParameter



def nodeCreator():
	return OpenMayaMPx.asMPxPtr( tubeDeformer() )

# initializer
def nodeInitializer():
	gAttr = OpenMaya.MFnGenericAttribute()
	
	tubeDeformer.profile = gAttr.create( "profile", "prof")
	gAttr.addDataAccept( OpenMaya.MFnData.kMesh )
	gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
	gAttr.setHidden(False)
	
	tubeDeformer.curve = gAttr.create( "curve", "curve")
	gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
	gAttr.setHidden(False)
	
	
	nAttr = OpenMaya.MFnNumericAttribute()
	
	tubeDeformer.profileScale = nAttr.create( "profileScale", "psc", OpenMaya.MFnNumericData.kDouble, 1.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(4)
	
	tubeDeformer.profileRotate = nAttr.create( "profileRotate", "prot", OpenMaya.MFnNumericData.kDouble, 0.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(360)

	tubeDeformer.twist = nAttr.create( "profileTwist", "twist", OpenMaya.MFnNumericData.kDouble, 0.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(360)
	
	tubeDeformer.taper = nAttr.create( "profileTaper", "taper", OpenMaya.MFnNumericData.kDouble, 0.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(1)

	tubeDeformer.growth = nAttr.create( "growth", "g", OpenMaya.MFnNumericData.kDouble, 1.0)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setMin(0)
	nAttr.setMax(1)

	tubeDeformer.segments = nAttr.create( "segments", "segs", OpenMaya.MFnNumericData.kInt, 2)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setMin(3)
	nAttr.setSoftMax(10)

	tubeDeformer.circleSegments = nAttr.create( "circleSegments", "circlesegs", OpenMaya.MFnNumericData.kInt, 8)
	nAttr.setKeyable(True)
	nAttr.setStorable(True)
	nAttr.setMin(1)
	nAttr.setSoftMax(16)

	tubeDeformer.fixType = nAttr.create( "fixType", "fix", OpenMaya.MFnNumericData.kInt, 0)
	nAttr.setMin(0)
	nAttr.setMax(3)
	

	#mAttr = OpenMaya.MFnMatrixAttribute()
	
	#tubeDeformer.profileMatrix = mAttr.create("profileMatrix", "profmatr", OpenMaya.MFnNumericData.kFloat )
	#mAttr.setHidden(True)
	
	rAttr = OpenMaya.MRampAttribute()
	
	tubeDeformer.profileRamp = rAttr.createCurveRamp("profileRamp", "pr")
	
	eAttr = OpenMaya.MFnEnumAttribute()
	
	tubeDeformer.cap = eAttr.create("cap", "cap", 0)
	eAttr.addField("off", 0);
	eAttr.addField("on", 1);
	eAttr.setHidden(False);
	eAttr.setStorable(True);

	tubeDeformer.scaleCorners = eAttr.create("scaleCorners", "sc", 0)
	eAttr.addField("off", 0);
	eAttr.addField("on", 1);
	eAttr.setHidden(False);
	eAttr.setStorable(True);

	tubeDeformer.evenDistribute = eAttr.create("even", "ev", 0)
	eAttr.addField("off", 0);
	eAttr.addField("on", 1);
	eAttr.setHidden(False);
	eAttr.setStorable(True);

	tubeDeformer.reverse = eAttr.create("reverse", "rv", 0)
	eAttr.addField("off", 0);
	eAttr.addField("on", 1);
	eAttr.setHidden(False);
	eAttr.setStorable(True);

	

	typedAttr = OpenMaya.MFnTypedAttribute()
	tubeDeformer.outputMesh = typedAttr.create("outputMesh", "out", OpenMaya.MFnData.kMesh)
	# add attribute

	tubeDeformer.addAttribute( tubeDeformer.profile )
	tubeDeformer.addAttribute( tubeDeformer.curve )
	tubeDeformer.addAttribute( tubeDeformer.profileScale )
	tubeDeformer.addAttribute( tubeDeformer.profileRotate )
	tubeDeformer.addAttribute( tubeDeformer.taper )
	tubeDeformer.addAttribute( tubeDeformer.twist )
	tubeDeformer.addAttribute( tubeDeformer.growth )
	tubeDeformer.addAttribute( tubeDeformer.segments )
	tubeDeformer.addAttribute( tubeDeformer.fixType )
	#tubeDeformer.addAttribute( tubeDeformer.profileMatrix )
	tubeDeformer.addAttribute( tubeDeformer.profileRamp )
	tubeDeformer.addAttribute( tubeDeformer.cap )
	tubeDeformer.addAttribute( tubeDeformer.scaleCorners )
	tubeDeformer.addAttribute( tubeDeformer.evenDistribute )
	tubeDeformer.addAttribute( tubeDeformer.reverse )
	tubeDeformer.addAttribute( tubeDeformer.circleSegments )
	tubeDeformer.addAttribute( tubeDeformer.outputMesh )
	
	
	tubeDeformer.attributeAffects( tubeDeformer.curve, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.profile, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.profileScale, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.profileRotate, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.taper, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.twist, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.growth, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.segments, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.circleSegments, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.fixType, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.cap, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.scaleCorners, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.evenDistribute, tubeDeformer.outputMesh )
	tubeDeformer.attributeAffects( tubeDeformer.reverse, tubeDeformer.outputMesh )
			

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Zhekichan", "0.0.1", "Any")
	try:
		mplugin.registerNode( kPluginNodeTypeName, tubeDeformerId, nodeCreator, nodeInitializer )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( tubeDeformerId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )

mel = '''
global proc tubeDeformer()
{
	string $sel[] = `ls -sl -tr`;
	if (size($sel)==2)
	{
		string $curve = $sel[0];
		string $profile = $sel[1];
		string $curveshape[] = `listRelatives -s $curve`;
		string $profileshape[] = `listRelatives -s $profile`;
		//string $tubedeformer[] = `deformer -typ "tubeDeformer" -n "tubeDeformer" $profile`;
		string $tubedeformer = `createNode "tubeDeformer"`;
		

		connectAttr -f ($curveshape[0]+".worldSpace[0]") ($tubedeformer+".curve");
		string $get = `objectType $profileshape[0]`;
		if($get=="nurbsCurve")
		{
			connectAttr -f ($profileshape[0]+".worldSpace[0]") ($tubedeformer+".profile");
		}
		if($get=="mesh")
		{
			connectAttr -f ($profileshape[0]+".worldMesh[0]") ($tubedeformer+".profile");
		}
		string $outMesh = `createNode mesh`;
		connectAttr -f ($tubedeformer+".outputMesh") ($outMesh+".inMesh");

		sets -e -fe "initialShadingGroup" $outMesh;
	}
	else
	{
		//error "please select curve and profile: first curve then the mesh that should be deformed.";
		string $curve = $sel[0];
		string $curveshape[] = `listRelatives -s $curve`;
		string $tubedeformer = `createNode "tubeDeformer"`;
		connectAttr -f ($curveshape[0]+".worldSpace[0]") ($tubedeformer+".curve");
		string $outMesh = `createNode mesh`;
		connectAttr -f ($tubedeformer+".outputMesh") ($outMesh+".inMesh");
		setAttr ($tubedeformer+".circleSegments") 8;
		sets -e -fe "initialShadingGroup" $outMesh;
	}
}


	global proc AEtubeDeformerNew( string $attributeName1, string $attributeName2, string $attributeName3, string $attributeName4) {
		checkBoxGrp -numberOfCheckBoxes 1 -label "Cap holes" capctr;
		checkBoxGrp -numberOfCheckBoxes 1 -label "Don't scale corners" zupactr;
		checkBoxGrp -numberOfCheckBoxes 1 -label "Even distribution" evenctr;
		checkBoxGrp -numberOfCheckBoxes 1 -label "Reverse" reversectr;
		
		connectControl -index 2 capctr ($attributeName1);
		connectControl -index 2 zupactr ($attributeName2);
		connectControl -index 2 evenctr ($attributeName3);
		connectControl -index 2 reversectr ($attributeName4);
	}

	global proc AEtubeDeformerReplace( string $attributeName1, string $attributeName2, string $attributeName3, string $attributeName4) {
		connectControl -index 2 capctr ($attributeName1);
		connectControl -index 2 zupactr ($attributeName2);
		connectControl -index 2 evenctr ($attributeName3);
		connectControl -index 2 reversectr ($attributeName4);
	}

	global proc AEtubeDeformerTemplate( string $nodeName )
	{
		// the following controls will be in a scrollable layout
		editorTemplate -beginScrollLayout;

			// add a bunch of common properties
			editorTemplate -beginLayout "Tube Deformer Attributes" -collapse 0;
				editorTemplate -callCustom "AEtubeDeformerNew" "AEtubeDeformerReplace" "cap" "scaleCorners" "even" "reverse";
				editorTemplate -addSeparator;
				editorTemplate -addControl  "profileScale" ;
				editorTemplate -addControl  "profileRotate" ;
				editorTemplate -addControl  "twist" ;
				editorTemplate -addControl  "taper" ;
				editorTemplate -addControl  "segments" ;
				editorTemplate -addControl  "fixType" ;
				editorTemplate -addControl  "circleSegments" ;
				editorTemplate -addControl  "growth" ;
				
				//AEaddRampControl "profileRamp" ;
				
			editorTemplate -endLayout;

			// include/call base class/node attributes
			AEdependNodeTemplate $nodeName;

			// add any extra attributes that have been added
			editorTemplate -addExtraControls;

		editorTemplate -endScrollLayout;
	}
'''
meval( mel )