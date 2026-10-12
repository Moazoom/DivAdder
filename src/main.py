
import flet as ft

PURCHASES = [(0, 0) for _ in range(10)]


def main(page: ft.Page):
    page.title = "Dividend Share Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
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

    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#F4F6FA"

    def parse_number(value):
        try:
            return float(str(value).replace(",", "").strip())
        except (ValueError, TypeError):
            return 0.0

    def money(value):
        return f"${value:,.2f}"

    def number(value):
        return f"{value:,.2f}"

    dividend_input = ft.TextField(
        label="Dividend amount ($)",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50"),
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
    )

    share_price_input = ft.TextField(
        label="Current share price ($)",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        color="#172033",
        label_style=ft.TextStyle(color="#303B50"),
        border_color="#9AA7BC",
        focused_border_color="#2448A8",
    )

    purchase_fields = []

    def create_summary_card(label, value):
        value_text = ft.Text(
            value,
            size=22,
            weight=ft.FontWeight.BOLD,
            color="#172033",
        )

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        label,
                        size=12,
                        color="#303B50",
                        weight=ft.FontWeight.W_500,
                    ),
                    value_text,
                ],
                spacing=8,
            ),
            bgcolor="#FFFFFF",
            padding=18,
            border_radius=12,
            border=ft.Border.all(1, "#D5DCE8"),
            expand=True,
        )

        return card, value_text

    shares_card, shares_value = create_summary_card(
        "SHARES AFFORDABLE", "0.00"
    )

    cost_card, cost_value = create_summary_card(
        "TOTAL PURCHASE COST", "$0.00"
    )

    remaining_card, remaining_value = create_summary_card(
        "REMAINING BUDGET", "$0.00"
    )

    remaining_shares_card, remaining_shares_value = create_summary_card(
        "REMAINING SHARES", "0.00"
    )

    purchase_list = ft.Column(spacing=0)

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
            value=str(price),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            dense=True,
            width=115,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
        )

        quantity_input = ft.TextField(
            value=str(quantity),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            dense=True,
            width=115,
            color="#172033",
            border_color="#9AA7BC",
            focused_border_color="#2448A8",
            on_change=recalculate,
        )

        cost_text = ft.Text(
            "$0.00",
            size=14,
            weight=ft.FontWeight.W_500,
            color="#172033",
            text_align=ft.TextAlign.RIGHT,
        )

        purchase_fields.append({
            "price": price_input,
            "quantity": quantity_input,
            "cost": cost_text,
        })

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        f"Purchase {index}",
                        width=105,
                        weight=ft.FontWeight.W_500,
                        color="#172033",
                    ),
                    price_input,
                    quantity_input,
                    ft.Container(
                        content=cost_text,
                        width=105,
                        alignment=ft.Alignment.CENTER_RIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.Padding.symmetric(vertical=8),
            border=ft.Border(
                bottom=ft.BorderSide(1, "#D5DCE8")
            ),
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

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Dividend Share Calculator",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#172033",
                ),

                ft.Text(
                    "Calculate your share purchases and remaining budget.",
                    color="#303B50",
                    size=14,
                ),

                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Calculator Inputs",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#172033",
                            ),
                            ft.Row(
                                [dividend_input, share_price_input],
                                spacing=16,
                            ),
                        ],
                        spacing=16,
                    ),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=12,
                    border=ft.Border.all(1, "#D5DCE8"),
                ),

                ft.ResponsiveRow(
                    [
                        ft.Container(
                            content=shares_card,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=cost_card,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=remaining_card,
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=remaining_shares_card,
                            col={"xs": 12, "md": 6},
                        ),
                    ],
                    spacing=12,
                    run_spacing=12,
                ),

                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Purchase Breakdown",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#172033",
                            ),

                            ft.Text(
                                "Edit the price and quantity of each "
                                "purchase. Costs update automatically.",
                                color="#303B50",
                                size=13,
                            ),

                            ft.Row(
                                [
                                    ft.Text(
                                        "Purchase",
                                        width=105,
                                        weight=ft.FontWeight.BOLD,
                                        color="#172033",
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Price ($)",
                                            weight=ft.FontWeight.BOLD,
                                            color="#172033",
                                        ),
                                        width=115,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Quantity",
                                            weight=ft.FontWeight.BOLD,
                                            color="#172033",
                                        ),
                                        width=115,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Cost ($)",
                                            weight=ft.FontWeight.BOLD,
                                            color="#172033",
                                        ),
                                        width=105,
                                        alignment=ft.Alignment.CENTER_RIGHT,
                                    ),
                                ],
                                spacing=8,
                            ),

                            ft.Divider(color="#D5DCE8", height=1),

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
                        spacing=14,
                    ),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=12,
                    border=ft.Border.all(1, "#D5DCE8"),
                ),

                ft.Text(
                    "All calculations use the values entered above.",
                    size=12,
                    color="#303B50",
                ),
            ],
            spacing=18,
        )
    )

    recalculate()


if __name__ == "__main__":
    ft.run(main)