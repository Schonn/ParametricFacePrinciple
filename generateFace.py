import bpy
import random
import mathutils

def selectVerts(vertNumbers,addSelection):
    bpy.ops.object.mode_set(mode='EDIT')
    if(addSelection == False):
        bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    meshVertices = bpy.context.object.data.vertices
    for vertex in vertNumbers:
        meshVertices[vertex].select = True
    bpy.ops.object.mode_set(mode='EDIT') 
    
def getSelectedVertList():
    bpy.ops.object.mode_set(mode='OBJECT')
    meshVertices = bpy.context.object.data.vertices
    vertList = []
    for vertexNumber in range(len(meshVertices)):
        if(meshVertices[vertexNumber].select == True):
            vertList.append(vertexNumber)
    bpy.ops.object.mode_set(mode='EDIT')
    return vertList

def selectCreatedEdge(vertIndex,addSelection):
    selectVerts([vertIndex,vertIndex-1],addSelection)
    
def selectCreatedEdgeVertical(vertIndex,addSelection):
    selectVerts([vertIndex,vertIndex-2],addSelection)

def extrudeDirection(extrudeX,extrudeY,extrudeZ,overallScale):
    vertList = getSelectedVertList()
    vertIndex = vertList[0] + len(vertList)*2
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(extrudeX*overallScale,extrudeY*overallScale,extrudeZ*overallScale)})
    return vertIndex - 1

def extrudeMultiple(directionList,scaleList,rotateList,overallScale):
    vertIndex = 0
    for transformNumber in range(len(directionList)):
        vertIndex = extrudeDirection(directionList[transformNumber][0],directionList[transformNumber][1],directionList[transformNumber][2],overallScale)
        scaleAmount(scaleList[transformNumber][0],scaleList[transformNumber][1],scaleList[transformNumber][2])
        if(rotateList != None):
            rotateAmount(rotateList[transformNumber][0],rotateList[transformNumber][1],rotateList[transformNumber][2])
    return vertIndex

def moveDirection(moveX,moveY,moveZ,overallScale):
    bpy.ops.transform.translate(value=(moveX*overallScale,moveY*overallScale,moveZ*overallScale))

def scaleAmount(scaleX,scaleY,scaleZ):
    bpy.ops.transform.resize(value=(scaleX,scaleY,scaleZ))
    
def rotateAmount(rotateX,rotateY,rotateZ):
    bpy.ops.transform.rotate(value=rotateX, axis=(1,0,0))
    bpy.ops.transform.rotate(value=rotateY, axis=(0,1,0))
    bpy.ops.transform.rotate(value=rotateZ, axis=(0,0,1))

def createMeshForGeneration(planeSize):
    bpy.ops.mesh.primitive_plane_add(radius=planeSize)
    placeholderMesh = bpy.context.scene.objects.active
    placeholderMesh.name = "Generated"
    bpy.context.scene.update()
    bpy.ops.object.mode_set(mode='EDIT')
    
def selectAndFillVerts(vertList):
    for vertGroup in vertList:
        selectVerts(vertGroup,False)
        bpy.ops.mesh.edge_face_add()
        
def selectAndMergeVerts(vertList):
    selectVerts(vertList,False)
    bpy.ops.mesh.merge(type='CENTER')
    
def printVertsSelected():
    print(getSelectedVertList())
    
def cleanMesh():
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent()
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.uv.smart_project(angle_limit=89,island_margin=0.03)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.subdivision_set(level=1)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
def createBoneAtPosition(moveX,moveY,moveZ,overallScale,boneName):
    tweakingArmature = None
    if(bpy.context.object.type != 'ARMATURE'):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.armature_add()
        tweakingArmature = bpy.context.object
        bpy.ops.object.mode_set(mode='EDIT')
        tweakingArmature.show_x_ray = True
    else:
        bpy.ops.object.armature_add()
    bpy.ops.armature.select_more()
    bpy.ops.transform.translate(value=(moveX*overallScale,moveY*overallScale,moveZ*overallScale))
    bpy.context.selected_editable_bones[0].name = boneName
    
def selectAndTransformVerts(weightAndVertList,moveBy,scaleBy,rotateBy,overallScale):
    for weightVertSet in range(len(weightAndVertList)):
        vertSet = weightAndVertList[weightVertSet][1]
        weightAmount = weightAndVertList[weightVertSet][0]
        selectVerts(vertSet,False)
        moveDirection(moveBy[0]*weightAmount,moveBy[1]*weightAmount,moveBy[2]*weightAmount,overallScale)
        scaleAmount(1+(scaleBy[0]*weightAmount),1+(scaleBy[1]*weightAmount),1+(scaleBy[2]*weightAmount))
        rotateAmount(rotateBy[0]*weightAmount,rotateBy[1]*weightAmount,rotateBy[2]*weightAmount)

