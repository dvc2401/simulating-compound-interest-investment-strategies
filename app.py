import plotly.express as px
import streamlit as st
import random
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Mô phỏng đầu tư", layout="wide")

st.title("📈 MÔ PHỎNG CHIẾN LƯỢC ĐẦU TƯ LÃI KÉP")

# ===== NHẬP DỮ LIỆU =====
st.sidebar.header("Nhập thông tin đầu tư")

von_ban_dau = st.sidebar.number_input("Vốn ban đầu (VND)", value=10000000)
lai_suat = st.sidebar.number_input("Lãi suất năm (%)", value=7.0) / 100
so_nam = st.sidebar.number_input("Số năm đầu tư", min_value=1, max_value=50, value=10)
gui_them_thang = st.sidebar.number_input("Gửi thêm mỗi tháng (VND)", value=2000000)
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

st.metric("P5 (5% xấu nhất)", f"{round(p5,0):,.0f} VND")
st.metric("P95 (5% tốt nhất)", f"{round(p95,0):,.0f} VND")

# ===== HIỂN THỊ KẾT QUẢ =====
st.subheader("📊 Kết quả Monte Carlo (1000 lần mô phỏng)")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Trung bình", f"{round(trung_binh,0):,.0f} VND")
col2.metric("🚀 Tốt nhất", f"{round(tot_nhat,0):,.0f} VND")
col3.metric("⚠️ Xấu nhất", f"{round(xau_nhat,0):,.0f} VND")
col4, col5, col6 = st.columns(3)
col4.metric("📈 Xác suất lời", f"{round(xac_suat_loi,2)} %")
col5.metric("🔻 P5 (5% xấu nhất)", f"{round(p5,0):,.0f} VND")
col6.metric("🔺 P95 (5% tốt nhất)", f"{round(p95,0):,.0f} VND")

# ===== VẼ BIỂU ĐỒ =====
data1 = [x/1_000_000 for x in mean_path]
data2 = [x/1_000_000 for x in mean_path]
data3 = [x/1_000_000 for x in mean_path]

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
    line=dict(width=4, color='blue'),
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
    fillcolor='rgba(255,0,0,0.2)',
    line=dict(width=0),
    name='Vùng rủi ro'
))
fig.update_layout(
    title="Monte Carlo Simulation (1000 đường mô phỏng)",
    xaxis_title="Tháng",
    yaxis_title="Số tiền (Triệu VND)"
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

st.plotly_chart(fig2, use_container_width=True)


