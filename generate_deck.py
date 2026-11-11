import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Initialize Presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Color Palette (NASA Dark Theme & Aerospace Spec)
BG_COLOR = RGBColor(4, 8, 22)           # #040816 Deep space dark
CARD_BG = RGBColor(14, 27, 56)          # #0E1B38 Glass card base
CARD_BG_ALT = RGBColor(18, 36, 74)      # #12244A Slightly lighter card
CARD_BORDER = RGBColor(38, 72, 130)     # #264882 Subdued blue border
CYAN_ACCENT = RGBColor(0, 242, 255)     # #00F2FF Bright cyan neon
CYAN_GLOW = RGBColor(56, 189, 248)      # #38BDF8 Sky glow
NASA_RED = RGBColor(224, 60, 49)        # #E03C31 NASA Red
NASA_BLUE = RGBColor(11, 61, 145)       # #0B3D91 NASA Meatball Blue
AMBER_WARN = RGBColor(245, 158, 11)     # #F59E0B Warning orange/amber
GREEN_OK = RGBColor(16, 185, 129)       # #10B981 Emerald safe
TEXT_MAIN = RGBColor(248, 250, 252)     # #F8FAFC Crisp white
TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Slate silver
TEXT_SUBTLE = RGBColor(100, 116, 139)   # #64748B Secondary grey

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

def create_base_slide(notes_text=""):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    
    if notes_text:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text
        
    return slide

def add_header(slide, title, category="NASA SPACE APPS CHALLENGE 2026", slide_num=None):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8.0), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = f"// {category.upper()}"
    p_c.font.name = FONT_MONO
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.0), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_MAIN

    # Right telemetry indicator
    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.55), Inches(1.8), Inches(0.5))
        tf_n = num_box.text_frame
        tf_n.word_wrap = False
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"SLIDE [{slide_num:02d}/08]"
        p_n.font.name = FONT_MONO
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = CYAN_GLOW

    # Decorative horizontal line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()

def add_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg
    card.line.color.rgb = border
    card.line.width = Pt(1.2)
    return card

# ==============================================================================
# SLIDE 1: TRANG BÌA (HERO COVER)
# ==============================================================================
s1_notes = """Kính chào ban giám khảo và các bạn, tôi là Vũ Bảo Nam. Hôm nay tôi xin giới thiệu dự án 'Flames in Freefall' – một nền tảng trí tuệ nhân tạo và mô phỏng vật lý chuyên sâu nhằm giải mã hành vi của ngọn lửa trong môi trường vi trọng lực, hướng tới bảo vệ an toàn tính mạng cho các phi hành gia trên trạm ISS và các sứ mệnh Artemis, Sao Hỏa tương lai."""
s1 = create_base_slide(s1_notes)

# Top badge
badge = add_card(s1, Inches(0.8), Inches(1.0), Inches(4.5), Inches(0.45), bg=RGBColor(11, 30, 68), border=CYAN_ACCENT)
tf_b = badge.text_frame
tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
p_b = tf_b.paragraphs[0]
p_b.alignment = PP_ALIGN.CENTER
p_b.text = "NASA SPACE APPS CHALLENGE 2026 // OFFICIAL ENTRY"
p_b.font.name = FONT_MONO
p_b.font.size = Pt(10)
p_b.font.bold = True
p_b.font.color.rgb = CYAN_ACCENT

# Big Project Title
t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.5), Inches(1.6))
tf = t_box.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "FLAMES IN FREEFALL"
p1.font.name = FONT_HEADING
p1.font.size = Pt(54)
p1.font.bold = True
p1.font.color.rgb = TEXT_MAIN

p2 = tf.add_paragraph()
p2.text = "Bảng điều khiển AI phân tích sự cháy trong vi trọng lực & An toàn hỏa hoạn tàu vũ trụ"
p2.font.name = FONT_HEADING
p2.font.size = Pt(20)
p2.font.color.rgb = CYAN_GLOW

# Three Hero Info Cards
col_w = Inches(3.65)
gap = Inches(0.4)
top_y = Inches(3.6)
card_h = Inches(2.6)

# Card 1: Core Combustion Engine
c1 = add_card(s1, Inches(0.8), top_y, col_w, card_h)
tf1 = c1.text_frame
tf1.word_wrap = True
tf1.margin_top = Inches(0.25)
tf1.margin_left = tf1.margin_right = Inches(0.3)

p = tf1.paragraphs[0]
p.text = "CORE COMBUSTION ENGINE"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf1.add_paragraph()
p.text = "Bebo Ignis-0G"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf1.add_paragraph()
p.text = "\n• Mô phỏng động học cháy 3D phi trọng lực\n• Đo lường giới hạn dập tắt bức xạ & đối lưu\n• Đánh giá chỉ số rủi ro tức thời (SFRS 0-100)"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Card 2: Experimental Foundation
c2 = add_card(s1, Inches(0.8) + col_w + gap, top_y, col_w, card_h)
tf2 = c2.text_frame
tf2.word_wrap = True
tf2.margin_top = Inches(0.25)
tf2.margin_left = tf2.margin_right = Inches(0.3)

