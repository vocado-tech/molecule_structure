import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 그래프 내부 한글 깨짐을 방지하기 위해, 그래프 내부 텍스트는 영문(C, O, H, F 등)으로 처리함
plt.rc('axes', unicode_minus=False)

# 🎈 왼쪽 하단에 고정되어 떠다니는 말풍선 CSS 및 HTML 추가
st.markdown(
    """
    <style>
    .floating-bubble {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background-color: #ff4b4b;
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
        font-size: 14px;
        font-weight: bold;
        z-index: 9999;
        animation: floatAnimation 3s ease-in-out infinite;
    }
    
    /* 말풍선 꼬리 모양 */
    .floating-bubble::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 20px;
        border-width: 8px 8px 0;
        border-style: solid;
        border-color: #ff4b4b transparent;
        display: block;
        width: 0;
    }

    /* 위아래로 부드럽게 흔들리는 애니메이션 효과 */
    @keyframes floatAnimation {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
    <div class="floating-bubble">
        기하는 너무 어려워 ㅠㅠ
    </div>
    """,
    unsafe_allow_html=True
)

# 타이틀 수정 및 서브 캡션 추가
st.title("🧪 분자 벡터 합성 시뮬레이터 (2D & 3D)")
st.caption("제작: 김도형")
st.write("평면벡터부터 공간벡터까지: 분자 구조의 기하학적 분석")

# 사이드바에 폴링 전기음성도 정보 제공 (의예과 물리화학/유기화학 기초 개념)
st.sidebar.markdown("### 📊 Pauling Electronegativity")
st.sidebar.code(
    "F : 3.98\n"
    "O : 3.44\n"
    "C : 2.55\n"
    "H : 2.20\n"
    "B : 2.04"
)

# 1. 시뮬레이션 모드 선택
mode = st.sidebar.selectbox("분석 모드 선택", ["2D 평면 분자 (H2O, CO2 등)", "3D 공간 분자 (CH4 메테인)"])

