import flet as ft


def main(page: ft.Page):
    page.title = "Dividend Calculator"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # Color Palette Definitions
    PRIMARY_BLUE = "#1565C0"       # Blue 800
    ACCENT_GREEN = "#2E7D32"       # Green 700
    LIGHT_GREEN = "#E0F2F1"        # Teal 50
    BORDER_COLOR = "#90CAF9"       # Blue 200
    TEXT_GREY_600 = "#757575"
    TEXT_GREY_700 = "#616161"
    SHADOW_COLOR = "#CFD8DC"

    # Alignment definitions safe across all Flet versions
    ALIGN_TOP_LEFT = ft.Alignment(-1.0, -1.0)
    ALIGN_BOTTOM_RIGHT = ft.Alignment(1.0, 1.0)
    ALIGN_TOP_CENTER = ft.Alignment(0.0, -1.0)

    # State variables
    num_shares = 0
    buy_price = 0.0
    face_value = 0
    q1 = 0.0
    q2 = 0.0
    q3 = 0.0
    q4 = 0.0
    filer_status = None

    # Title Section
    title_text = ft.Text(
        "Dividend Calculator", size=22, weight=ft.FontWeight.BOLD, color=ACCENT_GREEN
    )
    by_text = ft.Text(
        "by M.Z. for Pakistan Stock Exchange", italic=True, color=TEXT_GREY_600
    )

    logo = ft.Image(src="/Pakistan_Stock_Exchange_logo.png", width=36, height=36)

    title_row = ft.Row(
        [title_text, logo], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Investment Result Display
    investment_text = ft.Text(
        "Rs. 0.00",
        size=18,
        weight=ft.FontWeight.W_600,
        color=ACCENT_GREEN,
    )

    # Dividend For Label
    dividend_for_text = ft.Text(
        "Enter Dividends announced:",
        size=16,
        weight=ft.FontWeight.W_500,
        color=PRIMARY_BLUE,
    )

    # Calculation Outcome Controls
    out_pct_val = ft.Text("0.00%", size=20, weight=ft.FontWeight.BOLD, color=ACCENT_GREEN)
    out_gain_val = ft.Text("Rs. 0.00", size=20, weight=ft.FontWeight.BOLD, color=ACCENT_GREEN)

    # Display Boxes for Outputs
    pct_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("Dividend in %", size=13, color=TEXT_GREY_700, weight=ft.FontWeight.W_500),
                out_pct_val,
            ],
            spacing=4,
        ),
        padding=16,
        border=ft.Border.all(1.5, ACCENT_GREEN),
        border_radius=12,
        bgcolor=LIGHT_GREEN,
        expand=True,
    )

    gain_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("Total Gain Rs.", size=13, color=TEXT_GREY_700, weight=ft.FontWeight.W_500),
                out_gain_val,
            ],
            spacing=4,
        ),
        padding=16,
        border=ft.Border.all(1.5, ACCENT_GREEN),
        border_radius=12,
        bgcolor=LIGHT_GREEN,
        expand=True,
    )

    investment_box = ft.Row([ft.Container(
        content=ft.Column(
            [ft.Text("Your investment is ", size=13, color=TEXT_GREY_700, weight=ft.FontWeight.W_500), investment_text], spacing=4
        ),
        padding=16,
        border=ft.Border.all(1.5, ACCENT_GREEN),
        border_radius=12,
        bgcolor=LIGHT_GREEN,
        expand=True,
    )], expand=True)

    def calculate():
        nonlocal num_shares, buy_price, face_value, q1, q2, q3, q4, filer_status

        investment = num_shares * buy_price
        investment_text.value = f"Rs. {round(investment, 2):,.2f}"

        if filer_status is not None and investment > 0:
            total_div = q1 + q2 + q3 + q4
            amount = num_shares * buy_price

            if filer_status == "Filer":
                out = 0.85 * face_value * total_div * num_shares / amount
            elif filer_status == "Non filer":
                out = 0.70 * face_value * total_div * num_shares / amount

            out_pct_val.value = f"{round(out, 2):.2f}%"
            out_gain_val.value = f"{round(out * investment / 100, 2):,.2f}"
        else:
            out_pct_val.value = "0.00%"
            out_gain_val.value = "Rs. 0.00"

        page.update()

    # Change Handlers
    def on_shares_change(e):
        nonlocal num_shares
        try:
            num_shares = int(e.control.value) if e.control.value else 0
        except ValueError:
            num_shares = 0
        calculate()

    def on_price_change(e):
        nonlocal buy_price
        try:
            buy_price = float(e.control.value) if e.control.value else 0.0
        except ValueError:
            buy_price = 0.0
        calculate()

    def on_face_value_change(e):
        nonlocal face_value
        try:
            face_value = int(e.control.value) if e.control.value else 0
        except ValueError:
            face_value = 0
        calculate()

    def make_quarter_handler(quarter_attr):
        def handler(e):
            nonlocal q1, q2, q3, q4
            try:
                val = float(e.control.value) if e.control.value else 0.0
                val = min(max(val, 0.0), 100.0)
            except ValueError:
                val = 0.0

            if quarter_attr == "q1":
                q1 = val
            elif quarter_attr == "q2":
                q2 = val
            elif quarter_attr == "q3":
                q3 = val
            elif quarter_attr == "q4":
                q4 = val
            calculate()

        return handler

    def on_filer_change(e):
        nonlocal filer_status
        selected_val = e.control.selected
        if isinstance(selected_val, (set, list, tuple)):
            filer_status = list(selected_val)[0] if selected_val else None
        else:
            filer_status = selected_val
        calculate()

    # Input Fields Styling Helper
    def create_textfield(label, value, on_change, hint_text=None):
        return ft.TextField(
            label=label,
            value=value,
            hint_text=hint_text,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=on_change,
            border_color=BORDER_COLOR,
            focused_border_color=PRIMARY_BLUE,
            label_style=ft.TextStyle(color=PRIMARY_BLUE),
            bgcolor="white",
            border_radius=8,
            expand=True,
        )

    # Input Fields
    input_shares = create_textfield("No. of Shares", "0", on_shares_change)
    input_price = create_textfield("Buy Price", "0.00", on_price_change)
    input_face_value = create_textfield("Face Value", "0", on_face_value_change)

    input_q1 = create_textfield("Quarter 1 in %", "0.00", make_quarter_handler("q1"), "Enter a percentage...")
    input_q2 = create_textfield("Quarter 2 in %", "0.00", make_quarter_handler("q2"), "Enter a percentage...")
    input_q3 = create_textfield("Quarter 3 in %", "0.00", make_quarter_handler("q3"), "Enter a percentage...")
    input_q4 = create_textfield("Quarter 4 in %", "0.00", make_quarter_handler("q4"), "Enter a percentage...")

    filer_segmented = ft.SegmentedButton(
        selected=[],
        allow_empty_selection=True,
        segments=[
            ft.Segment(value="Filer", label=ft.Text("Filer")),
            ft.Segment(value="Non filer", label=ft.Text("Non filer")),
        ],
        on_change=on_filer_change,
        expand=True,
        # Define the outline color using ButtonStyle
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, BORDER_COLOR),  # 2px width, Primary Blue border
        ),
    )

    # Main Card Container
    card_content = ft.Container(
        padding=24,
        margin=20,
        bgcolor="white",
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=SHADOW_COLOR,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            [
                title_row,
                by_text,
                ft.Divider(height=15, color="transparent"),
                ft.Row([input_shares, input_price, input_face_value], spacing=10),
                ft.Divider(height=10, color="transparent"),
                investment_box,
                ft.Divider(height=10, color="transparent"),
                dividend_for_text,
                ft.Divider(height=5, color="transparent"),
                ft.Row([input_q1, input_q2], spacing=10),
                ft.Row([input_q3, input_q4], spacing=10),
                ft.Divider(height=15, color="transparent"),
                ft.Text("Are you a filer?", size=16, weight=ft.FontWeight.W_500, color=PRIMARY_BLUE),
                ft.Row([filer_segmented]),
                ft.Divider(height=15, color="transparent"),
                ft.Row([pct_box, gain_box], spacing=10),
            ]
        ,spacing=8),
    )

    # Main Page Layout with Blue-Green Gradient Background
    main_background = ft.Container(
        gradient=ft.LinearGradient(
            begin=ALIGN_TOP_LEFT,
            end=ALIGN_BOTTOM_RIGHT,
            colors=[
                "#E3F2FD",  # Soft Blue
                "#E0F2F1",  # Soft Teal
                "#E8F5E9",  # Soft Green
            ],
        ),
        alignment=ALIGN_TOP_CENTER,
        expand=True,
        content=card_content,
    )

    page.add(main_background)


if __name__ == "__main__":
    if hasattr(ft, "app"):
        ft.app(target=main)
    else:
        ft.run(main)