import flet as ft

PURCHASES = [(0, 0) for _ in range(10)]


def main(page: ft.Page):
    page.title = "My Purchases"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 12
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#F4F6FA"

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#2448A8",
            on_surface="#172033",
            on_surface_variant="#303B50",
            surface="#FFFFFF",
        ),
        text_theme=ft.TextTheme(
            body_large=ft.TextStyle(color="#172033"),
            body_medium=ft.TextStyle(color="#172033"),
            body_small=ft.TextStyle(color="#303B50"),
            title_large=ft.TextStyle(color="#172033"),
            title_medium=ft.TextStyle(color="#172033"),
            title_small=ft.TextStyle(color="#172033"),
            label_large=ft.TextStyle(color="#172033"),
            label_medium=ft.TextStyle(color="#303B50"),
            label_small=ft.TextStyle(color="#303B50"),
        ),
    )

    def parse_number(value):
        try:
            return float(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0.0

    def money(value):
        return f"{value:,.0f}"

    def number(value):
        return f"{value:,.0f}"

    # Calculator inputs

    dividend_input = ft.TextField(
        label="My Cash",
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50", size=12),
        text_size=16,
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
        content_padding=10,
        text_align=ft.TextAlign.RIGHT,
    )

    share_price_input = ft.TextField(
        label="Share price (Rs.)",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50", size=12),
        text_size=14,
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
        content_padding=10,
        text_align=ft.TextAlign.RIGHT,
        height=30
    )

    purchase_fields = []

    # Result cards

    def create_summary_card(label, value):
        value_text = ft.Text(
            value,
            size=17,
            weight=ft.FontWeight.BOLD,
            color="#172033",
            selectable=True,
            text_align=ft.TextAlign.RIGHT,
            expand=True
        )

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        label,
                        size=11,
                        weight=ft.FontWeight.W_500,
                        color="#303B50",
                    ),
                    value_text,
                ],
                spacing=6,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.END
            ),
            bgcolor="#FFFFFF",
            padding=5,
            border_radius=10,
            border=ft.Border.all(1, "#D5DCE8"),
            expand=True,
            height=60
        )

        return card, value_text

    shares_card, shares_value = create_summary_card(
        "Can Be Buy", "-"
    )

    cost_card, cost_value = create_summary_card(
        "Total Price", "Rs. 0"
    )

    remaining_card, remaining_value = create_summary_card(
        "Remaining Rs.", "Rs. 0"
    )

    remaining_shares_card, remaining_shares_value = (
        create_summary_card("Buy More", "0")
    )

    # Purchase list

    purchase_list = ft.Column(spacing=7)

    def recalculate(e=None):
        budget = parse_number(dividend_input.value)
        current_price = parse_number(share_price_input.value)

        total_cost = 0

        for item in purchase_fields:
            price = parse_number(item["price"].value)
            quantity = parse_number(item["quantity"].value)

            purchase_cost = price * quantity
            total_cost += purchase_cost
            item["cost"].value = money(purchase_cost)

        remaining_budget = budget - total_cost

        shares_value.value = (
            number(budget / current_price)
            if current_price > 0
            else ""
        )

        cost_value.value = total_cost
        remaining_value.value = money(remaining_budget)

        remaining_shares_value.value = (
            number(remaining_budget / current_price)
            if current_price > 0
            else ""
        )

        page.update()

    def create_purchase_row(index, price, quantity):
        price_input = ft.TextField(
            label="Price (Rs.)",
            value= "" if (price==0) else str(price),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            text_size=12,
            label_style=ft.TextStyle(color="#303B50", size=11),
            content_padding=7,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
            expand=True,
            height=26
        )

        quantity_input = ft.TextField(
            label="Quantity",
            value= "" if (quantity==0) else str(quantity),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            text_size=12,
            label_style=ft.TextStyle(color="#303B50", size=11),
            content_padding=10,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
            expand=True,
            height=26
        )

        cost_text = ft.Text(
            "0",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#172033",
            width=70,
            text_align=ft.TextAlign.END
        )

        purchase_fields.append(
            {
                "price": price_input,
                "quantity": quantity_input,
                "cost": cost_text,
            }
        )

        return ft.Container(
                ft.Row(
                    [ft.Text(f"{index}", size=16, weight=ft.FontWeight.BOLD, color="#172033"), quantity_input, price_input, cost_text],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),

            bgcolor="#FFFFFF",
            padding=10,
            border_radius=10,
            border=ft.Border.all(1, "#D5DCE8"),
        )

    def reset_values(e=None):
        dividend_input.value = ""
        share_price_input.value = ""

        for item in purchase_fields:
            item["price"].value = ""
            item["quantity"].value = ""

        recalculate()

    for index, (price, quantity) in enumerate(PURCHASES, start=1):
        purchase_list.controls.append(
            create_purchase_row(index, price, quantity)
        )

    dividend_input.on_change = recalculate
    share_price_input.on_change = recalculate

    # Main layout

    page.add(
        ft.Column(
            [
                ft.Container(height=15),
                ft.Text(
                    "My Purchases",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#172033",
                ),

                # Input fields
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            content=dividend_input,
                            col={"xs": 6, "md": 6},
                        ),
                        ft.Container(
                            content=remaining_card,
                            col={"xs": 6, "md": 6},
                        ),
                    ],
                    spacing=8,
                    run_spacing=8,
                ),


                # Purchase breakdown
                ft.Container(
                    content=ft.Column(
                        [

                            purchase_list,
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        "Reset Values",
                                        icon=ft.Icons.RESTART_ALT,
                                        on_click=reset_values,
                                    ),
                                    cost_card
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor="#F4F6FA",
                    padding=0,
                    border_radius=10,
                ),
            ],
            spacing=14,
            expand=True,
        )
    )

    recalculate()


if __name__ == "__main__":
    ft.run(main)