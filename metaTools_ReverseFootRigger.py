import maya.cmds as cmds

# Assumptions:
#   For Left Foot,
#   -> The joints' primary axes are +Y (aims down positive Y)
#   -> The joints' up vectors would be +Z (if the foot turns right or left, it would use RotateZ)
#   -> The joints' side axes are X (meaning, the foot roll will perform on RotateX)
#
#   -> The tool assumes that the pivots required to enable reverse foot rig are present and have already been positioned accordingly.
#   -> The tool assumes that the reverse foot rig attributes (for animation, and for settings) are set in the foot controller.
#   -> The tool assumes that the user has already created necessary pivot nodes and are parented to form appropriate hierarchy.
#   -> The tool assumes that there are no name duplicates for the nodes required in the process
#   
#   What the Tool doesn't do:
#       -> The tool doesn't check if the pivots are located correctly at their preferred location. (expected to have pivots located correctly from the outset)
#       -> The tool doesn't create the animator-facing attributes in the foot controller. (expected to have attributes created in the foot controller from the outset)
#       -> The tool doesn't check if the foot joints have branching (eg. extra joint chain branching out from the foot joints). (expected to have a single clean joint chain with no branching)
#   What the Tool does:
#       -> The tool checks if the necessary pivots for foot roll and banking exist and are parented under the correct hierarchy
#       -> The tool checks if the necessary attributes for foot roll and banking exist in the foot controller with the correct specifications (data type, value range, etc).
#       -> The tool creates the necessary utility nodes for foot roll and foot banking, sets their specifications, and connects them together to form the reverse foot rig setup.
#       -> The tool connects the reverse foot rig setup to the foot roll attribute and foot banking attributes in the foot controller, and to the appropriate pivot nodes for foot roll and foot banking.
#
# ---------------------------------------------------------------
#
# Number of nodes:
#   1) Condition: 6 {
#                       footRoll_ball_condition,
#                       footRoll_heel_condition,
#                       footRoll_end_condition,
#                       footRoll_clamp_condition,
#                       footRoll_tiptoe_condition,
#                       footBank_condition
#                   }

#   2) multiplyDivide: 3 {
#                       footRoll_multi,
#                       footRoll_ball_multi
#                       footBank_multi
#                   }

#   3) plusMinusAverage: 3 {
#                       footRoll_pma,
#                       footRoll_ball_pma,
#                       footRoll_tiptoe_pma
#                   }
#
# ---------------------------------------------------------------
#
#   Animator-facing Attributes: 5 {
#                       foot_ctrl.Roll
#                       foot_ctrl.Bank
#                       foot_ctrl.ToeSway
#                       foot_ctrl.HeelSway
#                       foot_ctrl.ToeTap
#                   }
#
#   Setting/Tuning Attributes: 5 {
#                       foot_ctrl.RollBack
#                       foot_ctrl.RollEnd
#                       foot_ctrl.ToeFlex
#                       foot_ctrl.ToeStraightAngle
#                       foot_ctrl.BankMultiplier
#                   }
#
# ---------------------------------------------------------------
#
#   Rotation pivots: 8 {
#                       root_pivot,
#                       heel_pivot,
#                       inner_pivot,
#                       outer_pivot,
#                       end_pivot,
#                       ball_pivot,
#                       ankle_pivot,
#                       toe_pivot,
#                   }



# ---------------------------------------------------------------
# UI
# ---------------------------------------------------------------

