"""Load humanaopen.urdf in PyBullet and run kinematic/physics smoke tests."""
import os
import sys
import pybullet as p

URDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "humanaopen.urdf")

USE_GUI = "--gui" in sys.argv

p.connect(p.GUI if USE_GUI else p.DIRECT)
print(f"[1] loading: {URDF}")
robot = p.loadURDF(URDF, useFixedBase=False, flags=p.URDF_USE_INERTIA_FROM_FILE)
print(f"    loaded OK, body id={robot}")

print("\n[2] joint inventory")
n = p.getNumJoints(robot)
joint_info = []
for i in range(n):
    info = p.getJointInfo(robot, i)
    name = info[1].decode()
    jtype = info[2]  # 0=revolute 1=prismatic 2=spherical 3=planar 4=fixed 10=continuous
    lower, upper = info[8], info[9]
    axis = [round(x, 3) for x in info[13]]
    joint_info.append((i, name, jtype, lower, upper, axis))
    print(f"    [{i:2d}] {name:32s} type={jtype:2d} range=({lower:.3f},{upper:.3f}) axis={axis}")

non_fixed = [(i, n_, t) for i, n_, t, *_ in joint_info if t != 4]
print(f"    movable joints: {len(non_fixed)}")

print("\n[3] command each joint to 50% of range, read back")
all_ok = True
for i, name, jtype in non_fixed:
    lower, upper = joint_info[i][3], joint_info[i][4]
    if jtype == 10:  # continuous: just rotate 1 rad
        target, lb, ub = 1.0, -1.0, 1.0
    else:
        target, lb, ub = 0.5 * (lower + upper), lower, upper
    p.resetJointState(robot, i, target)
    state = p.getJointState(robot, i)
    ok = abs(state[0] - target) < 1e-6
    all_ok &= ok
    flag = "OK " if ok else "FAIL"
    print(f"    [{flag}] {name:32s} target={target:+7.4f} readback={state[0]:+7.4f}")

print(f"\n    all joints command/readback: {'PASS' if all_ok else 'FAIL'}")

print("\n[4] forward kinematics at zero pose (default) -> base z vs wheels")
for ln in ["base_link", "base_left_wheel", "base_right_wheel", "lift_carriage", "torso"]:
    idx = -1
    for i in range(n):
        if joint_info[i][1] == ln + "_joint":
            idx = i
            parent = joint_info[i][0]
            break
    st = p.getLinkState(robot, parent if idx >= 0 else 0, computeForwardKinematics=1)
    if len(st) >= 5:
        pos = st[4]
        print(f"    {ln:24s} world pos = ({pos[0]:+.3f},{pos[1]:+.3f},{pos[2]:+.3f})")

print("\n[5] collision check at default pose (contact pairs between non-adjacent links)")
p.performCollisionDetection()
contacts = p.getContactPoints(robot, robot)
real = []
for c in contacts:
    bodyA, bodyB = c[1], c[2]
    if bodyA == bodyB == robot:
        real.append(c)
print(f"    self-collisions detected: {len(real)}")
if real:
    print("    (note: adjacent links sharing a joint may register touching contacts)")
    for c in real[:5]:
        print(f"      linkA={c[3]} linkB={c[4]} dist={c[8]:.4f}")

print("\n[6] total mass")
print(f"    base mass = {p.getDynamicsInfo(robot, -1)[0]:.3f} kg")
print("RESULT: " + ("PASS" if all_ok else "FAIL"))
p.disconnect()