p = tf2.paragraphs[0]
p.text = "DATA FOUNDATION"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf2.add_paragraph()
p.text = "NASA PSI Informatics"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf2.add_paragraph()
p.text = "\n• SoFIE (Solid Fuel Ignition & Extinction)\n• Saffire (Cygnus large-scale fire tests)\n• BASS-II & FLEX-2 droplet combustion"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Card 3: Author & Attribution
c3 = add_card(s1, Inches(0.8) + (col_w + gap)*2, top_y, col_w, card_h)
tf3 = c3.text_frame
tf3.word_wrap = True
tf3.margin_top = Inches(0.25)
tf3.margin_left = tf3.margin_right = Inches(0.3)

p = tf3.paragraphs[0]
p.text = "LEAD ARCHITECT & RESEARCH LAB"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf3.add_paragraph()
p.text = "Vũ Bảo Nam"
p.font.name = FONT_HEADING
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf3.add_paragraph()
p.text = "\n• Bebo ZeroG-X • VBN Lab (THPT FPT)\n• AI & Space Systems Developer\n• GitHub: github.com/baonamv200/nasa"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Footer spec bar
f_bar = s1.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.4))
tf_f = f_bar.text_frame
p_f = tf_f.paragraphs[0]
p_f.text = "AEROSPACE GRADE PLATFORM // BUILT WITH PYTHON, STREAMLIT & PLOTLY // BILINGUAL VI-EN READY"
p_f.font.name = FONT_MONO
p_f.font.size = Pt(10)
p_f.font.color.rgb = TEXT_SUBTLE

# ==============================================================================
# SLIDE 2: VẤN ĐỀ THỰC TIỄN (THE PROBLEM)
# ==============================================================================
s2_notes = """Trên Trái Đất, trọng lực sinh ra lực đẩy nổi giúp ngọn lửa bốc lên trên và tỏa nhiệt; nhưng trong vi trọng lực, lửa cuộn thành khối cầu xanh tĩnh lặng và cháy âm ỉ mà cảm biến quang học thông thường rất khó phát hiện. Nguy hiểm hơn, hệ thống thông gió bắt buộc trên tàu vũ trụ vô tình biến thành nguồn thổi oxy liên tục, kích hoạt đám cháy bùng phát dữ dội mà không có lối thoát hiểm."""
s2 = create_base_slide(s2_notes)
add_header(s2, "TẠI SAO LỬA NGOÀI KHÔNG GIAN LÀ CƠN ÁC MỘNG?", "PHYSICS PARADOX & THREATS", 2)

col2_w = Inches(5.65)
col2_gap = Inches(0.433)

# Left Column: Earth 1g
c_earth = add_card(s2, Inches(0.8), Inches(1.7), col2_w, Inches(2.9), bg=RGBColor(24, 22, 38), border=RGBColor(90, 60, 40))
tfe = c_earth.text_frame
tfe.word_wrap = True
tfe.margin_left = tfe.margin_right = Inches(0.35)
tfe.margin_top = Inches(0.25)

p = tfe.paragraphs[0]
p.text = "TRÁI ĐẤT (1.0g) - ĐỐI LƯU TỰ NHIÊN"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = AMBER_WARN

p = tfe.add_paragraph()
p.text = "Ngọn lửa hình giọt nước thuôn nhọn (L/W ≈ 3.2)"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfe.add_paragraph()
p.text = "\n• Lực đẩy nổi (buoyancy) kéo khí nóng lên trên, hút khí lạnh và oxy mới vào đáy ngọn lửa.\n• Nhiệt độ đỉnh đạt ~1850 K, muội than phát sáng màu vàng cam rực rỡ, dễ phát hiện từ xa.\n• Dễ dập tắt bằng nước hoặc bình bọt khí CO2 theo cơ chế dội thẳng vào gốc lửa."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Right Column: Space 0g
c_space = add_card(s2, Inches(0.8) + col2_w + col2_gap, Inches(1.7), col2_w, Inches(2.9), bg=RGBColor(10, 28, 60), border=CYAN_ACCENT)
tfs = c_space.text_frame
tfs.word_wrap = True
tfs.margin_left = tfs.margin_right = Inches(0.35)
tfs.margin_top = Inches(0.25)

p = tfs.paragraphs[0]
p.text = "VI TRỌNG LỰC (0.0g) - KHUẾCH TÁN ĐỒNG HƯỚNG"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfs.add_paragraph()
p.text = "Khối cầu lửa màu xanh lam đối xứng (L/W ≈ 1.0)"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfs.add_paragraph()
p.text = "\n• Hoàn toàn triệt tiêu lực đẩy nổi; oxy cung cấp thuần túy bằng khuếch tán phân tử 3D.\n• Nhiệt độ thấp hơn (~1380 K), không có muội than, ngọn lửa xanh mờ vô hình với mắt thường.\n• Cháy âm ỉ cực kỳ bền bỉ và hầu như không tự dập tắt được nếu còn vật liệu cháy."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Two Bottom Callout Banners
b_w = Inches(5.65)
b_h = Inches(1.9)
b_top = Inches(4.9)

