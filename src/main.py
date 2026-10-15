import flet as ft

PURCHASES = [(0, 0) for _ in range(10)]


def main(page: ft.Page):
    page.title = "Dividend Share Calculator"
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
        return f"Rs. {value:,.2f}"

    def number(value):
        return f"{value:,.2f}"

    # Calculator inputs

    dividend_input = ft.TextField(
        label="Dividend (Rs.)",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50", size=12),
        text_size=14,
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
        content_padding=10,
    )

    share_price_input = ft.TextField(
        label="Share price (Rs.)",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50", size=12),
        text_size=14,
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
        content_padding=10,
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
            ),
            bgcolor="#FFFFFF",
            padding=10,
            border_radius=10,
            border=ft.Border.all(1, "#D5DCE8"),
            expand=True,
        )

        return card, value_text

    shares_card, shares_value = create_summary_card(
        "SHARES AFFORDABLE", "0"
    )

    cost_card, cost_value = create_summary_card(
        "TOTAL COST", "Rs. 0.00"
    )

    remaining_card, remaining_value = create_summary_card(
        "REMAINING BUDGET", "Rs. 0.00"
    )

    remaining_shares_card, remaining_shares_value = (
        create_summary_card("REMAINING SHARES", "0")
    )

    # Purchase list

    purchase_list = ft.Column(spacing=10)

    def recalculate(e=None):
        budget = parse_number(dividend_input.value)
        current_price = parse_number(share_price_input.value)

        total_cost = 0.0

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
            else "0.00"
        )

        cost_value.value = money(total_cost)
        remaining_value.value = money(remaining_budget)

        remaining_shares_value.value = (
            number(remaining_budget / current_price)
            if current_price > 0
            else "0.00"
        )

        page.update()

    def create_purchase_row(index, price, quantity):
        price_input = ft.TextField(
            label="Price (Rs.)",
            value=str(price),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            text_size=14,
            label_style=ft.TextStyle(color="#303B50", size=11),
            content_padding=10,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
            expand=True,
        )

        quantity_input = ft.TextField(
            label="Quantity",
            value=str(quantity),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            text_size=14,
            label_style=ft.TextStyle(color="#303B50", size=11),
            content_padding=10,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
            expand=True,
        )

        cost_text = ft.Text(
            "Rs. 0.00",
            size=15,
            weight=ft.FontWeight.BOLD,
            color="#172033",
        )

        purchase_fields.append(
            {
                "price": price_input,
                "quantity": quantity_input,
                "cost": cost_text,
            }
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                f"Purchase {index}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color="#172033",
                            ),
                            ft.Container(expand=True),
                            ft.Text("Cost:", size=12, color="#303B50"),
                            cost_text,
                        ],
                        spacing=8,
                    ),
                    ft.Row(
                        [price_input, quantity_input],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=8,
            ),
            bgcolor="#FFFFFF",
            padding=12,
            border_radius=10,
            border=ft.Border.all(1, "#D5DCE8"),
        )

    def reset_values(e=None):
        dividend_input.value = "0"
        share_price_input.value = "0"

        for item in purchase_fields:
            item["price"].value = "0"
            item["quantity"].value = "0"

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
                ft.Text(
                    "Dividend Share Calculator",
                    size=25,
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
                            content=share_price_input,
                            col={"xs": 6, "md": 6},
                        ),
                    ],
                    spacing=8,
                    run_spacing=8,
                ),

                # Top results row
                # Shares Affordable | Remaining Budget | Remaining Shares
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            content=shares_card,
                            col={"xs": 4, "md": 4},
                        ),
                        ft.Container(
                            content=remaining_card,
                            col={"xs": 4, "md": 4},
                        ),
                        ft.Container(
                            content=remaining_shares_card,
                            col={"xs": 4, "md": 4},
                        ),
                    ],
                    spacing=6,
                    run_spacing=6,
                ),

                # Purchase breakdown
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Purchase Breakdown",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#172033",
                            ),
                            purchase_list,
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        "Reset Values",
                                        icon=ft.Icons.RESTART_ALT,
                                        on_click=reset_values,
                                    ),
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

                # Total cost at the bottom
                cost_card,
            ],
            spacing=14,
            expand=True,
        )
    )

    recalculate()


if __name__ == "__main__":
    ft.run(main)