def genFace():
    sceneObjects = bpy.context.scene.objects
    #variable features
    overallScale = 0.5
    
    chinDown = 0
    chinForwards = 0
    chinWiden = 0
    jawNarrow = 0
    mouthCornerLeftUp = 0
    mouthCornerRightUp = 0
    mouthDown = 0
    lipTopWiden = 0
    lipBottomWiden = 0
    cheekFoldWiden = 0
    cheekForwardLeft = 0
    cheekForwardRight = 0
    noseForwards = 0
    noseWiden = 0
    noseDown = 0
    eyeLeftOut = 0
    eyeRightOut = 0
    upperLidLeftDown = 0
    upperLidRightDown = 0
    lowerLidLeftUp = 0
    lowerLidRightUp = 0
    browLeftUp = 0
    browRightUp = 0
    earLeftForwards = 0
    earRightForwards = 0
    earLeftHeight = 0
    earRightHeight = 0
    neckJoinLower = 0

    
    if(bpy.context.object != None):
        if(bpy.context.object.mode != 'OBJECT'):
            bpy.ops.object.mode_set(mode='OBJECT')
            if('Generated' in sceneObjects):
                sceneObjects['Generated'].select = True
            bpy.ops.object.delete(use_global=False)
    bpy.ops.object.delete(use_global=False)

    createMeshForGeneration(overallScale)
    scaleAmount(0.4,1,1)
    selectCreatedEdge(3,False)
    moveDirection(0,-2.6,2.5,overallScale)
    noScale = [1,1,1]
    noRotate = [0,0,0]
    #head outline
    directionList = [[0,-2,-0.2],[0,-0.8,0.7],[0,0,1],[0,0.3,0.7],[0,-0.5,0.5],[0,0,0.4], #bottom lip
                    [0,0.5,0.4],[0,0.4,-1.2],[0,0.1,0.3],[0,0.4,0],[0,0.1,-0.3],[0,0.6,-0.5],#bottom gum
                    [0,2,0],[0,-1,0.5],[0,-1.4,0],[0,-0.5,1],[0,2.5,0],[0,1,-0.7],[0,0,-2],[0,1,0],
                    [0,0,3.5],[0,-4,0],[0,-0.6,-0.2],[0,-0.1,-0.5],[0,-0.4,0],
                    [0,-0.1,0.5],[0,-0.2,-0.8],[0,-0.5,0.4],[0,0,0.4],[0,0.2,0.1],[0,0.2,0.6],
                    [0,-0.5,0],[0,-0.4,0.2],[0,-0.2,0.15],[0,-0.2,0.6],[0,0.4,0.4],[0,0.3,0.5],
                    [0,0.8,0.75],[0,0,0.3],[0,-0.3,0.6],[0,-0.1,0.6],[0,0.3,1.5],[0,0.8,2.7], #forehead
                    [0,2,1.2],[0,4.5,0],[0,3.6,-1],[0,1.2,-3.5],[0,0,-3],[0,-2,-3],[0,0,-1.5],[0,1,-4.6]]
    scaleList = [[2,1,1],noScale,noScale,[0.5,1,1],noScale,[1.5,1,1],
                    noScale,[0.5,1,1],noScale,noScale,noScale,noScale,
                    noScale,noScale,noScale,noScale,noScale,noScale,noScale,
                    noScale,noScale,[1.3,1,1],noScale,noScale,noScale,
                    noScale,noScale,noScale,noScale,[0.3,1,1],[2,1,1],
                    [0.6,1,1],[1.6,1,1],noScale,[2,1,1],[0.7,1,1],noScale,
                    noScale,noScale,[1.4,1,1],noScale,noScale,noScale,
                    noScale,[1.4,1,1],[1.4,1,1],noScale,noScale,noScale,
                    noScale,noScale]
    extrudeMultiple(directionList,scaleList,None,overallScale)
    #LEFT FACE SIDE
    #nose to chin loop
    selectCreatedEdgeVertical(77,False)
    directionList = [[0.5,0.9,-0.3],[0.8,0,-0.3],[1.2,0.3,-0.7],[0.3,0.7,-1],[0,0.2,-1.1],[-0.5,-0.3,-1.3]]
    scaleList = [noScale,noScale,[1,1,1.5],noScale,noScale,noScale]
    rotateList = [noRotate,[0.5,0.5,0.5],[0.4,0.8,0.7],[0.4,0.7,0.5],[0,-0.2,0],[0.4,1.4,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(9,True)
    bpy.ops.mesh.edge_face_add()
    #nose to cheek join
    selectCreatedEdgeVertical(71,False)
    directionList = [[0.2,0.2,0.1],[0.4,0.5,-0.1],[0,0.3,-0.1],[0.2,0.1,-0.5],[0.4,0.2,-0.3],[0.5,0.3,0.3]]
    scaleList = [noScale,[1.5,1.5,1],noScale,noScale,[1.5,1,1],[3,1,1]]
    rotateList = [[0,0,0.6],[0,0,1],noRotate,[0,0,0.3],[0,-1,0],[0.6,-0.7,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(112,True)
    bpy.ops.mesh.edge_face_add()
    #nose edge
    selectCreatedEdgeVertical(121,False)
    selectCreatedEdgeVertical(123,True)
    extrudeDirection(0.15,-0.1,0.5,overallScale)
    fillVertsList = [[130,119,71,73],
                    [73, 75, 106, 130],
                    [106, 130, 131, 132]]
    selectAndFillVerts(fillVertsList)
    #cheek crease
    selectCreatedEdgeVertical(108,False)
    extrudeDirection(0,0.2,-0.3,overallScale)
    selectAndMergeVerts([132,133])
    fillVertsList = [[108, 110, 129, 133],
                    [123, 125, 132, 133],
                    [125, 127, 129, 133],
                    [63, 65, 122, 124],
                    [65, 67, 120, 122],
                    [67, 69, 118, 120]]
    selectAndFillVerts(fillVertsList)
    selectVerts([122,65],True)
    extrudeDirection(-0.1,0.1,0.3,overallScale)
    rotateAmount(0.2,1.3,0)
    scaleAmount(1,0.7,1)
    #top lip
    selectCreatedEdgeVertical(61,False)
    directionList = [[0.5,0.2,0.1],[0.6,0.3,-0.4],[0.5,0.6,-0.1]]
    scaleList = [[1,1,1.1],[1,1,0.6],noScale]
    rotateList = [noRotate,noRotate,[0,-0.1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[112, 128, 144, 145],
                    [126, 128, 143, 145],
                    [124, 126, 141, 143],
                    [61, 63, 124, 141]]
    selectAndFillVerts(fillVertsList)
    #bottom lip
    selectCreatedEdgeVertical(15,False)
    directionList = [[0.5,0.3,0.1],[0.3,0.5,-0.1]]
    scaleList = [[1,1,0.6],[1,1,1.6]]
    rotateList = [[0,-0.4,0],[0,0.5,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[11, 13, 146, 148],
                    [9, 11, 116, 148],
                    [114, 116, 148, 149],
                    [112, 114, 144, 149]]
    selectAndFillVerts(fillVertsList)
    #eye socket
    selectCreatedEdgeVertical(81,False)
    directionList = [[0.2,0.5,-0.3],[0.3,0,0.1],[0,0.3,0],[0.3,0,0],[0.1,0.3,0],[0.3,0.1,0],[0.6,0.1,0],
                    [0.3,0.1,0.1],[0,-0.5,0],[0.3,0.2,0],[0.3,0.3,0],[0.4,0.6,0]]
    scaleList = [[1,1,2],[1,1,0.5],noScale,[1,1,1.5],noScale,[1,1,2.5],noScale,
                [1,1,0.2],noScale,noScale,[1,1,4],[1,1,2]]
    rotateList = [noRotate,noRotate,noRotate,noRotate,noRotate,noRotate,noRotate,
                noRotate,[0.7,0,0],noRotate,[-0.2,-0.3,0.3],[0.7,-0.3,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #upperlid
    selectCreatedEdgeVertical(155,False)
    directionList = [[0.3,0,0],[0.5,-0.3,0.3],[0.6,0.1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,[-0.5,0,0],[0,1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([157,175])
    fillVertsList = [[157, 159, 161, 176],
                    [161, 163, 176, 178],
                    [167, 169, 177, 178],
                    [163, 165, 167, 178]]
    selectAndFillVerts(fillVertsList)
    #lower lid
    selectCreatedEdgeVertical(154,False)
    directionList = [[0.3,0,0],[0.5,-0.1,-0.3],[0.6,0.1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,[0.3,0,0],[0,-1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([156, 180])
    fillVertsList = [[162, 164, 166, 183],
                    [160, 162, 181, 183],
                    [156, 158, 160, 181],
                    [166, 168, 182, 183]]
    selectAndFillVerts(fillVertsList)
    #upper lid and brow
    selectCreatedEdgeVertical(177,False)
    directionList = [[0,0.1,0.3],[-0.1+0.2,-0.6+0.2,0.1],[0.1,0,0.6],[0.1,0.4,1.8],[0.2-0.2,0.8,2],[0.3,2,1],
                    [1.1,3.5,-0.2],[-0.2,2.8,-0.7],[0.4,1,-3],[-0.2,-0.3,-3],[-0.5,-1.8,-3],[0,0,-1.7],[0.5,0.5,-4.5]]
    scaleList = [noScale,[1.5,1,1],[1.2,1,1],[1.2,1,1],noScale,noScale,
                [1.3,1,1],noScale,noScale,noScale,noScale,noScale,noScale]
    rotateList = [noRotate,[0,0,0.5],noRotate,[0,-0.3,0],[0,0.7,0],[0,0,-0.5],
                [0,0,-0.2],[0,0,-0.5],[0,-0.4,-0.3],noRotate,[0,-0.1,0],[0,0.3,0],[0,-0.3,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #lower lid to cheek
    selectCreatedEdgeVertical(182,False)
    directionList = [[0,0.1,-0.3],[0.2,-0.2,-0.2]]
    scaleList = [noScale,[1.6,0,0]]
    rotateList = [noRotate,[0,0.1,0.1]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[109, 111, 212, 213],
                    [168, 170, 182, 211],
                    [169, 171, 177, 185],
                    [153, 174, 175, 184],
                    [152, 179, 180, 210],
                    [150, 152, 210, 212],
                    [151, 153, 184, 186],
                    [171, 173, 185, 187],
                    [170, 172, 211, 213],
                    [107, 109, 150, 212],
                    [77, 79, 107, 150],
                    [81, 83, 151, 186],
                    [83, 85, 186, 188],
                    [85, 87, 188, 190],
                    [87, 89, 190, 192],
                    [89, 91, 192, 194],
                    [91, 93, 194, 196],
                    [93, 95, 196, 198],
                    [95, 97, 198, 200],
                    [97, 99, 200, 202],
                    [99, 101, 202, 204],
                    [101, 103, 204, 206],
                    [103, 105, 206, 208]]
    selectAndFillVerts(fillVertsList)
    #chin to scalp 
    selectCreatedEdgeVertical(5,False)
    directionList = [[2,1.5,0.7],[1.4,0.8,1],[0.5,0.3,2.6],[0.1,-0.1,1.6],[-0.2,-0.2,1],[0,-0.6,1.3],[-0.1,0.3,1],
                    [0,0.6,2]]
    scaleList = [[1,1,1],[1,0.6,1],[1,1.3,1],[1,1.5,1],[1,1.7,1],[1,0.4,1],[1,1.5,1],
                noScale]
    rotateList = [noRotate,[0,0,-0.5],noRotate,[0,1,0],noRotate,[0,0,0.3],[0,0,-0.3],
                noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([173, 225])
    selectAndMergeVerts([172, 223])
    fillVertsList = [[173, 187, 189, 225],
                    [189, 191, 225, 227],
                    [191, 193, 195, 227],
                    [195, 197, 226, 227],
                    [111, 172, 213, 221],
                    [111, 113, 219, 221],
                    [113, 115, 217, 219],
                    [115, 117, 215, 217],
                    [5, 7, 117, 215]]
    selectAndFillVerts(fillVertsList)
    #ear
    selectCreatedEdgeVertical(222,False)
    directionList = [[0.1,0.4,-0.6],[0,0.3,0],[-0.2,0.3,-0.2],[0.2,0.6,0],[0.4,-0.3,0.1],
    [0.2,0.5,-0.1],[-0.1,0.3,0],[0.3,0.1,0],[0,0.3,-0.1],[-0.4,0,0],[-0.6,-0.5,0.3]]
    scaleList = [[0.2,0.2,0.5],noScale,[1,1,1.7],noScale,noScale,
    noScale,[1,1,0.6],noScale,[1,1,1.5],noScale,[1,1,1.5]]
    rotateList = [noRotate,noRotate,noRotate,noRotate,noRotate,
    noRotate,noRotate,[-0.1,0.3,0],noRotate,noRotate,[0.1,-0.1,0.5]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #ear outer loop top
    selectCreatedEdgeVertical(245,False)
    directionList = [[0.1,0.1,0.8],[0.1,0,0.8],[0,-0.4,0.4],[0,-0.6,0.1],[-0.1,-0.4,-0.1],[-0.6,-0.5,-1],[-0.2,0.4,-0.4]]
    scaleList = [noScale,noScale,noScale,noScale,noScale,[1,1,1.3],[1,1.5,1.7]]
    rotateList = [noRotate,[0.5,0,0],[0.5,0,0],[0.5,0,0],[0.5,0,0],[0.7,0,0],[0.7,0,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #ear outer loop bottom
    selectCreatedEdgeVertical(244,False)
    directionList = [[-0.2,-0.4,-0.6],[-0.2,-0.8,-0.4],[0,-0.6,-0.1],[-0.2,-0.2,0.5],[-0.2,0.2,0.5]]
    scaleList = [noScale,[1,1,1.5],noScale,[1,2.2,1.5],[0.2,0.2,0.2]]
    rotateList = [[-0.3,0,0],[-0.7,0,0],[-0.5,0,0],[-0.5,0,-0.4],[0,0,0.3]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #inner ear main branch outer
    selectCreatedEdgeVertical(241,False)
    directionList = [[0.1,0.2,0.5],[0,0,0.7],[0.1,-0.3,0.7]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #inner ear main branch inner
    selectCreatedEdgeVertical(237,False)
    directionList = [[0.2,0.3,0.7],[0.1,-0.3,0.3],[0.1,-0.5,0.6]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [[0,0,1],[0,0.2,0.7],[1,0,0.5]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(238,False)
    extrudeDirection(-0.2,-0.5,-0.3,overallScale)
    rotateAmount(-1.5,0,0)
    scaleAmount(1,1,0.7)
    selectAndMergeVerts([218, 271])
    fillVertsList = [[218, 220, 228, 272],
                    [228, 230, 271, 272],
                    [232, 234, 236, 285],
                    [230, 232, 271, 285],
                    [270, 271, 285, 286],
                    [266, 268, 270, 286],
                    [238, 264, 266, 286],
                    [238, 240, 242, 264],
                    [241, 243, 250, 274],
                    [250, 252, 274, 276],
                    [252, 254, 276, 278],
                    [254, 256, 277, 278],
                    [256, 258, 277, 284],
                    [275, 277, 282, 284],
                    [273, 275, 280, 282],
                    [237, 239, 273, 280],
                    [233, 235, 262, 263],
                    [229, 231, 233, 263],
                    [260, 262, 281, 283],
                    [235, 262, 279, 281],
                    [222, 229, 261, 263],
                    [258, 260, 283, 284]]
    selectAndFillVerts(fillVertsList)
    selectVerts([230, 231, 232, 233],False)
    extrudeDirection(-0.6,-0.3,0,overallScale)
    selectVerts([281, 282, 283, 284],False)
    extrudeDirection(-0.3,-0.1,0.2,overallScale)
    scaleAmount(1,0.5,0.5)
    #back of ear top
    selectCreatedEdgeVertical(249,False)
    directionList = [[0,0.1,0.7],[0.1,-0.1,0.7],[0.1,-0.3,0.4],[0,-0.5,0.1],[0,-0.5,-0.1],[-0.2,-0.4,-0.5]]
    scaleList = [[0.5,1,1],noScale,noScale,noScale,[0.5,0.5,1],[0.5,0.5,1]]
    rotateList = [[0,-1,-0.2],[0.5,0,0],[0,-0.2,-0.2],[0,0,-0.2],[0,0,-0.2],[0,0.3,-0.2]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #back of ear bottom
    selectCreatedEdgeVertical(248,False)
    directionList = [[-0.2,-0.5,-0.6],[0,-0.6,-0.5],[0.1,-0.6,0.1]]
    scaleList = [noScale,[1,1,0.5],noScale]
    rotateList = [[0,0.7,0],[-1,0,0],[-0.5,0,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #under chin
    selectCreatedEdgeVertical(216,False)
    directionList = [[0.7,1.2,0.4],[0,1,0.4]]
    scaleList = [[0.5,1,0.7],noScale]
    rotateList = [noRotate,[0,-0.7,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectVerts([214,313],False)
    extrudeDirection(0,0,-3.5,overallScale)
    rotateAmount(0,0.5,0)
    selectCreatedEdgeVertical(209,False)
    extrudeDirection(0,-1,0,overallScale)
    selectAndMergeVerts([315, 319])
    fillVertsList = [[267, 269, 309, 311],
                    [265, 267, 307, 309],
                    [244, 246, 265, 307],
                    [245, 247, 251, 295],
                    [251, 253, 295, 297],
                    [253, 255, 297, 299],
                    [255, 257, 299, 301],
                    [257, 259, 301, 303],
                    [259, 261, 303, 305],
                    [222, 261, 305, 306],
                    [218, 269, 311, 312],
                    [205, 207, 315, 316],
                    [205, 308, 310, 316],
                    [310, 312, 314, 316],
                    [216, 218, 312, 314],
                    [1, 3, 214, 317],
                    [313, 315, 318, 319],
                    [203, 205, 248, 308],
                    [203, 248, 249, 296],
                    [201, 203, 296, 298],
                    [199, 201, 298, 300],
                    [197, 199, 300, 302],
                    [197, 226, 302, 304],
                    [224, 226, 304, 306],
                    [222, 223, 224, 306]]
    selectAndFillVerts(fillVertsList)
    #mouth - inner cheek loop
    selectCreatedEdgeVertical(144,False)
    directionList = [[-0.2,0.2,-0.4],[1,0.7,0.3],[0.5,0.5,0],[0.2,1,0],[0.2,1,0],[-0.4,0,0],[-0.2,0,-0.3],[-0.3,0,0],
    [-0.2,0,-0.4],[-0.9,0,-0.5],[0,-1.7,0],[0.3,-0.3,0.3],[0,0,0.4],[0.3,-0.3,0],[0,0,-0.5],[-0.6,-0.8,1.2]]
    scaleList = [[0.5,0.5,0.5],[1,1,3],[1,1,2],noScale,noScale,noScale,[0,0,0.2],noScale,
    [1,4,4],noScale,noScale,noScale,noScale,noScale,noScale,noScale]
    rotateList = [[-0.5,0,0],[-0.3,0,0],[-0.3,0.5,-2],[-0.2,0,1],noRotate,noRotate,noRotate,[-0.7,0,0],
    noRotate,[0,1.3,1.7],[0,-0.5,1.5],noRotate,[0,0.2,0],noRotate,noRotate,[0,0.7,-0.3]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #outer gum top
    selectCreatedEdgeVertical(55,False)
    directionList = [[1.1,0.6,0],[1.2,1,0],[0.2,1.3,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[330, 332, 356, 357],
                    [333, 335, 345, 347],
                    [335, 337, 343, 345],
                    [337, 339, 341, 343],
                    [23, 25, 342, 344],
                    [21, 23, 344, 346],
                    [331, 333, 347, 349],
                    [25, 27, 340, 342],
                    [27, 29, 338, 340],
                    [17, 19, 348, 350],
                    [15, 17, 147, 350],
                    [147, 149, 350, 351],
                    [19, 21, 346, 348]]
    selectAndFillVerts(fillVertsList)
    selectAndMergeVerts([149, 321])
    selectCreatedEdgeVertical(59,False)
    extrudeDirection(0.5,0.2,0.1,overallScale)
    selectAndMergeVerts([140, 358])
    fillVertsList = [[140, 142, 320, 357],
                    [320, 321, 352, 357],
                    [321, 323, 352, 354],
                    [323, 325, 354, 356],
                    [325, 327, 329, 356],
                    [149, 322, 348, 350],
                    [322, 324, 326, 348],
                    [326, 328, 330, 348],
                    [55, 57, 352, 357]]
    selectAndFillVerts(fillVertsList)
    #inner gum top
    selectCreatedEdgeVertical(51,False)
    directionList = [[1,0.5,0],[1,1,0],[0,1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(47,False)
    extrudeDirection(1,0,0,overallScale)
    scaleAmount(1,0.5,1)
    fillVertsList = [[333, 335, 362, 363],
                    [47, 49, 358, 365],
                    [358, 360, 362, 365],
                    [335, 362, 364, 365],
                    [331, 333, 355, 363],
                    [353, 355, 361, 363],
                    [351, 353, 359, 361],
                    [51, 53, 351, 359]]
    selectAndFillVerts(fillVertsList)
    selectVerts([39, 41, 43],False)
    extrudeDirection(0.5,0,0.5,overallScale)
    scaleAmount(1,0.5,1)
    selectVerts([31, 33, 35, 37],False)
    extrudeDirection(1.2,0.2,0,overallScale)
    scaleAmount(1,0.5,1)
    fillVertsList = [[369, 370, 371, 372],
                    [335, 337, 364, 366],
                    [37, 39, 366, 372],
                    [364, 366, 367, 368],
                    [43, 45, 364, 368],
                    [337, 366, 369, 372],
                    [29, 31, 337, 369]]
    selectAndFillVerts(fillVertsList)
    #bottom gums
    selectVerts([21, 23, 343, 345],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,-0.3)
    scaleAmount(0.1,0.7,0)
    selectVerts([343, 344, 345, 346],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,-0.6)
    scaleAmount(0.1,0.7,0)
    selectVerts([332, 334, 344, 346],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,0.2)
    scaleAmount(0.6,0.1,0)
    selectVerts([20, 21, 22, 23],False)
    extrudeDirection(0,0,0.1,overallScale)
    scaleAmount(0.1,1,0)
    #bottom teeth
    selectVerts([20, 22, 385, 387],False) #1
    extrudeDirection(0,-0.1,0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([21, 23, 386, 388],False) #2
    extrudeDirection(0,-0.1,0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([21, 23, 373, 374],False) #3
    extrudeDirection(0.1,-0.1,0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([343, 345, 375, 376],False) #4
    extrudeDirection(0.1,-0.1,0.4,overallScale)
    scaleAmount(1.5,1,0)
    selectVerts([343, 345, 377, 379],False) #5
    extrudeDirection(0.05,-0.05,0.3,overallScale)
    scaleAmount(1.5,1,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([344, 346, 378, 380],False) #6
    extrudeDirection(0.05,-0.05,0.3,overallScale)
    scaleAmount(1.2,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([344, 346, 383, 384],False) #7
    extrudeDirection(0.05,-0.05,0.3,overallScale)
    scaleAmount(1.1,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([332, 334, 381, 382],False) #8
    extrudeDirection(0.05,-0.05,0.3,overallScale)
    scaleAmount(1.3,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    #top gums
    selectVerts([50, 51, 52, 53],False)
    extrudeDirection(0,0,-0.1,overallScale)
    scaleAmount(0.1,1,0)
    selectVerts([51, 53, 351, 359],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,-0.3)
    scaleAmount(0.1,0.7,0)
    selectVerts([351, 353, 359, 361],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,-0.6)
    scaleAmount(0.1,0.7,0)
    selectVerts([353, 355, 361, 363],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,0.2)
    scaleAmount(0.6,0.1,0)
    #top teeth
    selectVerts([50, 52, 449, 451],False) #1
    extrudeDirection(0,0,-0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([51, 53, 450, 452],False) #2
    extrudeDirection(0,0,-0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([51, 53, 453, 454],False) #3
    extrudeDirection(0.1,0,-0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([351, 359, 455, 456],False) #4
    extrudeDirection(0.1,-0.1,-0.4,overallScale)
    scaleAmount(1.5,1,0)
    selectVerts([351, 359, 457, 459],False) #5
    extrudeDirection(0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.5,1,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([353, 361, 458, 460],False) #6
    extrudeDirection(0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.2,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([353, 361, 461, 463],False) #7
    extrudeDirection(0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.1,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([355, 363, 462, 464],False) #8
    extrudeDirection(0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.3,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    #RIGHT FACE SIDE
    #nose to chin loop
    selectCreatedEdgeVertical(76,False)
    directionList = [[-0.5,0.9,-0.3],[-0.8,0,-0.3],[-1.2,0.3,-0.7],[-0.3,0.7,-1],[0,0.2,-1.1],[0.5,-0.3,-1.3]]
    scaleList = [noScale,noScale,[1,1,1.5],noScale,noScale,noScale]
    rotateList = [noRotate,[0.5,-0.5,-0.5],[0.4,-0.8,-0.7],[0.4,-0.7,-0.5],[0,0.2,0],[0.4,-1.4,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(8,True)
    bpy.ops.mesh.edge_face_add()
    #nose to cheek join
    selectCreatedEdgeVertical(70,False)
    directionList = [[-0.2,0.2,0.1],[-0.4,0.5,-0.1],[0,0.3,-0.1],[-0.2,0.1,-0.5],[-0.4,0.2,-0.3],[-0.5,0.3,0.3]]
    scaleList = [noScale,[1.5,1.5,1],noScale,noScale,[1.5,1,1],[3,1,1]]
    rotateList = [[0,0,-0.6],[0,0,-1],noRotate,[0,0,-0.3],[0,1,0],[0.6,0.7,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(531,True)
    bpy.ops.mesh.edge_face_add()
    #nose edge
    selectCreatedEdgeVertical(540,False)
    selectCreatedEdgeVertical(542,True)
    extrudeDirection(-0.15,-0.1,0.5,overallScale)
    fillVertsList = [[70, 72, 538, 549],
                    [72, 74, 525, 549],
                    [525, 549, 550, 551]]
    selectAndFillVerts(fillVertsList)
    #cheek crease
    selectCreatedEdgeVertical(527,False)
    extrudeDirection(0,0.2,-0.3,overallScale)
    selectAndMergeVerts([551,552])
    fillVertsList = [[542, 544, 551, 552],
                    [544, 546, 548, 552],
                    [527, 529, 548, 552],
                    [62, 64, 541, 543],
                    [64, 66, 539, 541],
                    [66, 68, 537, 539]]
    selectAndFillVerts(fillVertsList)
    selectVerts([64, 541],True)
    extrudeDirection(0.1,0.1,0.3,overallScale)
    rotateAmount(0.2,-1.3,0)
    scaleAmount(1,0.7,1)
    #top lip
    selectCreatedEdgeVertical(60,False)
    directionList = [[-0.5,0.2,0.1],[-0.6,0.3,-0.4],[-0.5,0.6,-0.1]]
    scaleList = [[1,1,1.1],[1,1,0.6],noScale]
    rotateList = [noRotate,noRotate,[0,0.1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[60, 62, 543, 560],
                    [543, 545, 560, 562],
                    [545, 547, 562, 564],
                    [531, 547, 563, 564]]
    selectAndFillVerts(fillVertsList)
    #bottom lip
    selectCreatedEdgeVertical(14,False)
    directionList = [[-0.5,0.3,0.1],[-0.3,0.5,-0.1]]
    scaleList = [[1,1,0.6],[1,1,1.6]]
    rotateList = [[0,0.4,0],[0,-0.5,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[10, 12, 565, 567],
                    [8, 10, 535, 567],
                    [533, 535, 567, 568],
                    [531, 533, 563, 568]]
    selectAndFillVerts(fillVertsList)
    #eye socket
    selectCreatedEdgeVertical(80,False)
    directionList = [[-0.2,0.5,-0.3],[-0.3,0,0.1],[0,0.3,0],[-0.3,0,0],[-0.1,0.3,0],[-0.3,0.1,0],[-0.6,0.1,0],
                    [-0.3,0.1,0.1],[0,-0.5,0],[-0.3,0.2,0],[-0.3,0.3,0],[-0.4,0.6,0]]
    scaleList = [[1,1,2],[1,1,0.5],noScale,[1,1,1.5],noScale,[1,1,2.5],noScale,
                [1,1,0.2],noScale,noScale,[1,1,4],[1,1,2]]
    rotateList = [noRotate,noRotate,noRotate,noRotate,noRotate,noRotate,noRotate,
                noRotate,[0.7,0,0],noRotate,[-0.2,0.3,-0.3],[0.7,0.3,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #upperlid
    selectCreatedEdgeVertical(574,False)
    directionList = [[-0.3,0,0],[-0.5,-0.3,0.3],[-0.6,0.1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,[-0.5,0,0],[0,-1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([576, 594])
    fillVertsList = [[576, 578, 580, 595],
                    [580, 582, 595, 597],
                    [582, 584, 586, 597],
                    [586, 588, 596, 597]]
    selectAndFillVerts(fillVertsList)
    #lower lid
    selectCreatedEdgeVertical(573,False)
    directionList = [[-0.3,0,0],[-0.5,-0.1,-0.3],[-0.6,0.1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,[0.3,0,0],[0,1,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([575, 599])
    fillVertsList = [[575, 577, 579, 600],
                    [579, 581, 600, 602],
                    [581, 583, 585, 602],
                    [585, 587, 601, 602]]
    selectAndFillVerts(fillVertsList)
    #upper lid and brow
    selectCreatedEdgeVertical(596,False)
    directionList = [[0,0.1,0.3],[0.1-0.2,-0.6+0.2,0.1],[-0.1,0,0.6],[-0.1,0.4,1.8],[-0.2+0.2,0.8,2],[-0.3,2,1],
                    [-1.1,3.5,-0.2],[0.2,2.8,-0.7],[-0.4,1,-3],[0.2,-0.3,-3],[0.5,-1.8,-3],[0,0,-1.7],[-0.5,0.5,-4.5]]
    scaleList = [noScale,[1.6,1,1],[1.2,1,1],[1.2,1,1],noScale,noScale,
                [1.3,1,1],noScale,noScale,noScale,noScale,noScale,noScale]
    rotateList = [noRotate,[0,0,-0.5],noRotate,[0,0.3,0],[0,-0.7,0],[0,0,0.5],
                [0,0,0.2],[0,0,0.5],[0,0.4,0.3],noRotate,[0,0.1,0],[0,-0.3,0],[0,0.3,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #lower lid to cheek
    selectCreatedEdgeVertical(601,False)
    directionList = [[0,0.1,-0.3],[-0.2,-0.2,-0.2]]
    scaleList = [noScale,[1.6,0,0]]
    rotateList = [noRotate,[0,-0.1,-0.1]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[572, 593, 594, 603],
                    [570, 572, 603, 605],
                    [80, 82, 570, 605],
                    [82, 84, 605, 607],
                    [84, 86, 607, 609],
                    [86, 88, 609, 611],
                    [88, 90, 611, 613],
                    [90, 92, 613, 615],
                    [92, 94, 615, 617],
                    [94, 96, 617, 619],
                    [96, 98, 619, 621],
                    [98, 100, 621, 623],
                    [100, 102, 623, 625],
                    [102, 104, 625, 627],
                    [571, 598, 599, 629],
                    [569, 571, 629, 631],
                    [76, 78, 526, 569],
                    [526, 528, 569, 631],
                    [528, 530, 631, 632],
                    [588, 590, 596, 604],
                    [590, 592, 604, 606],
                    [587, 589, 601, 630],
                    [589, 591, 630, 632]]
    selectAndFillVerts(fillVertsList)
    #chin to scalp 
    selectCreatedEdgeVertical(4,False)
    directionList = [[-2,1.5,0.7],[-1.4,0.8,1],[-0.5,0.3,2.6],[-0.1,-0.1,1.6],[0.2,-0.2,1],[0,-0.6,1.3],[0.1,0.3,1],
                    [0,0.6,2]]
    scaleList = [[1,1,1],[1,0.6,1],[1,1.3,1],[1,1.5,1],[1,1.7,1],[1,0.4,1],[1,1.5,1],
                noScale]
    rotateList = [noRotate,[0,0,0.5],noRotate,[0,-1,0],noRotate,[0,0,-0.3],[0,0,0.3],
                noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectAndMergeVerts([592, 644])
    selectAndMergeVerts([591, 642])
    fillVertsList = [[4, 6, 536, 634],
                    [534, 536, 634, 636],
                    [532, 534, 636, 638],
                    [530, 532, 638, 640],
                    [530, 591, 632, 640],
                    [592, 606, 608, 644],
                    [608, 610, 644, 646],
                    [610, 612, 614, 646],
                    [614, 616, 645, 646]]
    selectAndFillVerts(fillVertsList)
    #ear
    selectCreatedEdgeVertical(641,False)
    directionList = [[-0.1,0.4,-0.6],[0,0.3,0],[0.2,0.3,-0.2],[-0.2,0.6,0],[-0.4,-0.3,0.1],
    [-0.2,0.5,-0.1],[0.1,0.3,0],[-0.3,0.1,0],[0,0.3,-0.1],[0.4,0,0],[0.6,-0.5,0.3]]
    scaleList = [[0.2,0.2,0.5],noScale,[1,1,1.7],noScale,noScale,
    noScale,[1,1,0.6],noScale,[1,1,1.5],noScale,[1,1,1.5]]
    rotateList = [noRotate,noRotate,noRotate,noRotate,noRotate,
    noRotate,noRotate,[-0.1,-0.3,0],noRotate,noRotate,[0.1,0.1,-0.5]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #ear outer loop top
    selectCreatedEdgeVertical(664,False)
    directionList = [[-0.1,0.1,0.8],[-0.1,0,0.8],[0,-0.4,0.4],[0,-0.6,0.1],[0.1,-0.4,-0.1],[0.6,-0.5,-1],[0.2,0.4,-0.4]]
    scaleList = [noScale,noScale,noScale,noScale,noScale,[1,1,1.3],[1,1.5,1.7]]
    rotateList = [noRotate,[0.5,0,0],[0.5,0,0],[0.5,0,0],[0.5,0,0],[0.7,0,0],[0.7,0,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #ear outer loop bottom
    selectCreatedEdgeVertical(663,False)
    directionList = [[0.2,-0.4,-0.6],[0.2,-0.8,-0.4],[0,-0.6,-0.1],[0.2,-0.2,0.5],[0.2,0.2,0.5]]
    scaleList = [noScale,[1,1,1.5],noScale,[1,2.2,1.5],[0.2,0.2,0.2]]
    rotateList = [[-0.3,0,0],[-0.7,0,0],[-0.5,0,0],[-0.5,0,0.4],[0,0,-0.3]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #inner ear main branch outer
    selectCreatedEdgeVertical(660,False)
    directionList = [[-0.1,0.2,0.5],[0,0,0.7],[-0.1,-0.3,0.7]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #inner ear main branch inner
    selectCreatedEdgeVertical(656,False)
    directionList = [[-0.2,0.3,0.7],[-0.1,-0.3,0.3],[-0.1,-0.5,0.6]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [[0,0,-1],[0,-0.2,-0.7],[1,0,-0.5]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(657,False)
    extrudeDirection(0.2,-0.5,-0.3,overallScale)
    rotateAmount(-1.5,0,0)
    scaleAmount(1,1,0.7)
    selectAndMergeVerts([637, 690])
    fillVertsList = [[648, 650, 652, 682],
                    [641, 648, 680, 682],
                    [647, 649, 690, 691],
                    [649, 651, 690, 704],
                    [689, 690, 704, 705],
                    [637, 639, 647, 691],
                    [657, 659, 661, 683],
                    [657, 683, 685, 705],
                    [685, 687, 689, 705],
                    [677, 679, 702, 703],
                    [675, 677, 696, 703],
                    [673, 675, 696, 697],
                    [671, 673, 695, 697],
                    [669, 671, 693, 695],
                    [660, 662, 669, 693],
                    [656, 658, 692, 699],
                    [692, 694, 699, 701],
                    [694, 696, 701, 703],
                    [679, 681, 700, 702],
                    [654, 681, 698, 700],
                    [652, 654, 681, 682],
                    [651, 653, 655, 704]]
    selectAndFillVerts(fillVertsList)
    selectVerts([651, 652, 653, 654],False)
    extrudeDirection(0.6,-0.3,0,overallScale)
    selectVerts([700, 701, 702, 703],False)
    extrudeDirection(0.3,-0.1,0.2,overallScale)
    scaleAmount(1,0.5,0.5)
    #back of ear top
    selectCreatedEdgeVertical(668,False)
    directionList = [[0,0.1,0.7],[-0.1,-0.1,0.7],[-0.1,-0.3,0.4],[0,-0.5,0.1],[0,-0.5,-0.1],[0.2,-0.4,-0.5]]
    scaleList = [[0.5,1,1],noScale,noScale,noScale,[0.5,0.5,1],[0.5,0.5,1]]
    rotateList = [[0,1,0.2],[0.5,0,0],[0,0.2,0.2],[0,0,0.2],[0,0,0.2],[0,-0.3,0.2]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #back of ear bottom
    selectCreatedEdgeVertical(667,False)
    directionList = [[0.2,-0.5,-0.6],[0,-0.6,-0.5],[-0.1,-0.6,0.1]]
    scaleList = [noScale,[1,1,0.5],noScale]
    rotateList = [[0,-0.7,0],[-1,0,0],[-0.5,0,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #under chin
    selectCreatedEdgeVertical(635,False)
    directionList = [[-0.7,1.2,0.4],[0,1,0.4]]
    scaleList = [[0.5,1,0.7],noScale]
    rotateList = [noRotate,[0,0.7,0]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectVerts([633, 732],False)
    extrudeDirection(0,0,-3.5,overallScale)
    rotateAmount(0,-0.5,0)
    selectCreatedEdgeVertical(628,False)
    extrudeDirection(0,-1,0,overallScale)
    selectAndMergeVerts([734, 738])
    fillVertsList = [[0, 2, 633, 736],
                    [732, 734, 737, 738],
                    [624, 626, 734, 735],
                    [678, 680, 722, 724],
                    [676, 678, 720, 722],
                    [674, 676, 718, 720],
                    [672, 674, 716, 718],
                    [670, 672, 714, 716],
                    [664, 666, 670, 714],
                    [663, 665, 684, 726],
                    [684, 686, 726, 728],
                    [686, 688, 728, 730],
                    [637, 688, 730, 731],
                    [641, 680, 724, 725],
                    [635, 637, 731, 733],
                    [729, 731, 733, 735],
                    [624, 727, 729, 735],
                    [622, 624, 667, 727],
                    [622, 667, 668, 715],
                    [620, 622, 715, 717],
                    [618, 620, 717, 719],
                    [616, 618, 719, 721],
                    [616, 645, 721, 723],
                    [643, 645, 723, 725],
                    [641, 642, 643, 725]]
    selectAndFillVerts(fillVertsList)
    #mouth - inner cheek loop
    selectCreatedEdgeVertical(563,False)
    directionList = [[0.2,0.2,-0.4],[-1,0.7,0.3],[-0.5,0.5,0],[-0.2,1,0],[-0.2,1,0],[0.4,0,0],[0.2,0,-0.3],[0.3,0,0],
    [0.2,0,-0.4],[0.9,0,-0.5],[0,-1.7,0],[-0.3,-0.3,0.3],[0,0,0.4],[-0.3,-0.3,0],[0,0,-0.5],[0.6,-0.8,1.2]]
    scaleList = [[0.5,0.5,0.5],[1,1,3],[1,1,2],noScale,noScale,noScale,[0,0,0.2],noScale,
    [1,4,4],noScale,noScale,noScale,noScale,noScale,noScale,noScale]
    rotateList = [[-0.5,0,0],[-0.3,0,0],[-0.3,-0.5,2],[-0.2,0,-1],noRotate,noRotate,noRotate,[-0.7,0,0],
    noRotate,[0,-1.3,-1.7],[0,0.5,-1.5],noRotate,[0,-0.2,0],noRotate,noRotate,[0,-0.7,0.3]]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #outer gum top
    selectCreatedEdgeVertical(54,False)
    directionList = [[-1.1,0.6,0],[-1.2,1,0],[-0.2,1.3,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    fillVertsList = [[26, 28, 757, 759],
                    [24, 26, 759, 761],
                    [22, 24, 761, 763],
                    [20, 22, 763, 765],
                    [18, 20, 765, 767],
                    [16, 18, 767, 769],
                    [14, 16, 566, 769],
                    [566, 568, 769, 770],
                    [756, 758, 760, 762],
                    [754, 756, 762, 764],
                    [752, 754, 764, 766],
                    [750, 752, 766, 768],
                    [745, 747, 749, 776]]
    selectAndFillVerts(fillVertsList)
    
    selectAndMergeVerts([568, 740])
    selectCreatedEdgeVertical(58,False)
    extrudeDirection(-0.5,0.2,0.1,overallScale)
    selectAndMergeVerts([559, 777])
    fillVertsList = [[559, 561, 739, 776],
                    [54, 56, 771, 776],
                    [739, 740, 771, 776],
                    [559, 561, 739, 776],
                    [54, 56, 771, 776],
                    [739, 740, 771, 776],
                    [740, 742, 771, 773],
                    [742, 744, 773, 775],
                    [568, 741, 767, 769],
                    [741, 743, 745, 767],
                    [745, 747, 749, 767],
                    [748, 750, 774, 775]]
    selectAndFillVerts(fillVertsList)
    #inner gum top
    selectCreatedEdgeVertical(50,False)
    directionList = [[-1,0.5,0],[-1,1,0],[0,1,0]]
    scaleList = [noScale,noScale,noScale]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectCreatedEdgeVertical(46,False)
    extrudeDirection(-1,0,0,overallScale)
    scaleAmount(1,0.5,1) #8
    fillVertsList = [[46, 48, 777, 784],
                    [777, 779, 781, 784],
                    [750, 752, 774, 782],
                    [772, 774, 780, 782],
                    [770, 772, 778, 780],
                    [50, 52, 770, 778],
                    [752, 754, 781, 782],
                    [754, 781, 783, 784]]
    selectAndFillVerts(fillVertsList)
    selectVerts([38, 40, 42],False)
    extrudeDirection(-0.5,0,0.5,overallScale)
    scaleAmount(1,0.5,1)
    selectVerts([30, 32, 34, 36],False)
    extrudeDirection(-1.2,0.2,0,overallScale)
    scaleAmount(1,0.5,1)
    fillVertsList = [[788, 789, 790, 791],
                    [28, 30, 756, 788],
                    [36, 38, 785, 791],
                    [756, 785, 788, 791],
                    [783, 785, 786, 787],
                    [42, 44, 783, 787],
                    [754, 756, 783, 785]]
    selectAndFillVerts(fillVertsList)
    #bottom gums
    selectVerts([20, 22, 762, 764],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,0.3)
    scaleAmount(0.1,0.7,0)
    selectVerts([762, 763, 764, 765],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,0.6)
    scaleAmount(0.1,0.7,0)
    selectVerts([751, 753, 763, 765],False)
    extrudeDirection(0,0,0.1,overallScale)
    rotateAmount(0,0,-0.2)
    scaleAmount(0.6,0.1,0)
    #bottom teeth
    selectVerts([20, 22, 792, 793],False) #3
    extrudeDirection(-0.1,-0.1,0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([762, 764, 794, 795],False) #4
    extrudeDirection(-0.1,-0.1,0.4,overallScale)
    scaleAmount(1.5,1,0)
    selectVerts([762, 764, 796, 798],False) #5
    extrudeDirection(-0.05,-0.05,0.3,overallScale)
    scaleAmount(1.5,1,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([763, 765, 797, 799],False) #6
    extrudeDirection(-0.05,-0.05,0.3,overallScale)
    scaleAmount(1.2,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([763, 765, 802, 803],False) #7
    extrudeDirection(-0.05,-0.05,0.3,overallScale)
    scaleAmount(1.1,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    selectVerts([751, 753, 800, 801],False) #8
    extrudeDirection(-0.05,-0.05,0.3,overallScale)
    scaleAmount(1.3,1.2,0)
    extrudeDirection(0,0,0.1,overallScale)
    #top gums
    selectVerts([50, 52, 770, 778],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,0.3)
    scaleAmount(0.1,0.7,0)
    selectVerts([770, 772, 778, 780],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,0.6)
    scaleAmount(0.1,0.7,0)
    selectVerts([772, 774, 780, 782],False)
    extrudeDirection(0,0,-0.1,overallScale)
    rotateAmount(0,0,-0.2)
    scaleAmount(0.6,0.1,0)
    #top teeth
    selectVerts([50, 52, 848, 849],False) #3
    extrudeDirection(-0.1,0,-0.3,overallScale)
    scaleAmount(1.5,0.5,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([770, 778, 850, 851],False) #4
    extrudeDirection(-0.1,-0.1,-0.4,overallScale)
    scaleAmount(1.5,1,0)
    selectVerts([770, 778, 852, 854],False) #5
    extrudeDirection(-0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.5,1,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([772, 780, 853, 855],False) #6
    extrudeDirection(-0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.2,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([772, 780, 856, 858],False) #7
    extrudeDirection(-0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.1,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    selectVerts([774, 782, 857, 859],False) #8
    extrudeDirection(-0.05,-0.05,-0.3,overallScale)
    scaleAmount(1.3,1.2,0)
    extrudeDirection(0,0,-0.1,overallScale)
    #eyes
    selectVerts([160, 161, 162, 163],False)
    directionList = [[0,-0.2,0],[0,-0.5,0.2],[0,0,0]]
    scaleList = [[3,0.5,2],[0.4,1,0.3],[0.6,1,0.7]]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    selectVerts([579, 580, 581, 582],False)
    directionList = [[0,-0.2,0],[0,-0.5,0.2],[0,0,0]]
    scaleList = [[3,0.5,2],[0.4,1,0.3],[0.6,1,0.7]]
    rotateList = [noRotate,noRotate,noRotate]
    extrudeMultiple(directionList,scaleList,rotateList,overallScale)
    #cleanup
    cleanMesh()
    #face modifications
    #chin down
    vertTransformWeightLists = [[1,[4, 5, 6, 7, 8, 9]],
                                [0.7,[215, 634]],
                                [0.5,[2, 3, 116, 535, 117, 536, 217, 636]],
                                [0.3,[214, 633, 216, 635]],
                                [0.1,[313, 732]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-chinDown],[0,0,0],[0,0,0],overallScale)
    #chin forwards
    vertTransformWeightLists = [[1,[6, 7, 8, 9, 4, 5]],
                                [0.5,[116, 117, 535, 536, 215, 634]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-chinForwards,0],[0,0,0],[0,0,0],overallScale)
    #chin width
    vertTransformWeightLists = [[1,[4, 5, 6, 7, 8, 9]],
                                [0.15,[116, 117, 215, 535, 536, 634]],
                                [0.1,[314, 316, 733, 735, 216, 217, 635, 636]],
                                [0.05,[218, 219, 637, 638]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0+chinWiden,0,0],[0,0,0],overallScale)
    #nose forwards lengthen
    vertTransformWeightLists = [[1,[70, 71, 72, 73]],
                                [0.2,[119, 130, 538, 549, 74, 75]],
                                [0.01,[68, 69, 118, 136, 137, 537, 555, 556]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-noseForwards,0+(noseForwards*0.1)],[0,0,0],[0,0,0],overallScale)
    #nose width
    vertTransformWeightLists = [[1,[118, 119, 120, 121, 122, 123, 130, 131, 132, 134, 135, 136, 137, 138, 139, 537, 538, 539, 540, 541, 542, 549, 550, 551, 553, 554, 555, 556, 557, 558]],
                                [0.5,[64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 134, 135, 136, 553, 554, 555, 74, 75, 106, 525, 125, 544]],
                                [0.3,[127, 546]],
                                [0.2,[108, 124, 133, 527, 552, 128, 129, 547, 548]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0+noseWiden,0,0],[0,0,0],overallScale)
    #left eye distance
    vertTransformWeightLists = [[1,[152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 
                                166, 167, 168, 169, 170, 171, 174, 175, 176, 177, 178, 179, 180, 181, 182, 
                                183, 184, 185, 210, 211, 213, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915]],
                                [0.5,[172, 173, 111, 187, 189, 186, 188]],
                                [0.3,[79, 81, 150, 151, 83, 85]]]
    selectAndTransformVerts(vertTransformWeightLists,[0+eyeLeftOut+0.15,0,0],[0,0,0],[0,0,0],overallScale)
    #right eye distance
    vertTransformWeightLists = [[1,[571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 
                                585, 586, 587, 588, 589, 590, 593, 594, 595, 596, 597, 598, 599, 600, 601, 
                                602, 603, 604, 629, 630, 632, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927]],
                                [0.5,[530, 591, 592, 605, 606, 607, 608]],
                                [0.3,[78, 80, 82, 84, 569, 570]]]
    selectAndTransformVerts(vertTransformWeightLists,[0-eyeRightOut-0.15,0,0],[0,0,0],[0,0,0],overallScale)
    #cheek fold wideness
    vertTransformWeightLists = [[1,[129, 133, 548, 552]],
                                [0.5,[108, 527]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0+cheekFoldWiden-0.3,0],[0+((cheekFoldWiden-0.3)*0.5),0,0],[0,0,0],overallScale)
    vertTransformWeightLists = [[1,[110, 112, 529, 531]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0+((cheekFoldWiden-0.3)*0.5),0,0],[0,0,0],overallScale)
    #cheek forwards left
    vertTransformWeightLists = [[1,[108, 111, 133, 110, 129]],
                                [0.5,[109, 213, 106, 123, 132, 112, 113, 125, 127, 128]],
                                [0.2,[107, 212]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-cheekForwardLeft+0.3,0],[0,0,0],[0,0,0],overallScale)
    #cheek forwards right
    vertTransformWeightLists = [[1,[527, 529, 530, 548, 552]],
                                [0.5,[525, 528, 531, 532, 542, 544, 546, 547, 551, 632]],
                                [0.2,[526, 631]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-cheekForwardRight+0.3,0],[0,0,0],[0,0,0],overallScale)
    #narrowing of mouth and jaw
    vertTransformWeightLists = [[1,[114, 115, 116, 117, 214, 215, 217, 533, 534, 535, 536, 633, 634, 636]],
                                [0.7,[18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, #entire mouth
                                48, 49, 50, 51, 52, 53, 54, 55, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 
                                340, 341, 342, 343, 344, 345, 346, 347, 348, 350, 351, 352, 353, 354, 355, 356, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 
                                368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 
                                394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 
                                420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 
                                446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 
                                472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 
                                498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 
                                524, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 
                                765, 766, 767, 769, 770, 771, 772, 773, 774, 775, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 
                                793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 
                                819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 
                                845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 
                                871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 
                                897, 898, 899, 900, 901, 902, 903]],
                                [0.5,[113, 218, 219, 532, 637, 638, 205, 207, 208, 209, 317, 318, 319, 624, 626, 627, 628, 736, 737, 738, 313, 314, 315, 316, 732, 733, 734, 735, 216, 635]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0-jawNarrow-0.1,0,0],[0,0,0],overallScale)
    #bring down left upper lid
    vertTransformWeightLists = [[1,[175, 176, 177, 178, 161, 163]],
                                [0.5,[184, 185]],
                                [0.1,[153, 167, 169, 171, 174]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-upperLidLeftDown],[0,0,0],[0,0,0],overallScale)
    #bring up left lower lid
    vertTransformWeightLists = [[1,[180, 181, 182, 183, 160, 162]],
                                [0.8,[210, 211, 212, 213]],
                                [0.5,[109]],
                                [0.1,[152, 166, 168, 170, 179]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+lowerLidLeftUp+0.1],[0,0,0],[0,0,0],overallScale)
    #bring down right upper lid
    vertTransformWeightLists = [[1,[594, 595, 596, 597, 580, 582]],
                                [0.5,[603, 604]],
                                [0.1,[572, 586, 588, 590, 593]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-upperLidRightDown],[0,0,0],[0,0,0],overallScale)
    #bring up right lower lid
    vertTransformWeightLists = [[1,[599, 600, 601, 602, 579, 581]],
                                [0.8,[629, 630, 631, 632]],
                                [0.5,[528]],
                                [0.1,[571, 585, 587, 589, 598]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+lowerLidRightUp+0.1],[0,0,0],[0,0,0],overallScale)
    #bring up left brow
    vertTransformWeightLists = [[1,[186, 187, 188, 189]],
                                [0.5,[83, 85, 173, 225, 190, 191]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+browLeftUp+0.2],[0,0,0],[0,0,0],overallScale)
    #bring up right brow
    vertTransformWeightLists = [[1,[605, 606, 607, 608]],
                                [0.5,[82, 84, 592, 609, 610, 644]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+browRightUp+0.2],[0,0,0],[0,0,0],overallScale)
    #bring up left mouth corner
    vertTransformWeightLists = [[1,[142, 143, 144, 145]],
                                [0.8,[114, 126, 149, 320, 350]],
                                [0.5,[108, 110, 112, 125, 127, 128, 129, 133]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+mouthCornerLeftUp+0.2],[0,0,0],[0,0,0],overallScale)
    #bring up right mouth corner
    vertTransformWeightLists = [[1,[561, 562, 563, 564]],
                                [0.8,[531, 545, 547, 568, 739]],
                                [0.5,[527, 529, 532, 548, 552, 769, 533, 544, 546]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0+mouthCornerRightUp+0.2],[0,0,0],[0,0,0],overallScale)
    #bring forwards left ear
    vertTransformWeightLists = [[1,[218, 220, 222, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 
                                241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 
                                258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 
                                275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 
                                292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 
                                309, 310, 311, 312]],
                                [0.5,[624, 626, 734, 735]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-earLeftForwards-1,0],[0,0,0],[0,0,0],overallScale)
    #bring forwards right ear
    vertTransformWeightLists = [[1,[637, 639, 641, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 
                                660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 
                                677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 
                                694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 
                                711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 
                                728, 729, 730, 731]],
                                [0.5,[205, 207, 315, 316]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0-earRightForwards-1,0],[0,0,0],[0,0,0],overallScale)
    #bring down mouth
    vertTransformWeightLists = [[1,[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 124, 126, 140, 141, 142, 143, 
                                144, 145, 146, 147, 148, 149, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 
                                330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 
                                346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 
                                362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 
                                378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 
                                394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 
                                410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 
                                426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 
                                442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 
                                458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 
                                474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 
                                490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 
                                506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 
                                522, 523, 524, 543, 545, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 739, 
                                740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 
                                756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 
                                772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 
                                788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 
                                804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 
                                820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 
                                836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 
                                852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 
                                868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 
                                884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 
                                900, 901, 902, 903]],
                                [0.8,[112, 114, 531, 533]],
                                [0.5,[8, 9, 125, 127, 128, 544, 546, 547, 115, 116, 117, 534, 535, 536]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-mouthDown-0.15],[0,0,0],[0,0,0],overallScale)
    #widen top lip
    vertTransformWeightLists = [[1,[56, 57, 58, 59, 60, 61, 62, 63, 124, 126, 140, 141, 142, 143, 320, 357, 543, 
                                559, 560, 561, 562, 739, 776, 545]],
                                [0.7,[144, 145, 563, 564]],
                                [0.2,[110, 112, 128, 129, 529, 531, 547, 548, 125, 127, 544, 546, 108, 133, 527, 552]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0+lipTopWiden-0.2,0+(lipTopWiden*0.5)-0.1,0],[0,0,0],overallScale)
    vertTransformWeightLists = [[1,[144, 145, 563, 564]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0+(lipTopWiden*0.5)-0.1,0],[0,0,0],[0,0,0],overallScale)
    #widen bottom lip
    vertTransformWeightLists = [[1,[10, 11, 12, 13, 14, 15, 16, 17, 146, 147, 349, 565, 566, 768]],
                                [0.5,[148, 149, 567, 568]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0+lipBottomWiden+0.1,0+(lipBottomWiden*0.5)+0.05,0],[0,0,0],overallScale)
    vertTransformWeightLists = [[1,[148, 149, 567, 568]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0+(lipBottomWiden*0.5)+0.05,0],[0,0,0],[0,0,0],overallScale)
    #heighten left ear
    vertTransformWeightLists = [[1,[218, 220, 222, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 
                                241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 
                                258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 
                                275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 
                                292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 
                                309, 310, 311, 312]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0,0,0+earLeftHeight-0.15],[0,0,0],overallScale)
    #heighten right ear
    vertTransformWeightLists = [[1,[637, 639, 641, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 
                                660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 
                                677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 
                                694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 
                                711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 
                                728, 729, 730, 731]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0],[0,0,0+earRightHeight-0.15],[0,0,0],overallScale)
    #bring nose down
    vertTransformWeightLists = [[1,[64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 106, 118, 119, 120, 121, 122, 123, 
                                130, 131, 132, 134, 135, 136, 137, 138, 139, 525, 537, 538, 539, 540, 541, 542, 549, 550, 
                                551, 553, 554, 555, 556, 557, 558,108, 133, 527, 552]],
                                [0.5,[110, 112, 125, 127, 128, 129, 529, 531, 544, 546, 547, 548]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-noseDown],[0,0,0],[0,0,0],overallScale)
    #lower neck join for a less sharp jaw
    vertTransformWeightLists = [[1,[2, 3, 102, 103, 206, 207, 214, 313, 315, 625, 626, 633, 732, 734]]]
    selectAndTransformVerts(vertTransformWeightLists,[0,0,0-neckJoinLower],[0,0,0],[0,0,0],overallScale)
    #createBoneAtPosition(0,2.5,0,overallScale,"neckAdjust")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
#printVertsSelected() 
genFace()