# Bottom Left: Cool Flames
b1 = add_card(s2, Inches(0.8), b_top, b_w, b_h, bg=CARD_BG, border=RGBColor(120, 50, 60))
tf_b1 = b1.text_frame
tf_b1.word_wrap = True
tf_b1.margin_left = tf_b1.margin_right = Inches(0.3)
tf_b1.margin_top = Inches(0.2)

p = tf_b1.paragraphs[0]
p.text = "HIỂM HỌA 1: VÙNG NGỌN LỬA LẠNH (COOL FLAMES)"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NASA_RED

p = tf_b1.add_paragraph()
p.text = "Sự cháy diễn ra ở nhiệt độ thấp 500 - 800 K không phát sáng quang học nhưng âm thầm tạo ra lượng lớn khí độc CO và duy trì mầm mống tái bùng phát khi gặp dưỡng khí."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Bottom Right: Ventilation Paradox
b2 = add_card(s2, Inches(0.8) + b_w + col2_gap, b_top, b_w, b_h, bg=CARD_BG, border=CYAN_GLOW)
tf_b2 = b2.text_frame
tf_b2.word_wrap = True
tf_b2.margin_left = tf_b2.margin_right = Inches(0.3)
tf_b2.margin_top = Inches(0.2)

p = tf_b2.paragraphs[0]
p.text = "HIỂM HỌA 2: NGHỊCH LÝ QUẠT THÔNG GIÓ (VENTILATION PARADOX)"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_GLOW

p = tf_b2.add_paragraph()
p.text = "Để phi hành gia thở, trạm vũ trụ bắt buộc duy trì luồng gió 5 - 20 cm/s. Luồng gió này vô tình thổi bạt lớp khí trơ CO2 bảo vệ, cung cấp oxy cưỡng bức làm vật liệu bùng cháy dữ dội."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 3: THÁCH THỨC VỀ DỮ LIỆU (THE DATA CHALLENGE)
# ==============================================================================
s3_notes = """Để có được vài giây dữ liệu đốt cháy ngoài vũ trụ, NASA đã phải phóng các phòng thí nghiệm triệu đô như SoFIE hay đốt cháy cả con tàu chở hàng Cygnus trong dự án Saffire. Tuy nhiên, khối dữ liệu khổng lồ này lại tồn tại dưới dạng các file thô rời rạc, khiến các kỹ sư hàng không vũ trụ và người học rất khó khai thác một cách trực quan và tức thời."""
s3 = create_base_slide(s3_notes)
add_header(s3, "THÁCH THỨC DỮ LIỆU: KHO TÀNG NASA PSI BỊ RỜI RẠC", "MISSION DATA GAP", 3)

# 3 Dataset Cards
col3_w = Inches(3.65)
gap3 = Inches(0.4)
top3 = Inches(1.7)
h3 = Inches(3.0)

# Card 1: SoFIE
cd1 = add_card(s3, Inches(0.8), top3, col3_w, h3)
tfd1 = cd1.text_frame
tfd1.word_wrap = True
tfd1.margin_left = tfd1.margin_right = Inches(0.3)
tfd1.margin_top = Inches(0.25)

p = tfd1.paragraphs[0]
p.text = "DATASET // SOFIE"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfd1.add_paragraph()
p.text = "Solid Fuel Ignition & Extinction"
p.font.name = FONT_HEADING
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfd1.add_paragraph()
p.text = "\n• File: data/sofie_pmma_burn_rates.csv\n• Thử nghiệm đốt thanh nhựa PMMA trên ISS.\n• Biến số: Vận tốc gió (0 - 50 cm/s) và nồng độ oxy cưỡng bức.\n• Trạng thái: Dữ liệu đa kênh phức tạp."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Card 2: Saffire
cd2 = add_card(s3, Inches(0.8) + col3_w + gap3, top3, col3_w, h3)
tfd2 = cd2.text_frame
tfd2.word_wrap = True
tfd2.margin_left = tfd2.margin_right = Inches(0.3)
tfd2.margin_top = Inches(0.25)

p = tfd2.paragraphs[0]
p.text = "DATASET // SAFFIRE"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfd2.add_paragraph()
p.text = "Spacecraft Fire Safety Tests"
p.font.name = FONT_HEADING
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfd2.add_paragraph()
p.text = "\n• File: data/saffire_pressure_oxygen.csv\n• Đốt cháy tấm vải quy mô lớn (1.0m) trên tàu Cygnus trước khi tái nhập khí quyển.\n• Biến số: Suy giảm áp suất và siêu dưỡng khí.\n• Trạng thái: File dữ liệu lớn, khó mô hình hóa."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Card 3: BASS-II & FLEX-2
cd3 = add_card(s3, Inches(0.8) + (col3_w + gap3)*2, top3, col3_w, h3)
tfd3 = cd3.text_frame
tfd3.word_wrap = True
tfd3.margin_left = tfd3.margin_right = Inches(0.3)
tfd3.margin_top = Inches(0.25)