def openUI():
    # If window already exists, close it and create a fresh one.
    if cmds.window("reverse_foot_rig_window", exists=True):
        cmds.deleteUI("reverse_foot_rig_window")

    window = cmds.window(
        "reverse_foot_rig_window",
        title="metaTools Reverse Foot Rigger",
        width=360,
        sizeable=False
    )

    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6,
        columnAttach=("both", 10)
    )

    cmds.separator(height=6, style="none")

    cmds.text(
        label="< metaTools Reverse Foot Rigger >",
        align="center",
        height=24
    )

    cmds.separator(height=8, style="single")

    cmds.text(
        label="This tool creates a reverse foot rig setup using utility nodes and connects it to the foot controller and foot joints.",
        align="center",
        wordWrap=True,
        height=36
    )


    cmds.text(
        label="Note: This tool does not place pivots or create controller attributes.",
        align="center",
        wordWrap=True,
        height=36
    )

    cmds.separator(height=8, style="single")

    # -----------------------------------------------------------
    # Input fields
    # -----------------------------------------------------------


    # Limb side dropdown menu
    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(100, 80),
        columnAlign2=("right", "left"),
        columnAttach2=("right", "left"),
        columnOffset2=(0, 6)
    )

    cmds.text(label="Limb Side:")
    cmds.optionMenu("revFoot_limb_side_menu", width=80)
    cmds.menuItem(label="L")
    cmds.menuItem(label="R")

    cmds.setParent("..")

    # Foot controller text field
    cmds.textFieldGrp(
        "revFoot_foot_ctrl_field",
        label="Foot Ctrl: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    # IK foot joints text fields
    cmds.textFieldGrp(
        "revFoot_ankle_joint_IK_field",
        label="Ankle IK: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    cmds.textFieldGrp(
        "revFoot_ball_joint_IK_field",
        label="Ball IK: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    cmds.textFieldGrp(
        "revFoot_toe_joint_IK_field",
        label="Toe IK: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    cmds.separator(height=6, style="none")

    # Bind foot joints text fields
    cmds.textFieldGrp(
        "revFoot_ankle_joint_bind_field",
        label="Ankle Bind: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    cmds.textFieldGrp(
        "revFoot_ball_joint_bind_field",
        label="Ball Bind: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    cmds.textFieldGrp(
        "revFoot_toe_joint_bind_field",
        label="Toe Bind: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )

    # Leg IK handle text field
    cmds.textFieldGrp(
        "revFoot_leg_ikHandle_field",
        label="Leg RP IK: ",
        text="",
        columnWidth2=(100, 220),
        adjustableColumn=2
    )


    cmds.separator(height=10, style="single")

    # -----------------------------------------------------------
    # Build button
    # -----------------------------------------------------------

    cmds.button(
        label="Build Reverse Foot Rig",
        height=34,
        command=building_revRig
    )

    cmds.separator(height=6, style="none")

    
    cmds.text(
        label="Contact Email: khantarkarzwe@gmail.com",
        align="center",
        height=18
    )

    cmds.separator(height=6, style="none")


    cmds.showWindow(window)

    cmds.window(
        window,
        edit=True,
        widthHeight=(360, 510)
    )



def building_revRig(*args): # This is the main router function
    foot_ctrl, foot_joints_IK, foot_joints_bind, leg_ikHandle, limb_side = checking_UI_input()

    rig = ReverseFootRig(
        foot_ctrl,
        foot_joints_IK,
        foot_joints_bind,
        leg_ikHandle,
        limb_side
    )

    rig.checking_parenting_and_hierarchy()
    rig.creating_ikHandles()
    rig.connecting_foot_bind_joints()
    rig.creating_nodes()
    rig.setting_node_specs()
    rig.connecting_nodes()



def checking_UI_input():
    # received controller input from user ("String")
    # foot_ctrl = "L_ankle_IK_ctrl" # hardcoded for now. Later this will receive string value from UI from user.
    # foot_ctrl = cmds.textField("foot_ctrl_input_field", query=True, text=True)

    # received foot joints input from user ("String")
    # foot_joints = ["L_ankle_IK", "L_foot_IK", "L_tiptoe_IK"] # hardcoded for now. Later this will receive string value from UI from user.
    # foot_joints = cmds.textField("foot_joints_input_field", query=True, text=True)

    # received leg ikHandle input from user ("String")
    # leg_ikHandle = "L_Leg_RP_ikHandle" # hardcoded for now. Later this will receive string value from UI from user.
    # leg_ikHandle = cmds.textField("leg_ikHandle_input_field", query=True, text=True)

    # received limb side from user ("String")
    # limb_side = "L" # hardcoded for now. Later this will receive string value from UI from user.


    # -----------------------------------------------------------
    # Query UI text fields
    # -----------------------------------------------------------

    limb_side = cmds.optionMenu(
        "revFoot_limb_side_menu",
        query=True,
        value=True
    )

    foot_ctrl = cmds.textFieldGrp(
        "revFoot_foot_ctrl_field",
        query=True,
        text=True
    ).strip()

    ankle_joint_IK = cmds.textFieldGrp(
        "revFoot_ankle_joint_IK_field",
        query=True,
        text=True
    ).strip()

    ball_joint_IK = cmds.textFieldGrp(
        "revFoot_ball_joint_IK_field",
        query=True,
        text=True
    ).strip()

    toe_joint_IK = cmds.textFieldGrp(
        "revFoot_toe_joint_IK_field",
        query=True,
        text=True
    ).strip()

    ankle_joint_bind = cmds.textFieldGrp(
        "revFoot_ankle_joint_bind_field",
        query=True,
        text=True
    ).strip()

    ball_joint_bind = cmds.textFieldGrp(
        "revFoot_ball_joint_bind_field",
        query=True,
        text=True
    ).strip()

    toe_joint_bind = cmds.textFieldGrp(
        "revFoot_toe_joint_bind_field",
        query=True,
        text=True
    ).strip()

    leg_ikHandle = cmds.textFieldGrp(
        "revFoot_leg_ikHandle_field",
        query=True,
        text=True
    ).strip()


    foot_joints_IK = [
        ankle_joint_IK,
        ball_joint_IK,
        toe_joint_IK,    
    ]

    foot_joints_bind = [
        ankle_joint_bind,
        ball_joint_bind,
        toe_joint_bind,    
    ]


    # -----------------------------------------------------------
    # Basic empty-field validation
    # -----------------------------------------------------------

    if not foot_ctrl:
        cmds.error("Foot controller field is empty.")

    if not ankle_joint_IK:
        cmds.error("Ankle joint (IK) field is empty.")

    if not ball_joint_IK:
        cmds.error("Ball joint (IK) field is empty.")

    if not toe_joint_IK:
        cmds.error("Toe joint (IK) field is empty.")

    if not ankle_joint_bind:
        cmds.error("Ankle bind joint field is empty.")

    if not ball_joint_bind:
        cmds.error("Ball bind joint field is empty.")

    if not toe_joint_bind:
        cmds.error("Toe bind joint field is empty.")

    if not leg_ikHandle:
        cmds.error("Leg RP IK handle field is empty.")

    if not limb_side:
        cmds.error("Limb side field is empty. Expected 'L' or 'R'.")



    # -----------------------------------------------------------
    # Controller validation
    # -----------------------------------------------------------

    if not cmds.objExists(foot_ctrl):
        cmds.error(f"Foot controller does not exist: {foot_ctrl}")


    # -----------------------------------------------------------
    # Limb side validation
    # -----------------------------------------------------------

    # Check if the limb side is valid
    if limb_side not in ["L", "R"]:
        cmds.error(f" Invalid limb side: {limb_side}. Expected 'L' or 'R'.")


    # -----------------------------------------------------------
    # IK foot joint validation
    # -----------------------------------------------------------

    if len(foot_joints_IK) != 3:
        cmds.error(
            f"Current number of IK foot joints: {len(foot_joints_IK)}. "
            f"Expected 3 joints: ankle IK, ball IK, toe IK."
        )

    for joint in foot_joints_IK:
        if not cmds.objExists(joint):
            cmds.error(f"IK foot joint does not exist: {joint}")

        if cmds.nodeType(joint) != "joint":
            cmds.error(
                f"Received IK foot joint: {joint} is not a joint. "
                f"Current type: {cmds.nodeType(joint)}"
            )


    # -----------------------------------------------------------
    # Bind foot joint validation
    # -----------------------------------------------------------

    if len(foot_joints_bind) != 3:
        cmds.error(
            f"Current number of bind foot joints: {len(foot_joints_bind)}. "
            f"Expected 3 joints: ankle bind, ball bind, toe bind."
        )

    for joint in foot_joints_bind:
        if not cmds.objExists(joint):
            cmds.error(f"Bind foot joint does not exist: {joint}")

        if cmds.nodeType(joint) != "joint":
            cmds.error(
                f"Received bind foot joint: {joint} is not a joint. "
                f"Current type: {cmds.nodeType(joint)}"
            )


    # -----------------------------------------------------------
    # Prevent accidentally using the same joints for IK and bind
    # -----------------------------------------------------------

    for ik_joint, bind_joint in zip(foot_joints_IK, foot_joints_bind): # zip function uses one ik_joint and one bind_joint from the lists in each loop
        if ik_joint == bind_joint:
            cmds.error(
                f"IK joint and bind joint cannot be the same object: {ik_joint}"
            )
 

    # -----------------------------------------------------------
    # Attribute validation
    # -----------------------------------------------------------

    attr_list = [
        "Roll",
        "Bank",
        "ToeSway",
        "HeelSway",
        "ToeTap",
        "RollBack",
        "RollEnd",
        "ToeFlex",
        "ToeStraightAngle",
        "BankMultiplier"
    ]

    for attr in attr_list:
        if not cmds.attributeQuery(attr, node=foot_ctrl, exists=True):
            cmds.error(f"Missing attribute: {foot_ctrl}.{attr}")

        attr_type = cmds.getAttr(foot_ctrl + "." + attr, type=True)

        if attr_type not in ["float", "double", "long"]:
            cmds.error(
                f"Attribute {foot_ctrl}.{attr} must be numeric. "
                f"Current data type: {attr_type}"
            )


    # -----------------------------------------------------------
    # Roll range validation
    # -----------------------------------------------------------

    # Check if attribute "Roll" has minimum -10 and maximum 20 value range defined
    if not cmds.attributeQuery(attr_list[0], node=foot_ctrl, rangeExists=True):
        cmds.error(f"Attribute {foot_ctrl}.{attr_list[0]} does not have -10 to 20 range defined")

    # Get both values at once
    min_value, max_value = cmds.attributeQuery(attr_list[0], node=foot_ctrl, range=True)

    # Validate expected range
    if min_value != -10.0 or max_value != 20.0:
        cmds.error(
            f"Attribute {foot_ctrl}.{attr_list[0]} does not have the expected value range of -10 to 20. "
            f"Current range: {min_value} to {max_value}"
        )


    # -----------------------------------------------------------
    # IK handle validation
    # -----------------------------------------------------------

    if not cmds.objExists(leg_ikHandle):
        cmds.error(f"Missing required IK handle: {leg_ikHandle}")

    if cmds.nodeType(leg_ikHandle) != "ikHandle":
        cmds.error(
            f"Received IK handle: {leg_ikHandle} is not an ikHandle. "
            f"Current type: {cmds.nodeType(leg_ikHandle)}"
        )

    return foot_ctrl, foot_joints_IK, foot_joints_bind, leg_ikHandle, limb_side



def creating_unique_node_name(node_type, name):
    if cmds.objExists(name):
        cmds.error(f"Node already exists: {name}")

    return cmds.createNode(node_type, name=name)



class ReverseFootRig:
    def __init__(
            self,
            foot_ctrl,
            foot_joints_IK,
            foot_joints_bind,
            leg_ikHandle,
            limb_side):
        
        # defining UI inputs
        self.foot_ctrl = foot_ctrl
        self.foot_joints_IK = foot_joints_IK
        self.foot_joints_bind = foot_joints_bind
        self.leg_ikHandle = leg_ikHandle
        self.limb_side = limb_side

        # defining pivot nodes
        self.root_pivot = f"{self.limb_side}_root_pivot"
        self.heel_pivot = f"{self.limb_side}_heel_pivot"
        self.inner_pivot = f"{self.limb_side}_inner_pivot"
        self.outer_pivot = f"{self.limb_side}_outer_pivot"
        self.end_pivot = f"{self.limb_side}_end_pivot"
        self.ball_pivot = f"{self.limb_side}_ball_pivot"
        self.ankle_pivot = f"{self.limb_side}_ankle_pivot"
        self.toe_pivot = f"{self.limb_side}_toe_pivot"
        
        # defining condition nodes
        self.ball_condition = None
        self.heel_condition = None
        self.end_condition = None
        self.clamp_condition = None
        self.tiptoe_condition = None
        self.bank_condition = None

        # defining multiplyDivide nodes
        self.multi = None
        self.ball_multi = None
        self.bank_multi = None

        # defining plusMinusAverage nodes
        self.pma = None
        self.ball_pma = None
        self.tiptoe_pma = None

        # defining ikHandles
        self.ball_ikHandle = None
        self.toe_ikHandle = None



    def checking_parenting_and_hierarchy(self):
        # checking if pivot nodes exist
        pivot_list = [
            self.root_pivot,
            self.heel_pivot,
            self.inner_pivot,
            self.outer_pivot,
            self.end_pivot,
            self.ball_pivot,
            self.ankle_pivot,
            self.toe_pivot
        ]

        for pivot in pivot_list:
            # checking if pivot nodes exist
            if not cmds.objExists(pivot):
                cmds.error(f"Missing required pivot node: {pivot}")

            for axis in ["rotateX", "rotateY", "rotateZ"]:
                # checking if pivot nodes have their attributes locked
                if cmds.getAttr(f"{pivot}.{axis}", lock=True):
                    cmds.error(f"Attribute is locked: {pivot}.{axis}")

                # checking if pivot nodes have incoming connections on rotate attribute
                incoming = cmds.listConnections(f"{pivot}.{axis}", source=True, destination=False, plugs=True) or []
                if incoming:
                    cmds.error(f"Attribute already has incoming connection: {pivot}.{axis} from {incoming}")


        expected_chain = [
            self.root_pivot,
            self.heel_pivot,
            self.inner_pivot,
            self.outer_pivot,
            self.end_pivot,
            self.ball_pivot,
            self.ankle_pivot
        ]
        
        for i in range(1, len(expected_chain)): # checking hierarchy from root_pivot to ankle_pivot (excluding toe_pivot here since it is expected to be parented under end_pivot)
            # checking pivot node hierarchy
            child = expected_chain[i]
            expected_parent = expected_chain[i-1]
            parent = cmds.listRelatives(child, parent=True) or []
            if not parent or parent[0] != expected_parent: # if there is no parent (parent is None / 'not parent') or if the parent is not the expected parent
                cmds.error(f"Incorrect hierarchy: {child} should be parented under {expected_parent}") # parent is expected to be the previous pivot in the list


        # toe_pivot node is expected to be parented under end_pivot node
        toe_parent = cmds.listRelatives(self.toe_pivot, parent=True) or []
        if not toe_parent or toe_parent[0] != self.end_pivot:
            cmds.error(f"Incorrect hierarchy: {self.toe_pivot} should be parented under {self.end_pivot}")




    def creating_ikHandles(self):
        # creating ikHandles for foot joints
        self.ball_ikHandle = cmds.ikHandle(name=f"{self.limb_side}_ball_ikHandle", sol="ikSCsolver", sj=self.foot_joints_IK[0], ee=self.foot_joints_IK[1])[0]
        self.toe_ikHandle = cmds.ikHandle(name=f"{self.limb_side}_toe_ikHandle", sol="ikSCsolver", sj=self.foot_joints_IK[1], ee=self.foot_joints_IK[2])[0]

        cmds.parent(self.ball_ikHandle, self.ball_pivot)
        cmds.parent(self.toe_ikHandle, self.toe_pivot)
        cmds.parent(self.leg_ikHandle, self.ankle_pivot)



    def connecting_foot_bind_joints(self):
        # The ankle bind joint is already expected to be driven by the main IK/FK blended leg setup.
        # This reverse foot module only connects the foot/ball and toe bind joints to their IK counterparts.

        ball_IK = self.foot_joints_IK[1]
        toe_IK = self.foot_joints_IK[2]

        ball_bind = self.foot_joints_bind[1]
        toe_bind = self.foot_joints_bind[2]

        connection_pairs = [
            (ball_IK, ball_bind),
            (toe_IK, toe_bind)
        ]

        for IK_joint, bind_joint in connection_pairs:
            for channel in ["translate", "rotate"]:
                incoming = cmds.listConnections(
                    bind_joint + "." + channel,
                    source=True,
                    destination=False,
                    plugs=True
                ) or []

                if incoming:
                    cmds.error(
                        f"{bind_joint}.{channel} already has incoming connection: {incoming}"
                    )

            cmds.parentConstraint(
                IK_joint,
                bind_joint,
                weight=1,
                maintainOffset=False
            )



    def creating_nodes(self):
        # condition node creation
        self.ball_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footRoll_ball_condition")
        self.heel_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footRoll_heel_condition")
        self.end_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footRoll_end_condition")
        self.clamp_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footRoll_clamp_condition")
        self.tiptoe_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footRoll_tiptoe_condition")
        self.bank_condition = creating_unique_node_name("condition", name=f"{self.limb_side}_footBank_condition")

        # multiplyDivide node creation
        self.multi = creating_unique_node_name("multiplyDivide", name=f"{self.limb_side}_footRoll_multi")
        self.ball_multi = creating_unique_node_name("multiplyDivide", name=f"{self.limb_side}_footRoll_ball_multi")
        self.bank_multi = creating_unique_node_name("multiplyDivide", name=f"{self.limb_side}_footBank_multi")

        # plusMinusAverage node creation
        self.pma = creating_unique_node_name("plusMinusAverage", name=f"{self.limb_side}_footRoll_pma")
        self.ball_pma = creating_unique_node_name("plusMinusAverage", name=f"{self.limb_side}_footRoll_ball_pma")
        self.tiptoe_pma = creating_unique_node_name("plusMinusAverage", name=f"{self.limb_side}_footRoll_tiptoe_pma")

        

    def setting_node_specs(self):
            # condition node setting

        # setting second term
        # cmds.setAttr(self.ball_condition + ".secondTerm", 10) # Has been replaced with input from ToeStraightAngle
        cmds.setAttr(self.heel_condition + ".secondTerm", 0)
        cmds.setAttr(self.clamp_condition + ".secondTerm", 0)
        # cmds.setAttr(self.tiptoe_condition + ".secondTerm", 10) # Has been replaced with input from ToeStraightAngle
        cmds.setAttr(self.bank_condition + ".secondTerm", 0)

        # setting colour channels
        # cmds.setAttr(self._condition + ".colorIfTrue", 0)
        # cmds.setAttr(self._condition + ".colorIfFalse", 0)
        cmds.setAttr(self.ball_condition + ".colorIfTrueG", 0)
        cmds.setAttr(self.ball_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.ball_condition + ".colorIfFalseG", 0)
        cmds.setAttr(self.ball_condition + ".colorIfFalseB", 0)

        cmds.setAttr(self.heel_condition + ".colorIfTrueR", 0)
        cmds.setAttr(self.heel_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.heel_condition + ".colorIfFalseG", 0)
        cmds.setAttr(self.heel_condition + ".colorIfFalseB", 0)

        cmds.setAttr(self.end_condition + ".colorIfTrueG", 0)
        cmds.setAttr(self.end_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.end_condition + ".colorIfFalseR", 0)
        cmds.setAttr(self.end_condition + ".colorIfFalseG", 0)
        cmds.setAttr(self.end_condition + ".colorIfFalseB", 0)

        cmds.setAttr(self.clamp_condition + ".colorIfTrueG", 0)
        cmds.setAttr(self.clamp_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.clamp_condition + ".colorIfFalseR", 0)
        cmds.setAttr(self.clamp_condition + ".colorIfFalseG", 0)
        cmds.setAttr(self.clamp_condition + ".colorIfFalseB", 0)

        cmds.setAttr(self.tiptoe_condition + ".colorIfTrueG", 0)
        cmds.setAttr(self.tiptoe_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.tiptoe_condition + ".colorIfFalseR", 0)
        cmds.setAttr(self.tiptoe_condition + ".colorIfFalseG", 0)
        cmds.setAttr(self.tiptoe_condition + ".colorIfFalseB", 0)

        cmds.setAttr(self.bank_condition + ".colorIfTrueG", 0)
        cmds.setAttr(self.bank_condition + ".colorIfTrueB", 0)
        cmds.setAttr(self.bank_condition + ".colorIfFalseR", 0)
        cmds.setAttr(self.bank_condition + ".colorIfFalseB", 0)

        # setting operation
        cmds.setAttr(self.ball_condition + ".operation", 2)
        cmds.setAttr(self.heel_condition + ".operation", 2)
        cmds.setAttr(self.end_condition + ".operation", 2)
        cmds.setAttr(self.clamp_condition + ".operation", 2)
        cmds.setAttr(self.tiptoe_condition + ".operation", 2)
        cmds.setAttr(self.bank_condition + ".operation", 2)


            # multiplyDivide node setting

        # setting inputs
        cmds.setAttr(self.multi + ".input2Z", 15)
        cmds.setAttr(self.ball_multi + ".input2X", 2)
        cmds.setAttr(self.ball_multi + ".input2Y", 1)

        # setting operation
        cmds.setAttr(self.multi + ".operation", 1)
        cmds.setAttr(self.ball_multi + ".operation", 1)
        cmds.setAttr(self.bank_multi + ".operation", 1)


            # plusMinusAverage node setting

        # setting inputs
        # cmds.setAttr(self.pma + ".input1D[1]", 10) # Has been replaced with input from ToeStraightAngle
        # cmds.setAttr(self.ball_pma + ".input1D[0]", 10) # Has been replaced with input from ToeStraightAngle
        # cmds.setAttr(self.tiptoe_pma + ".input1D[1]", 10) # Has been replaced with input from ToeStraightAngle

        # setting operations
        cmds.setAttr(self.pma + ".operation", 2)
        cmds.setAttr(self.ball_pma + ".operation", 2)
        cmds.setAttr(self.tiptoe_pma + ".operation", 2)



    def connecting_nodes(self):
        # maya command that I will use for following connections
        # cmds.connectAttr("senderNode.outputX", "receiverNode.inputX", force=True)

            # condition node connections

        # connection into footRoll_ball_condition
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.ball_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.ball_condition + ".colorIfFalseR", force=True)
        cmds.connectAttr(self.ball_pma + ".output1D", self.ball_condition + ".colorIfTrueR", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeStraightAngle", self.ball_condition + ".secondTerm", force=True)

        # connection into footRoll_heel_condition
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.heel_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.heel_condition + ".colorIfFalseR", force=True)
        cmds.connectAttr(self.ball_condition + ".outColorR", self.heel_condition + ".colorIfTrueG", force=True)

        # connection into footRoll_end_condition
        cmds.connectAttr(self.multi + ".outputZ", self.end_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.multi + ".outputZ", self.end_condition + ".colorIfFalseR", force=True)
        cmds.connectAttr(self.foot_ctrl + ".RollEnd", self.end_condition + ".secondTerm", force=True)
        cmds.connectAttr(self.foot_ctrl + ".RollEnd", self.end_condition + ".colorIfTrueR", force=True)

        # connection into footRoll_clamp_condition
        cmds.connectAttr(self.multi + ".outputY", self.clamp_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.multi + ".outputY", self.clamp_condition + ".colorIfTrueR", force=True)

        # connection into footRoll_tiptoe_condition
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.tiptoe_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.tiptoe_pma + ".output1D", self.tiptoe_condition + ".colorIfTrueR", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeStraightAngle", self.tiptoe_condition + ".secondTerm", force=True)

        # connection into footBank_condition
        cmds.connectAttr(self.foot_ctrl + ".Bank", self.bank_condition + ".firstTerm", force=True)
        cmds.connectAttr(self.foot_ctrl + ".Bank", self.bank_condition + ".colorIfTrueR", force=True)
        cmds.connectAttr(self.foot_ctrl + ".Bank", self.bank_condition + ".colorIfFalseG", force=True)


            # multiplyDivide node connections

        # connection into footRoll_multi
        cmds.connectAttr(self.heel_condition + ".outColorR", self.multi + ".input1X", force=True)
        cmds.connectAttr(self.heel_condition + ".outColorG", self.multi + ".input1Y", force=True)
        cmds.connectAttr(self.foot_ctrl + ".RollBack", self.multi + ".input2X", force=True)
        cmds.connectAttr(self.ball_multi + ".outputY", self.multi + ".input2Y", force=True)
        cmds.connectAttr(self.tiptoe_condition + ".outColorR", self.multi + ".input1Z", force=True)

        # connection into footRoll_ball_multi
        cmds.connectAttr(self.pma + ".output1D", self.ball_multi + ".input1X", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeFlex", self.ball_multi + ".input1Y", force=True)

        # connection into footBank_multi
        cmds.connectAttr(self.foot_ctrl + ".BankMultiplier", self.bank_multi + ".input2X", force=True)
        cmds.connectAttr(self.foot_ctrl + ".BankMultiplier", self.bank_multi + ".input2Y", force=True)
        cmds.connectAttr(self.bank_condition + ".outColorR", self.bank_multi + ".input1X", force=True)
        cmds.connectAttr(self.bank_condition + ".outColorG", self.bank_multi + ".input1Y", force=True)


            # plusMinusAverage node connections

        # connection into footRoll_pma
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.pma + ".input1D[0]", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeStraightAngle", self.pma + ".input1D[1]", force=True)

        # connection into footRoll_ball_pma
        cmds.connectAttr(self.ball_multi + ".outputX", self.ball_pma + ".input1D[1]", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeStraightAngle", self.ball_pma + ".input1D[0]", force=True)

        # connection into footRoll_tiptoe_pma
        cmds.connectAttr(self.foot_ctrl + ".Roll", self.tiptoe_pma + ".input1D[0]", force=True)
        cmds.connectAttr(self.foot_ctrl + ".ToeStraightAngle", self.tiptoe_pma + ".input1D[1]", force=True)


            # pivot node connections

        # connection into heel_pivot
        cmds.connectAttr(self.multi + ".outputX", self.heel_pivot + ".rotateX", force=True) # Foot Roll
        cmds.connectAttr(self.foot_ctrl + ".ToeSway", self.heel_pivot + ".rotateY", force=True)

        # connection into ball_pivot
        cmds.connectAttr(self.clamp_condition + ".outColorR", self.ball_pivot + ".rotateX", force=True)

        # connection into end_pivot
        cmds.connectAttr(self.end_condition + ".outColorR", self.end_pivot + ".rotateX", force=True) # Foot Roll
        cmds.connectAttr(self.foot_ctrl + ".HeelSway", self.end_pivot + ".rotateY", force=True)

        # connection into inner_pivot and outer pivot (banking)
        if self.limb_side == "L":
            cmds.connectAttr(self.bank_multi + ".outputY", self.inner_pivot + ".rotateZ", force=True)
            cmds.connectAttr(self.bank_multi + ".outputX", self.outer_pivot + ".rotateZ", force=True)
        if self.limb_side == "R":
            cmds.connectAttr(self.bank_multi + ".outputX", self.inner_pivot + ".rotateZ", force=True)
            cmds.connectAttr(self.bank_multi + ".outputY", self.outer_pivot + ".rotateZ", force=True)

        # connection into toe_pivot
        cmds.connectAttr(self.foot_ctrl + ".ToeTap", self.toe_pivot + ".rotateX", force=True)





# End






















































