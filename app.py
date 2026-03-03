import plotly.express as px
import streamlit as st
import random
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Mô phỏng đầu tư", layout="wide")
st.markdown("""
<style>

/* Nền chính */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Tiêu đề lớn */
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #FFD700;
    text-align: center;
}

/* Box hiển thị số */
.metric-box {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

/* Số lớn */
.big-number {
    font-size: 28px;
    font-weight: bold;
    color: #00FF99;
}

/* Nội dung mô tả */
.description {
    font-size: 16px;
    color: white;
}

/* Section title */
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #FFD700;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📈 XÂY DỰNG HỆ THỐNG MÔ PHỎNG CHIẾN LƯỢC ĐẦU TƯ TÀI CHÍNH BẰNG LÃI KÉP</div>', unsafe_allow_html=True)

# ===== NHẬP DỮ LIỆU =====
st.sidebar.header("Nhập thông tin đầu tư")

von_ban_dau = st.sidebar.number_input("Vốn ban đầu (VND)", value=10000000)
lai_suat = st.sidebar.number_input("Lãi suất năm (%)", value=5.0) / 100
so_nam = st.sidebar.number_input("Số năm đầu tư", min_value=1, max_value=50, value=5)
gui_them_thang = st.sidebar.number_input("Gửi thêm mỗi tháng (VND)", value=1000000)
do_bien_dong = st.sidebar.slider("Độ biến động năm (%)", 5, 40, 20) /100
lam_phat = st.sidebar.number_input("Lạm phát năm (%)", value=3.0) / 100
so_lan_mo_phong = 1000

# ===== TÍNH TOÁN =====

ket_qua = []
all_paths = []

for simulation in range(so_lan_mo_phong):

    tien = von_ban_dau
    path = []

    for i in range(so_nam * 12):

        # Lợi suất kỳ vọng tháng
        mean_month = lai_suat / 12

        # Độ biến động tháng (chuẩn hóa theo năm)
        std_month = do_bien_dong / np.sqrt(12)

        # Sinh lợi suất ngẫu nhiên theo phân phối chuẩn
        random_return = np.random.normal(mean_month, std_month)

        # Cập nhật tiền
        tien = tien * (1 + random_return) + gui_them_thang

        # Trừ lạm phát
        tien *= (1 - lam_phat/12)

        path.append(tien)

    all_paths.append(path)
    ket_qua.append(tien)

# Chuyển sang mảng numpy
all_paths_array = np.array(all_paths)

# Trung bình theo từng tháng
mean_path = np.mean(all_paths_array, axis=0)

# P5 và P95 theo từng tháng
p5_path = np.percentile(all_paths_array, 5, axis=0)
p95_path = np.percentile(all_paths_array, 95, axis=0)

# ===== TÍNH THỐNG KÊ MONTE CARLO =====
trung_binh = sum(ket_qua) / len(ket_qua)
tot_nhat = max(ket_qua)
xau_nhat = min(ket_qua)

# Phần trăm xác suất lời
tong_von_bo_vao = von_ban_dau + gui_them_thang * so_nam * 12
so_lan_loi = len([x for x in ket_qua if x > tong_von_bo_vao])
xac_suat_loi = so_lan_loi / so_lan_mo_phong * 100
#====== TÍNH PERCEMTILE =======
p5 = sorted(ket_qua)[int(0.05*so_lan_mo_phong)]
p95 = sorted(ket_qua)[int(0.95*so_lan_mo_phong)]

loi_nhuan_tb = trung_binh - tong_von_bo_vao
ty_suat_loi_tb = (loi_nhuan_tb / tong_von_bo_vao) * 100

# ===== HIỂN THỊ KẾT QUẢ =====

st.markdown(
    "<h2 style='color:white;'>📊 Tổng quan đầu tư</h2>",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="section-title">📈 Xác suất sinh lời</div>
        <div class="big-number">{round(xac_suat_loi,1)}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    if ty_suat_loi_tb >= 0:
        delta_color = "#00FF88"
        delta_icon = "▲"
        delta_sign = "+"
    else:
        delta_color = "#FF4B4B"
        delta_icon = "▼"
        delta_sign = ""

    st.markdown(f"""
    <div class="metric-box">
        <div class="section-title">💰 Giá trị trung bình</div>
        <div class="big-number">{round(trung_binh,0):,.0f} VND</div>
        <div style="
            margin-top:10px;
            font-size:18px;
            font-weight:bold;
            color:{delta_color};
        ">
            {delta_icon} {delta_sign}{round(ty_suat_loi_tb,2)}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="section-title">🔻 Rủi ro thấp (P5)</div>
        <div class="big-number">{p5:,.0f} VND</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="section-title">🚀 Tiềm năng cao (P95)</div>
        <div class="big-number">{p95:,.0f} VND</div>
    </div>
    """, unsafe_allow_html=True)
if do_bien_dong < 0.15:
    st.success("📗 Mức rủi ro: Thấp")
elif do_bien_dong < 0.25:
    st.warning("📙 Mức rủi ro: Trung bình")
else:
    st.error("📕 Mức rủi ro: Cao")

# ===== VẼ BIỂU ĐỒ =====
data1 = [x/1_000_000 for x in mean_path]

thang_list = list(range(1, len(data1)+1))

fig = go.Figure()

# vẽ 1000 đường đầu cho nhẹ máy
for path in all_paths[:1000]:
    fig.add_trace(go.Scatter(
        y=[x/1_000_000 for x in path],
        mode='lines',
        line=dict(width=1),
        opacity=0.2,
        showlegend=False
    ))
# ===== VẼ ĐƯỜNG TRUNG BÌNH =====
fig.add_trace(go.Scatter(
    y=[x/1_000_000 for x in mean_path],
    mode='lines',
    line=dict(width=4, color='#00BFFF'),
    name='Trung bình'
))

# ===== VẼ P5 =====
fig.add_trace(go.Scatter(
    y=[x/1_000_000 for x in p5_path],
    mode='lines',
    line=dict(width=3, dash='dash', color='red'),
    name='P5 (5% xấu nhất)'
))

# ===== VẼ P95 =====
fig.add_trace(go.Scatter(
    y=[x/1_000_000 for x in p95_path],
    mode='lines',
    line=dict(width=3, dash='dash', color='green'),
    name='P95 (5% tốt nhất)'
))

# ===== TÔ VÙNG AN TOÀN (GIỮA P5 VÀ P95) =====
fig.add_trace(go.Scatter(
    y=[x/1_000_000 for x in p95_path],
    mode='lines',
    line=dict(width=0),
    showlegend=False
))

fig.add_trace(go.Scatter(
    y=[x/1_000_000 for x in p5_path],
    mode='lines',
    fill='tonexty',
    fillcolor='rgba(255,165,0,0.2)',
    line=dict(width=0),
    name='Vùng rủi ro'
))
fig.update_layout(
    title="Monte Carlo Simulation (1000 đường mô phỏng)",
    xaxis_title="Tháng",
    yaxis_title="Số tiền (Triệu VND)"
)
fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
fig.update_layout(
    font=dict(color="white"),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
)

fig.update_xaxes(
    color="white",
    showgrid=True,
    gridcolor="rgba(255,255,255,0.1)"
)

fig.update_yaxes(
    color="white",
    showgrid=True,
    gridcolor="rgba(255,255,255,0.1)"
)
st.plotly_chart(fig, use_container_width=True)

fig2 = px.histogram(
    ket_qua,
    nbins=50,
    title="Phân phối kết quả sau mô phỏng Monte Carlo",
    labels={"value": "Giá trị cuối kỳ (VND)"}
)

# Thêm đường P5
fig2.add_vline(
    x=p5,
    line_width=3,
    line_dash="dash",
    line_color="red",
    annotation_text="P5",
    annotation_position="top left"
)

# Thêm đường P95
fig2.add_vline(
    x=p95,
    line_width=3,
    line_dash="dash",
    line_color="green",
    annotation_text="P95",
    annotation_position="top right"
)
fig2.update_layout(
    template="plotly_dark",
    font=dict(color="white"),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    hovermode="x unified"
)

fig2.update_xaxes(
    color="white",
    showgrid=True,
    gridcolor="rgba(255,255,255,0.1)"
)

fig2.update_yaxes(
    color="white",
    showgrid=True,
    gridcolor="rgba(255,255,255,0.1)"
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown(
f"""
<div style="
    background-color:#1E1E1E;
    padding:25px;
    border-radius:15px;
    color:white;
    margin-top:30px;
">

<h3 style="margin-top:0;">🧠 Nhận định mô phỏng</h3>

Với mức lợi suất <b>{lai_suat*100:.1f}%</b> 
và độ biến động <b>{do_bien_dong*100:.0f}%</b>, 
xác suất sinh lời đạt 
<span style="color:#00FFAA; font-weight:bold;">
{round(xac_suat_loi,1)}%
</span>, 
khoảng 90% kết quả nằm trong vùng từ 
<b>{round(p5/1e6)} triệu</b> đến 
<b>{round(p95/1e6)} triệu VND</b>.

</div>
""",
unsafe_allow_html=True
)