p = tfd3.paragraphs[0]
p.text = "DATASET // BASS-II & FLEX"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfd3.add_paragraph()
p.text = "Burning & Suppression Limits"
p.font.name = FONT_HEADING
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfd3.add_paragraph()
p.text = "\n• File: data/bass_extinction_limits.csv\n• Đo giới hạn nồng độ oxy dập tắt (MOC/LOI).\n• Hơn 15 loại vật liệu hàng không vũ trụ.\n• Trạng thái: Các cột chỉ số thiếu tính liên kết."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Bottom Problem Summary Card
bot_c = add_card(s3, Inches(0.8), Inches(4.9), Inches(11.733), Inches(1.9), bg=RGBColor(26, 20, 36), border=RGBColor(160, 60, 60))
tf_bot = bot_c.text_frame
tf_bot.word_wrap = True
tf_bot.margin_left = tf_bot.margin_right = Inches(0.35)
tf_bot.margin_top = Inches(0.2)

p = tf_bot.paragraphs[0]
p.text = "KHOẢNG CÁCH GIỮA DỮ LIỆU KHOA HỌC VÀ ỨNG DỤNG THỰC TẾ"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = NASA_RED

p = tf_bot.add_paragraph()
p.text = "1. Độ trễ phân tích: Kỹ sư mất nhiều tuần để xử lý dữ liệu phi trọng lực bằng bảng tính thủ công.\n2. Thiếu công cụ giả lập: Phi hành đoàn không có hệ thống trực quan hóa 3D để dự báo nguy cơ trước chuyến bay.\n3. Rào cản tri thức: Các tiêu chuẩn nghiêm ngặt NASA-STD-6001B nằm rải rác trong hàng trăm trang báo cáo PDF phức tạp."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 4: GIẢI PHÁP "FLAMES IN FREEFALL"
# ==============================================================================
s4_notes = """Giải pháp của chúng tôi là 'Flames in Freefall' – một trung tâm chỉ huy số hóa biến dữ liệu thô của NASA thành bảng điều khiển trực quan sinh động. Chỉ bằng việc gạt các thanh trượt trọng lực, oxy hay áp suất, hệ thống sẽ tính toán ngay lập tức chỉ số rủi ro hỏa hoạn SFRS và tái hiện hành vi ngọn lửa trong từng môi trường cabin cụ thể từ trạm ISS tới Sao Hỏa."""
s4 = create_base_slide(s4_notes)
add_header(s4, "GIẢI PHÁP: TRẠM ĐIỀU HÀNH AN TOÀN HỎA HOẠN TÀU VŨ TRỤ", "OUR SOLUTION", 4)

# Left Column: The Dashboard & Risk Score
w_left = Inches(6.8)
c_sol1 = add_card(s4, Inches(0.8), Inches(1.7), w_left, Inches(5.1), bg=CARD_BG, border=CYAN_ACCENT)
tf_s1 = c_sol1.text_frame
tf_s1.word_wrap = True
tf_s1.margin_left = tf_s1.margin_right = Inches(0.35)
tf_s1.margin_top = Inches(0.3)

p = tf_s1.paragraphs[0]
p.text = "NỀN TẢNG MISSION CONTROL // PYTHON & STREAMLIT"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_s1.add_paragraph()
p.text = "Hệ thống Bảng điều khiển Thời gian thực"
p.font.name = FONT_HEADING
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf_s1.add_paragraph()
p.text = "\n• Giao diện chuẩn NASA Web Design System tối ưu cho các trạm mặt đất & trung tâm chỉ huy bay.\n• Biến đổi các tập dữ liệu thực nghiệm PSI rời rạc thành các đồ thị tương tác động.\n• Cho phép phi hành gia & kỹ sư thay đổi tức thời 4 thông số môi trường cabin:"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Inside sub-boxes
p = tf_s1.add_paragraph()
p.text = "\n   [1] Trọng lực: 0.00g (ISS) → 0.16g (Mặt Trăng) → 0.38g (Sao Hỏa) → 1.00g (Trái Đất)\n   [2] Nồng độ Oxy: 14.0% → 100.0% (Giàu dưỡng khí)\n   [3] Áp suất khoang: 25.0 kPa → 105.0 kPa (Tiêu chuẩn khí quyển)\n   [4] Tốc độ lưu thông gió quạt: 0 cm/s (Tĩnh) → 50 cm/s (Gió cưỡng bức)"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.color.rgb = CYAN_GLOW