if mode == "2D 평면 분자 (H2O, CO2 등)":
    molecule = st.radio("분자를 선택하세요", ["이산화탄소 (CO₂)", "물 (H₂O)", "폼알데하이드 (CH₂O)", "삼플루오린화붕소 (BF₃)"])
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(0, 0, 'ko', markersize=22, label="Central Atom")
    
    f_vectors = []
    labels = []
    coords = []
    bond_desc = ""
    
    # 실제 결합 길이(Å) 및 전기음성도 차이에 기반한 벡터 설계
    if molecule == "이산화탄소 (CO₂)":
        # C-O 결합 길이: ~1.16 Å, 전기음성도 차이: 3.44 - 2.55 = 0.89
        coords = [(-1.16, 0), (1.16, 0)]
        labels = ["Oxygen (O)", "Oxygen (O)"]
        # 전자는 탄소(C)에서 산소(O) 방향으로 끌림
        f_vectors = [np.array([-0.89, 0]), np.array([0.89, 0])]
        bond_desc = "C=O 쌍극자 모멘트 크기: 0.89 (방향: 외곽 산소 방향)"
        
    elif molecule == "물 (H₂O)":
        # O-H 결합 길이: ~0.96 Å, 결합각: 104.5도
        # 전기음성도 차이: 3.44 - 2.20 = 1.24
        angle_rad = np.radians(104.5 / 2)
        h_x = 0.96 * np.sin(angle_rad)
        h_y = -0.96 * np.cos(angle_rad)
        coords = [(-h_x, h_y), (h_x, h_y)]
        labels = ["Hydrogen (H)", "Hydrogen (H)"]
        # 전자는 수소(H)에서 산소(O) 방향으로 끌림 (안쪽으로 합산)
        f_vectors = [
            np.array([1.24 * np.sin(angle_rad), 1.24 * np.cos(angle_rad)]),
            np.array([-1.24 * np.sin(angle_rad), 1.24 * np.cos(angle_rad)])
        ]
        bond_desc = "O-H 쌍극자 모멘트 크기: 1.24 (방향: 중앙 산소 방향)"
        
    elif molecule == "폼알데하이드 (CH₂O)":
        # C=O 결합 길이: ~1.20 Å, C-H 결합 길이: ~1.10 Å, H-C-H 각도: ~116도
        # C-H 차이: 2.55 - 2.20 = 0.35 (탄소 방향으로 끌림)
        # C-O 차이: 3.44 - 2.55 = 0.89 (산소 방향으로 끌림)
        angle_rad = np.radians(116 / 2)
        h_x = 1.10 * np.sin(angle_rad)
        h_y = -1.10 * np.cos(angle_rad)
        coords = [(-h_x, h_y), (h_x, h_y), (0, 1.20)]
        labels = ["Hydrogen (H)", "Hydrogen (H)", "Oxygen (O)"]
        f_vectors = [
            np.array([0.35 * np.sin(angle_rad), 0.35 * np.cos(angle_rad)]), # H1 -> C
            np.array([-0.35 * np.sin(angle_rad), 0.35 * np.cos(angle_rad)]), # H2 -> C
            np.array([0, 0.89]) # C -> O
        ]
        bond_desc = "C-H 극성: 0.35 (안쪽), C=O 극성: 0.89 (바깥쪽)"
        
    elif molecule == "삼플루오린화붕소 (BF₃)":
        # B-F 결합 길이: ~1.30 Å, 결합각: 120도
        # 전기음성도 차이: 3.98 - 2.04 = 1.94
        # 전자는 붕소(B)에서 플루오린(F) 방향으로 끌림
        coords = [
            (0, 1.30),
            (1.30 * np.cos(np.radians(210)), 1.30 * np.sin(np.radians(210))),
            (1.30 * np.cos(np.radians(330)), 1.30 * np.sin(np.radians(330)))
        ]
        labels = ["Fluorine (F)", "Fluorine (F)", "Fluorine (F)"]
        f_vectors = [
            np.array([0, 1.94]),
            np.array([1.94 * np.cos(np.radians(210)), 1.94 * np.sin(np.radians(210))]),
            np.array([1.94 * np.cos(np.radians(330)), 1.94 * np.sin(np.radians(330))])
        ]
        bond_desc = "B-F 쌍극자 모멘트 크기: 1.94 (방향: 외곽 플루오린 방향)"

    f_total = sum(f_vectors)
    colors = ['blue', 'green', 'purple']
    
    # 구조적 선(결합) 및 원자 플로팅
    for i, (coord, f_vec, label) in enumerate(zip(coords, f_vectors, labels)):
        ax.plot([0, coord[0]], [0, coord[1]], color='gray', linestyle=':', linewidth=1.5)
        ax.plot(coord[0], coord[1], 'o', markersize=16, label=f"{label}")
        # quiver를 사용하여 실제 물리 크기에 비례하도록 벡터 스케일링 (scale_units='xy', scale=1)
        ax.quiver(0, 0, f_vec[0], f_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[i], alpha=0.7)
    
    # 합산 알짜 벡터(Net Dipole Moment) 플로팅
    if not np.allclose(f_total, [0, 0], atol=1e-2):
        ax.quiver(0, 0, f_total[0], f_total[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label='Net Vector')
        st.write(f"📊 **알짜 쌍극자 모멘트 벡터 합계:** x={f_total[0]:.2f}, y={f_total[1]:.2f}")
    else:
        st.success("✨ 대칭 구조로 인해 극성 벡터의 합이 완벽히 0(영벡터)이 되며, 무극성 분자입니다.")
    
    st.info(f"🔬 **물리화학적 데이터 분석:**\n* {bond_desc}")
    
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axhline(0, color='black', linewidth=0.5, alpha=0.3)
    ax.axvline(0, color='black', linewidth=0.5, alpha=0.3)
    ax.grid(True, alpha=0.2)
    ax.legend(loc='upper right')
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 메테인(CH₄): 정사면체 중심의 탄소(2.55)가 외곽 수소(2.20)보다 음성도가 커서, 4개의 정사면체 꼭짓점 방향에서 중심 원점 방향으로 벡터가 모입니다.")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # C-H 결합 길이: ~1.09 Å
    # 정사면체 기하학적 좌표 설정 (C: 원점, H: 각 꼭짓점)
    scale = 1.09 / np.sqrt(3)
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]]) * scale
    
    # 탄소(C) 원점 표시
    ax.scatter([0], [0], [0], color='black', s=350, label='Carbon (C)')
    
    # H -> C 로 향하는 극성 벡터 플로팅 (음성도 차이: 2.55 - 2.20 = 0.35)
    # 각 수소 원자의 위치에서 원점(0,0,0) 방향으로 크기 0.35의 벡터가 가해짐
    f_vectors_3d = []
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'Hydrogen (H){i+1}')
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')
        
        # 단위 방향 벡터 계산 후 전기음성도 차이(0.35) 반영
        unit_dir = -coord / np.linalg.norm(coord)
        v_polar = unit_dir * 0.35
        f_vectors_3d.append(v_polar)
        
        # 화살표 시작 지점을 수소 원자 위치로 잡아 안쪽(탄소)으로 쏠리도록 그림
        ax.quiver(coord[0], coord[1], coord[2], v_polar[0], v_polar[1], v_polar[2], 
                  color='blue', alpha=0.7, arrow_length_ratio=0.25)

    v_sum = np.sum(f_vectors_3d, axis=0)
    st.write(f"📊 **3차원 공간벡터 합계 (Σv):** x={v_sum[0]:.3f}, y={v_sum[1]:.3f}, z={v_sum[2]:.3f}")
    
    if np.allclose(v_sum, [0, 0, 0], atol=1e-2):
        st.success("✨ 4개의 공간 극성 벡터가 완벽히 상쇄되어 합이 영벡터(0,0,0)가 되므로 무극성입니다.")

    # 그래프 스케일 보정
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlim(-1.5, 1.5)
    ax.set_title("3D Space Vector Model of Methane (CH₄)")
    ax.legend()
    st.pyplot(fig)
