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

st.title("🧪 김도형의 분자 벡터 합성 시뮬레이터 (2D & 3D)")
st.write("평면벡터부터 공간벡터까지: 분자 구조의 기하학적 분석")

# 1. 시뮬레이션 모드 선택
mode = st.sidebar.selectbox("분석 모드 선택", ["2D 평면 분자 (H2O, CO2 등)", "3D 공간 분자 (CH4 메테인)"])

if mode == "2D 평면 분자 (H2O, CO2 등)":
    molecule = st.radio("분자를 선택하세요", ["이산화탄소 (CO₂)", "물 (H₂O)", "폼알데하이드 (CH₂O)", "삼플루오린화붕소 (BF₃)"])
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(0, 0, 'ko', markersize=20, label="Central Atom")
    
    f_vectors = []
    labels = []
    coords = []
    
    if molecule == "이산화탄소 (CO₂)":
        coords = [(-2, 0), (2, 0)]; labels = ["Oxygen (O)", "Oxygen (O)"]
        f_vectors = [np.array([-3, 0]), np.array([3, 0])]
    elif molecule == "물 (H₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2)]; labels = ["Hydrogen (H)", "Hydrogen (H)"]
        f_vectors = [np.array([2, 1.8]), np.array([-2, 1.8])]
    elif molecule == "폼알데하이드 (CH₂O)":
        coords = [(-1.5, -1.2), (1.5, -1.2), (0, 2.5)]; labels = ["Hydrogen (H)", "Hydrogen (H)", "Oxygen (O)"]
        f_vectors = [np.array([1.5, 1.2]), np.array([-1.5, 1.2]), np.array([0, 3.0])]
    elif molecule == "삼플루오린화붕소 (BF₃)":
        coords = [(0, 2.5), (-2.16, -1.25), (2.16, -1.25)]; labels = ["Fluorine (F)", "Fluorine (F)", "Fluorine (F)"]
        f_vectors = [np.array([0, 3.0]), np.array([-2.6, -1.5]), np.array([2.6, -1.5])]

    f_total = sum(f_vectors)
    colors = ['blue', 'green', 'purple']
    for i, (coord, f_vec, label) in enumerate(zip(coords, f_vectors, labels)):
        ax.plot(coord[0], coord[1], 'o', markersize=15, label=f"{label}")
        ax.quiver(0, 0, f_vec[0], f_vec[1], angles='xy', scale_units='xy', scale=1, color=colors[i], alpha=0.7)
    
    if not np.allclose(f_total, [0, 0], atol=1e-2):
        ax.quiver(0, 0, f_total[0], f_total[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label='Net Vector')
    
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True, alpha=0.2); ax.legend()
    st.pyplot(fig)

else:  # 3D 메테인 모드
    st.info("💡 메테인(CH₄): 정사면체 꼭짓점 방향으로 뻗은 4개의 공간벡터를 합하면 영벡터(0,0,0)가 됩니다.")
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 정사면체 기하학적 좌표 설정 (C: 원점, H: 각 꼭짓점)
    h_coords = np.array([[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
    
    # 탄소(C) 원점 표시
    ax.scatter([0], [0], [0], color='black', s=300, label='Carbon (C)')
    
    # 4개의 공간벡터 그리기
    for i, coord in enumerate(h_coords):
        ax.scatter(coord[0], coord[1], coord[2], s=200, label=f'Hydrogen (H){i+1}')
        ax.quiver(0, 0, 0, coord[0], coord[1], coord[2], color='blue', alpha=0.6, arrow_length_ratio=0.1)
        ax.plot([0, coord[0]], [0, coord[1]], [0, coord[2]], color='gray', linestyle='--')

    v_sum = np.sum(h_coords, axis=0)
    st.write(f"📊 **공간벡터 합계 (Σv):** x={v_sum[0]}, y={v_sum[1]}, z={v_sum[2]}")
    
    if np.allclose(v_sum, [0, 0, 0]):
        st.success("✨ 4개의 공간벡터가 3차원 상에서 완벽히 상쇄되어 무극성(영벡터)을 이룹니다.")

    ax.set_xlabel('X-axis'); ax.set_ylabel('Y-axis'); ax.set_zlabel('Z-axis')
    ax.set_title("3D Space Vector Model of Methane (CH₄)")
    ax.legend()
    st.pyplot(fig)