p = tf_s1.add_paragraph()
p.text = "\n• Chỉ số Rủi ro Hỏa hoạn Vũ trụ (Space Fire Risk Score - SFRS 0-100):\n  Thuật toán tự động xếp hạng an toàn động cho hơn 15 loại vật liệu hàng không vũ trụ."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MAIN

# Right Column: 6 Mission Presets
w_right = Inches(4.5)
c_sol2 = add_card(s4, Inches(0.8) + w_left + Inches(0.4), Inches(1.7), w_right, Inches(5.1), bg=CARD_BG_ALT, border=CARD_BORDER)
tf_s2 = c_sol2.text_frame
tf_s2.word_wrap = True
tf_s2.margin_left = tf_s2.margin_right = Inches(0.3)
tf_s2.margin_top = Inches(0.3)

p = tf_s2.paragraphs[0]
p.text = "6 CẤU HÌNH BAY CHUẨN ĐỊNH"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

presets = [
    ("1. ISS Standard", "0.0g | 21% O2 | 101.3 kPa | 15 cm/s"),
    ("2. Lunar Artemis Base", "0.16g | 34% O2 | 56.5 kPa | 10 cm/s"),
    ("3. Moon Rover Cabin", "0.16g | 30% O2 | 70.3 kPa | 12 cm/s"),
    ("4. EVA Pre-breathe", "0.16g | 100% O2 | 29.6 kPa | 5 cm/s"),
    ("5. Mars Transit Habitat", "0.38g | 26% O2 | 70.0 kPa | 15 cm/s"),
    ("6. Earth Ground Baseline", "1.0g | 21% O2 | 101.3 kPa | 0 cm/s")
]

for name, spec in presets:
    p = tf_s2.add_paragraph()
    p.text = f"\n{name}"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p = tf_s2.add_paragraph()
    p.text = f"  {spec}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN_GLOW

# ==============================================================================
# SLIDE 5: TÍNH NĂNG CỐT LÕI & CÔNG NGHỆ (KEY FEATURES & TECH STACK)
# ==============================================================================
s5_notes = """Sức mạnh của hệ thống nằm ở 3 trụ cột: Khả năng mô phỏng 3D tương tác với Plotly; Thuật toán phân hạng an toàn cho hàng loạt vật liệu tàu vũ trụ; và đặc biệt là hệ thống AI RAG được huấn luyện từ chính các tài liệu kỹ thuật của NASA, giúp kỹ sư tra cứu phương án phản ứng khẩn cấp chỉ trong vài mili-giây."""
s5 = create_base_slide(s5_notes)
add_header(s5, "TÍNH NĂNG CỐT LÕI & NGĂN XẾP CÔNG NGHỆ", "ENGINEERING CAPABILITIES", 5)

col5_w = Inches(3.65)
col5_gap = Inches(0.4)
top5 = Inches(1.7)
h5 = Inches(3.8)

# Pillar 1
p1_card = add_card(s5, Inches(0.8), top5, col5_w, h5)
tf_p1 = p1_card.text_frame
tf_p1.word_wrap = True
tf_p1.margin_left = tf_p1.margin_right = Inches(0.3)
tf_p1.margin_top = Inches(0.25)

p = tf_p1.paragraphs[0]
p.text = "01 // VẬT LÝ & PLOTLY 3D"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_p1.add_paragraph()
p.text = "Mô phỏng Động học Đốt cháy"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf_p1.add_paragraph()
p.text = "\n• Dựng hình thái ngọn lửa 3D (Plotly Mesh3d/Isosurface) theo trường nhiệt độ và vận tốc gió.\n• Đồ thị đường cong dập tắt vi trọng lực hình chữ U (U-Curve): Phân tách rõ Radiative Quenching vs Convective Blowoff.\n• Tính toán nồng độ Oxy hiệu dụng MOC và tốc độ lan truyền ngọn lửa."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Pillar 2
p2_card = add_card(s5, Inches(0.8) + col5_w + col5_gap, top5, col5_w, h5)
tf_p2 = p2_card.text_frame
tf_p2.word_wrap = True
tf_p2.margin_left = tf_p2.margin_right = Inches(0.3)
tf_p2.margin_top = Inches(0.25)

p = tf_p2.paragraphs[0]
p.text = "02 // NASA PSI DATA PIPELINE"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_p2.add_paragraph()
p.text = "Xếp hạng An toàn Vật liệu"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf_p2.add_paragraph()
p.text = "\n• Phân loại tự động hơn 15 vật liệu phi hành (PMMA, Nomex, Kapton, Delrin, Kydex, Mylar, Cotton...).\n• Đối chiếu trực tiếp với tiêu chuẩn vật liệu không gian NASA-STD-6001B.\n• Cảnh báo ngay lập tức các vật liệu nguy hiểm cao trong môi trường giàu oxy của trạm Mặt Trăng Artemis."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Pillar 3
p3_card = add_card(s5, Inches(0.8) + (col5_w + col5_gap)*2, top5, col5_w, h5)
tf_p3 = p3_card.text_frame
tf_p3.word_wrap = True
tf_p3.margin_left = tf_p3.margin_right = Inches(0.3)
tf_p3.margin_top = Inches(0.25)

