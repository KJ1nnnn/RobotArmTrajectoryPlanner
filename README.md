# AI Robot Arm Control Lab

로봇 팔의 기본 움직임을 Python으로 학습하기 위한 입문용 프로젝트입니다.

현재 프로젝트는 **2D 로봇 팔 시뮬레이터**와 **Trajectory Planning Simulator**를
포함합니다. 두 개의 링크를 가진 평면 로봇 팔을 모델링하고, forward
kinematics, inverse kinematics, waypoint 기반 경로 생성, joint angle 경로 변환,
matplotlib 시각화를 다룹니다.

## 프로젝트 단계

- Phase 1: 기본 2D 로봇 팔 시뮬레이터
- Phase 1.5: trajectory planning simulator
- Future Phase 2: PID control

현재 단계에서는 시뮬레이터와 trajectory planning에만 집중합니다. 아직 PID 제어,
AI, OpenCV, reinforcement learning, LeRobot, 하드웨어 제어는 포함하지 않습니다.

## 앞으로의 로드맵

- Phase 2: PID control
- Phase 3: OpenCV object detection
- Phase 4: simple AI policy model
- Phase 5: LeRobot/SO-ARM101 extension

## 설치 방법

가상환경을 만들고 활성화합니다.

```bash
python -m venv .venv
source .venv/bin/activate
```

필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 기본 시뮬레이터 실행

프로젝트 루트에서 아래 명령어를 실행합니다.

```bash
python scripts/run_simulator.py
```

이 스크립트는 두 링크 로봇 팔을 만들고, 목표 좌표로 이동한 결과를 matplotlib으로
보여줍니다.

시뮬레이터 창에서는 base 위치, 현재 end-effector 위치, target 위치를 확인할 수
있습니다. 입력창에 새로운 target `x`, `y` 값을 넣고 **Move** 버튼을 누르면 로봇
팔이 해당 위치로 이동합니다.

## Trajectory Demo 실행

프로젝트 루트에서 아래 명령어를 실행합니다.

```bash
python scripts/run_trajectory_demo.py
```

이 데모는 여러 waypoint를 연결해 cartesian path를 만들고, 그 경로를 joint angle
path로 변환한 뒤 로봇 팔이 계획된 경로를 따라 움직이는 모습을 애니메이션으로
보여줍니다.

trajectory demo에서는 다음 기능을 확인할 수 있습니다.

- end-effector가 따라가는 경로 시각화
- circular obstacle 충돌 여부 확인
- `Retry` 버튼으로 애니메이션 다시 시작
- `Stop` 버튼으로 애니메이션 정지
- 현재 end-effector의 `x`, `y` 좌표 수치 표시

## 테스트 실행

프로젝트 루트에서 아래 명령어를 실행합니다.

```bash
pytest
```

테스트는 forward kinematics, inverse kinematics, `RobotArm2D` 기본 동작,
trajectory planning, obstacle check, trajectory animation UI를 확인합니다.