p = tf_p3.paragraphs[0]
p.text = "03 // AI RAG VECTOR SEARCH"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_p3.add_paragraph()
p.text = "Trợ lý Tư vấn Cứu hỏa Không gian"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tf_p3.add_paragraph()
p.text = "\n• Động cơ Vector Search TF-IDF kết hợp Cosine Similarity tối ưu hóa siêu nhẹ, phản hồi < 4ms.\n• Lập chỉ mục 14 tài liệu NASA Technical Reports.\n• Trích dẫn chính xác số báo cáo, tác giả, và sinh khuyến nghị dập lửa theo thời gian thực."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MUTED

# Tech Stack Banner
ts_card = add_card(s5, Inches(0.8), Inches(5.75), Inches(11.733), Inches(1.1), bg=CARD_BG_ALT, border=CARD_BORDER)
tf_ts = ts_card.text_frame
tf_ts.word_wrap = True
tf_ts.margin_left = tf_ts.margin_right = Inches(0.35)
tf_ts.margin_top = Inches(0.15)

p = tf_ts.paragraphs[0]
p.text = "NGĂN XẾP CÔNG NGHỆ CHÍNH // TECH STACK"
p.font.name = FONT_MONO
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_ts.add_paragraph()
p.text = "Python 3.11  •  Streamlit Core  •  Plotly Interactive 3D  •  NumPy & Pandas  •  Scikit-Learn TF-IDF  •  NASA Web Design System (WDS)"
p.font.name = FONT_HEADING
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 6: KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)
# ==============================================================================
s6_notes = """Về mặt kiến trúc, dự án vận hành theo một luồng xử lý 4 tầng khép kín: Dữ liệu thô từ NASA được đưa vào động cơ Bebo Ignis-0G để giải các phương trình nhiệt động học; kết quả được đối chiếu qua Vector Database tài liệu và hiển thị trực quan lên giao diện Streamlit Cloud, sẵn sàng xuất báo cáo nhiệm vụ cho phi hành đoàn."""
s6 = create_base_slide(s6_notes)
add_header(s6, "KIẾN TRÚC HỆ THỐNG: LUỒNG DỮ LIỆU ĐẾN PHẢN ỨNG KHẨN CẤP", "HOW IT WORKS", 6)

# 4 Horizontal Workflow Steps
step_w = Inches(2.7)
step_gap = Inches(0.31)
step_top = Inches(1.7)
step_h = Inches(3.2)

steps_data = [
    ("STAGE 01", "INGESTION LAYER", "Dữ liệu NASA PSI", 
     "• Ingest CSV thô (SoFIE, Saffire, BASS-II)\n• Cache dữ liệu hàng không dự phòng\n• Chuẩn hóa đơn vị đo đạc SI vũ trụ"),
    ("STAGE 02", "PHYSICS ENGINE", "Bebo Ignis-0G", 
     "• Giải phương trình khuếch tán oxy MOC\n• Tính tỷ số Grashof, Richardson, Peclet\n• Tính điểm nguy hiểm SFRS (0-100)\n• Phát hiện ngọn lửa lạnh Cool Flames"),
    ("STAGE 03", "AI & VECTOR SEARCH", "NASA RAG Advisory", 
     "• Vector TF-IDF 14 báo cáo kỹ thuật\n• Tìm kiếm đối sánh cosine similarity\n• Bridge kết nối Gemini 2.5 Flash / OpenAI\n• Tạo hướng dẫn phản ứng khẩn cấp"),
    ("STAGE 04", "MISSION CONTROL", "Giao diện & Xuất bản", 
     "• Dashboard trực quan hóa Streamlit\n• Biểu đồ Plotly 3D/2D đa biến\n• Ma trận phản ứng dập lửa tức thời\n• Xuất Dossier JSON & Markdown có chữ ký")
]

for i, (stage, name, sub, desc) in enumerate(steps_data):
    x_pos = Inches(0.8) + i * (step_w + step_gap)
    st_card = add_card(s6, x_pos, step_top, step_w, step_h)
    tf_st = st_card.text_frame
    tf_st.word_wrap = True
    tf_st.margin_left = tf_st.margin_right = Inches(0.2)
    tf_st.margin_top = Inches(0.2)
    
    p = tf_st.paragraphs[0]
    p.text = stage
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    p = tf_st.add_paragraph()
    p.text = name
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p = tf_st.add_paragraph()
    p.text = sub
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN_GLOW
    
    p = tf_st.add_paragraph()
    p.text = f"\n{desc}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

# Emergency Action Matrix Callout (Bottom)
bot_proto = add_card(s6, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.7), bg=RGBColor(28, 18, 28), border=RGBColor(180, 50, 50))
tf_pr = bot_proto.text_frame
tf_pr.word_wrap = True
tf_pr.margin_left = tf_pr.margin_right = Inches(0.35)
tf_pr.margin_top = Inches(0.2)

p = tf_pr.paragraphs[0]
p.text = "QUY CHUẨN CỨU HỎA KHẨN CẤP ĐƯỢC TỰ ĐỘNG HÓA // EMERGENCY SUPPRESSION MATRIX"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NASA_RED

p = tf_pr.add_paragraph()
p.text = "1. T+0s đến T+3s: Lập tức cô lập quạt thông gió khoang (HVAC Isolation) nhằm triệt tiêu luồng oxy đối lưu cưỡng bức.\n2. Cấm tuyệt đối tia nước áp lực cao (High-velocity water jets) để tránh làm vỡ vụn nhựa nóng chảy bắn tung tóe trong cabin.\n3. Chỉ định phương án tối ưu: Sử dụng Sương nước siêu mịn (Fine Water Mist < 50 µm) hoặc bơm ngập khí trơ CO2."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 7: Ý NGHĨA & TÁC ĐỘNG (IMPACT & SIGNIFICANCE)
# ==============================================================================
s7_notes = """Flames in Freefall không chỉ là một công cụ phân tích dữ liệu, mà là cẩm nang an toàn sống còn. Dự án giúp các nhà thiết kế tàu vũ trụ ngăn chặn nguy cơ cháy từ khâu chọn vật liệu, cung cấp quy trình dập lửa chuẩn xác để bảo vệ các căn cứ tương lai trên Mặt Trăng và Sao Hỏa, đồng thời truyền cảm hứng khoa học dữ liệu tới cộng đồng STEM."""
s7 = create_base_slide(s7_notes)
add_header(s7, "Ý NGHĨA & TÁC ĐỘNG CHIẾN LƯỢC", "IMPACT & VALUE", 7)

w7 = Inches(3.65)
gap7 = Inches(0.4)
top7 = Inches(1.7)
h7 = Inches(5.1)

# Impact 1: Scientific
c_imp1 = add_card(s7, Inches(0.8), top7, w7, h7)
tfi1 = c_imp1.text_frame
tfi1.word_wrap = True
tfi1.margin_left = tfi1.margin_right = Inches(0.3)
tfi1.margin_top = Inches(0.3)

p = tfi1.paragraphs[0]
p.text = "GIÁ TRỊ 01 // KHOA HỌC"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfi1.add_paragraph()
p.text = "Hiểu sâu Cơ chế Đốt cháy Vi trọng lực"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfi1.add_paragraph()
p.text = "\n• Giải mã nghịch lý thông gió và các hiệu ứng phi tuyến tính khi trọng lực bị triệt tiêu.\n• Xác định chính xác vùng dập tắt bức xạ (Radiative Quenching) khi dòng gió < 3 cm/s.\n• Mô hình hóa hiện tượng ngọn lửa lạnh (Cool Flames) giúp bổ sung các lý thuyết nhiệt động học hàng không vũ trụ hiện đại."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Impact 2: Aerospace Engineering
c_imp2 = add_card(s7, Inches(0.8) + w7 + gap7, top7, w7, h7)
tfi2 = c_imp2.text_frame
tfi2.word_wrap = True
tfi2.margin_left = tfi2.margin_right = Inches(0.3)
tfi2.margin_top = Inches(0.3)

p = tfi2.paragraphs[0]
p.text = "GIÁ TRỊ 02 // THỰC TIỄN VŨ TRỤ"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfi2.add_paragraph()
p.text = "Thiết kế Tàu vũ trụ An toàn hơn"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfi2.add_paragraph()
p.text = "\n• Hỗ trợ trực tiếp cho các sứ mệnh Artemis (Mặt Trăng) và Chuyến bay có người lái lên Sao Hỏa.\n• Giúp các tập đoàn hàng không lựa chọn vật liệu tối ưu theo tiêu chuẩn NASA-STD-6001B.\n• Cung cấp cẩm nang dập lửa khẩn cấp cho phi hành đoàn và quy chuẩn thiết kế luồng gió cabin an toàn."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Impact 3: STEM Education
c_imp3 = add_card(s7, Inches(0.8) + (w7 + gap7)*2, top7, w7, h7)
tfi3 = c_imp3.text_frame
tfi3.word_wrap = True
tfi3.margin_left = tfi3.margin_right = Inches(0.3)
tfi3.margin_top = Inches(0.3)

p = tfi3.paragraphs[0]
p.text = "GIÁ TRỊ 03 // GIÁO DỤC STEM"
p.font.name = FONT_MONO
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tfi3.add_paragraph()
p.text = "Mở hóa Tri thức Khoa học Không gian"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

p = tfi3.add_paragraph()
p.text = "\n• Dân chủ hóa dữ liệu nghiên cứu chuyên sâu của NASA tới học sinh, sinh viên và lập trình viên toàn cầu.\n• Trải nghiệm học tập trực quan qua mô hình 3D thay vì những trang lý thuyết khô khan.\n• Truyền cảm hứng theo đuổi đam mê khám phá vũ trụ và ứng dụng trí tuệ nhân tạo giải quyết bài toán nhân loại."
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 8: ĐỊNH HƯỚNG PHÁT TRIỂN & KẾT LUẬN (ROADMAP & CONCLUSION)
# ==============================================================================
s8_notes = """Trong tương lai, chúng tôi sẽ tích hợp mạng nơ-ron vật lý PINNs và kết nối trực tiếp với cảm biến viễn thám trên trạm không gian để phát hiện cháy tự động. Mời quý vị quét mã QR để trải nghiệm sản phẩm trực tiếp và đóng góp vào kho mã nguồn mở của chúng tôi tại github.com/baonamv200/nasa. Xin chân thành cảm ơn!"""
s8 = create_base_slide(s8_notes)
add_header(s8, "ĐỊNH HƯỚNG PHÁT TRIỂN & KHO MÃ NGUỒN", "FUTURE ROADMAP & CONCLUSION", 8)

# Left Column: 3 Roadmap Milestones
w8_left = Inches(6.8)
c_road = add_card(s8, Inches(0.8), Inches(1.7), w8_left, Inches(5.1), bg=CARD_BG, border=CYAN_GLOW)
tf_r = c_road.text_frame
tf_r.word_wrap = True
tf_r.margin_left = tf_r.margin_right = Inches(0.35)
tf_r.margin_top = Inches(0.3)

p = tf_r.paragraphs[0]
p.text = "LỘ TRÌNH PHÁT TRIỂN TIẾP THEO // ROADMAP 2026 - 2027"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_r.add_paragraph()
p.text = "Hướng đi Chiến lược Nâng tầm Hệ thống"
p.font.name = FONT_HEADING
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = TEXT_MAIN

milestones = [
    ("Giai đoạn 1: Mở rộng Dữ liệu Thực nghiệm từ ISS", 
     "Tích hợp thêm các bộ dữ liệu SoFIE-GEL, SoFIE-MIST và cảm biến ảnh nhiệt đa phổ hồng ngoại."),
    ("Giai đoạn 2: Tối ưu Mô hình bằng Machine Learning (PINNs)", 
     "Huấn luyện mạng nơ-ron vật lý (Physics-Informed Neural Networks) để dự đoán hình thái cháy và rủi ro theo mili-giây."),
    ("Giai đoạn 3: Tích hợp Trực tiếp Cảm biến IoT Tàu vũ trụ", 
     "Kết nối API telemetry khoang tàu theo thời gian thực để kích hoạt hệ thống dập lửa tự động trước khi lửa bùng phát.")
]

for title, desc in milestones:
    p = tf_r.add_paragraph()
    p.text = f"\n• {title}"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p = tf_r.add_paragraph()
    p.text = f"  {desc}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MUTED

# Right Column: Source Code & Call to Action
w8_right = Inches(4.5)
c_cta = add_card(s8, Inches(0.8) + w8_left + Inches(0.4), Inches(1.7), w8_right, Inches(5.1), bg=RGBColor(11, 28, 64), border=CYAN_ACCENT)
tf_cta = c_cta.text_frame
tf_cta.word_wrap = True
tf_cta.margin_left = tf_cta.margin_right = Inches(0.35)
tf_cta.margin_top = Inches(0.3)

p = tf_cta.paragraphs[0]
p.text = "KHO MÃ NGUỒN CÔNG KHAI // OPEN SOURCE"
p.font.name = FONT_MONO
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf_cta.add_paragraph()
p.text = "github.com/baonamv200/nasa"
p.font.name = FONT_MONO
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = CYAN_GLOW

p = tf_cta.add_paragraph()
p.text = "\nTHÔNG TIN TÁC GIẢ & BẢN QUYỀN:\n• Vũ Bảo Nam (Vu Bao Nam)\n• Bebo ZeroG-X • VBN Lab\n• Trường THPT FPT (FPT High School)\n• Dự thi: NASA Space Apps Challenge 2026"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MAIN

p = tf_cta.add_paragraph()
p.text = "\nTRẢI NGHIỆM DỰ ÁN TRỰC TUYẾN:\n• Web App: flames-in-freefall.streamlit.app\n• Mã nguồn mở hoàn toàn theo giấy phép MIT\n• Sẵn sàng thử nghiệm trên Streamlit Cloud"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.color.rgb = TEXT_MUTED

p = tf_cta.add_paragraph()
p.text = "\nCẢM ƠN QUÝ BAN GIÁM KHẢO!"
p.font.name = FONT_HEADING
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

# Save presentation
output_path = "Flames_in_Freefall_Presentation.pptx"
prs.save(output_path)
print(f"SUCCESS: Presentation successfully generated at: {output_path}")

