"""In this module we define CssGenerators"""
import param

import panel as pn

from .color_scheme import COLOR_SCHEME_EDITABLE_COLORS, ColorScheme


class CssGenerator(param.Parameterized):
    color_scheme = param.ClassSelector(class_=ColorScheme, readonly=True)
    panel_css = param.String()
    dataframe_css = param.String()

    def __init__(self, **params):
        self.param.color_scheme.default = ColorScheme()

        super().__init__(**params)

        self._set_panel_css()
        self._set_dataframe_css()

    def _get_panel_css(self):
        return ""

    def _get_dataframe_css(self):
        return ""

    @param.depends("color_scheme", *COLOR_SCHEME_EDITABLE_COLORS, watch=True)
    def _set_panel_css(self):
        self.panel_css = self._get_panel_css()

    @param.depends("color_scheme", *COLOR_SCHEME_EDITABLE_COLORS, watch=True)
    def _set_dataframe_css(self):
        self.dataframe_css = self._get_dataframe_css()

    @param.depends("color_scheme")
    def _color_scheme_view(self):
        return self.color_scheme.view()

    def _css_view(self):
        return pn.Column(
            "## CSS",
            pn.Tabs(
                pn.Param(
                    self.param.panel_css,
                    name="Panel",
                    widgets={"panel_css": {"type": pn.widgets.TextAreaInput, "height": 600}},
                ),
                pn.Param(
                    self.param.dataframe_css,
                    name="Dataframe",
                    widgets={"dataframe_css": {"type": pn.widgets.TextAreaInput, "height": 600}},
                ),
            ),
        )

    @param.depends("color_scheme")
    def view(self):
        return pn.Column(self._color_scheme_view, pn.layout.HSpacer(width=10), self._css_view,)

# Inspiration:
# https://github.com/angular/components/blob/master/src/material/button/_button-theme.scss
# https://material-ui.com/components/buttons/
# https://material.io/resources/color/#!/?view.left=0&view.right=0&primary.color=9C27B0&secondary.color=F44336

class DarkCssGenerator(CssGenerator):
    def _get_panel_css(self):
        panel_css = f"""\
body {{
    background-color: {self.color_scheme.dark};
    color: {self.color_scheme.white};
}}

h1, h2, h3, h4, h5 {{
color: {self.color_scheme.white} !important;
}}

.bk-root .bk-tabs-header .bk-tab.bk-active {{
    background:  {self.color_scheme.primary};
    color:  {self.color_scheme.white};
    border-color:  {self.color_scheme.primary};
}}
"""
        panel_css += self._get_panel_button_outlined_css(button_type="default", color=self.color_scheme.text_primary, border_color=self.color_scheme.disabled_text)
        panel_css += self._get_panel_button_contained_css(button_type="primary", background_color=self.color_scheme.primary, color=self.color_scheme.white)
        panel_css += self._get_panel_button_contained_css(button_type="success", background_color=self.color_scheme.secondary, color=self.color_scheme.black)
        panel_css += self._get_panel_button_contained_css(button_type="warning", background_color=self.color_scheme.warning, color=self.color_scheme.white)
        panel_css += self._get_panel_button_contained_css(button_type="danger", background_color=self.color_scheme.warning, color=self.color_scheme.white)

        panel_css += self._get_panel_input_css()
        panel_css += self._get_slick_grid_css()

        return panel_css

    def _get_panel_button_outlined_css(self, button_type="default", color="gray", border_color="gray"):
        return f"""\
.bk-root .bk-btn-{button_type} {{
    color: {color};
    background-color: transparent;
    border: 0px;
    border-radius: 4px;
    border-width: 1px;
    border-style: solid;
    border-color: {border_color};
  }}
.bk-root .bk-btn-{button_type}:hover {{
  color: {color};
  background-color: transparent;
  border-color: {border_color};
}}
.bk-root .bk-btn-{button_type}.bk-active {{
  color: {color};
  background-color: transparent;
  border-color: {border_color};
}}
.bk-root .bk-btn-{button_type}[disabled],
.bk-root .bk-btn-{button_type}[disabled]:hover,
.bk-root .bk-btn-{button_type}[disabled]:focus,
.bk-root .bk-btn-{button_type}[disabled]:active,
.bk-root .bk-btn-{button_type}[disabled].bk-active {{
  background-color: transparent;
  border-color: {border_color};
}}"""

    def _get_panel_input_css(self):
        return f"""\
.bk-root .bk-input {{
    background: {self.color_scheme.gray_700};
    color: {self.color_scheme.white};
    border: 1px solid rgb(216,209,202);
    border-radius: 4px;
}}

.bk-root .bk-input:focus {{
    background: {self.color_scheme.gray_700};
    color: {self.color_scheme.white};
    border-color: {self.color_scheme.secondary};
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(102, 175, 233, 0.6);
}}

.bk-root .bk-input::placeholder,
.bk-root .bk-input:-ms-input-placeholder,
.bk-root .bk-input::-moz-placeholder,
.bk-root .bk-input::-webkit-input-placeholder {{
    color: #999;
    opacity: 1;
}}

.bk-root .bk-input[disabled],
.bk-root .bk-input[readonly] {{
    cursor: not-allowed;
    background-color: #eee;
    opacity: 1;
}}

.bk-root select[multiple].bk-input,
.bk-root select[size].bk-input,
.bk-root textarea.bk-input {{
    height: auto;
}}

.bk-root .bk-input-group {{
    width: 100%;
    height: 100%;
    display: inline-flex;
    display: -webkit-inline-flex;
    flex-wrap: nowrap;
    -webkit-flex-wrap: nowrap;
    align-items: start;
    -webkit-align-items: start;
    flex-direction: column;
    -webkit-flex-direction: column;
    white-space: nowrap;
}}
        """

    def _get_panel_button_contained_css(self, button_type="default", background_color="black", color="white"):
        return f"""\
.bk-root .bk-btn-{button_type} {{
    color: {color};
    background-color: {background_color};
    border: 0px;
    border-radius: 4px;
  }}
.bk-root .bk-btn-{button_type}:hover {{
  /* color: #1a2028; */
  background-color: {background_color};
  /* border-color: #1a2028; */
}}
.bk-root .bk-btn-{button_type}.bk-active {{
  background-color: {background_color};
  border-color: #adadad;
}}
.bk-root .bk-btn-{button_type}[disabled],
.bk-root .bk-btn-{button_type}[disabled]:hover,
.bk-root .bk-btn-{button_type}[disabled]:focus,
.bk-root .bk-btn-{button_type}[disabled]:active,
.bk-root .bk-btn-{button_type}[disabled].bk-active {{
  background-color: transparent;
  border-color: #ccc;
}}"""

# border-bottom: 1px solid {self.color_scheme.primary};
    def _get_dataframe_css(self, background="#424242", border_color="rgba(255,255,255, 0.5)", color="#ffffff"):
        return f"""\
table.panel-df {{
    color: {color};
    border-radius: 4px;
}}
.panel-df tbody tr:nth-child(odd) {{
    background: {background};
}}
.panel-df tbody tr {{
    background: {background};
    border-top-style: solid;
    border-top-width: 1px;
    border-top-color: {border_color};
   }}
.panel-df thead {{
    background: {background};
    color: {color};
    font-weight: 500px;
}}
.panel-df tr:hover:nth-child(odd) {{
    background: {background} !important;
}}
.panel-df tr:hover {{
    background: {background} !important;
}}
.panel-df thead tr:hover:nth-child(1) {{
    background-color: inherit !important;
}}

.panel-df thead:hover {{
    background: {background} !important;
}}"""


    def _get_slick_grid_css(self):
        return f"""\
.bk-root .slick-header-column.ui-state-default {{
    border-right: 1px solid silver;
}}

.bk-root .slick-sort-indicator-numbered {{
    color: #6190CD;
}}

.bk-root .slick-sortable-placeholder {{
    background: silver;
}}

.bk-root .slick-cell,
.bk-root .slick-headerrow-column,
.bk-root .slick-footerrow-column {{
    border: 1px solid transparent;
    border-right: 1px dotted silver;
    border-bottom-color: silver;
}}

.bk-root .slick-cell,
.bk-root .slick-headerrow-column {{
    border-bottom-color: silver;
}}

.bk-root .slick-footerrow-column {{
    border-top-color: silver;
}}

.bk-root .slick-cell.highlighted {{
    background: lightskyblue;
    background: rgba(0, 0, 255, 0.2);
}}

.bk-root .slick-cell.flashing {{
    border: 1px solid red !important;
}}

.bk-root .slick-cell.editable {{
    background: white;
    border-color: black;
    border-style: solid;
}}

.bk-root .slick-reorder-proxy {{
    background: blue;
    opacity: 0.15;
}}

.bk-root .slick-reorder-guide {{
    background: blue;
    opacity: 0.7;
}}

.bk-root .slick-selection {{
    border: 2px dashed black;
}}

.bk-root .slick-header-columns {{
    border-bottom: 1px solid silver;
}}

.bk-root .slick-header-column {{
    border-right: 1px solid silver;
    background: {self.color_scheme.gray_800};
    font-weight: 500px;
}}

.bk-root .slick-header-column:hover,
.bk-root .slick-header-column-active {{
    background: {self.color_scheme.gray_800} url('images/header-columns-over-bg.gif') repeat-x center bottom;
}}

.bk-root .slick-headerrow {{
    background: #fafafa;
}}

.bk-root .slick-headerrow-column {{
    background: #fafafa;
}}

.bk-root .slick-row.ui-state-active {{
    background: #F5F7D7;
}}

.bk-root .slick-row {{
    background: {self.color_scheme.gray_800};
}}

.bk-root .slick-row.selected {{
    background: #DFE8F6;
}}

.bk-root .slick-group {{
    border-bottom: 2px solid silver;
}}

.bk-root .slick-group-totals {{
    color: gray;
    background: white;
}}

.bk-root .slick-cell.selected {{
    background-color: {self.color_scheme.secondary};
    color: {self.color_scheme.black};
}}

.bk-root .slick-cell.active {{
    border-color: gray;
    border-style: solid;
}}

.bk-root .slick-sortable-placeholder {{
    background: silver !important;
}}

.bk-root .slick-row.odd {{
    background: {self.color_scheme.gray_800};
}}

.bk-root .slick-row.ui-state-active {{
    background: #F5F7D7;
}}

.bk-root .slick-row.loading {{
    opacity: 0.5;
}}

.bk-root .slick-cell.invalid {{
    border-color: red;
}}

@-moz-keyframes slickgrid-invalid-hilite {{
    from {{
        box-shadow: 0 0 6px red;
    }}
    to {{
        box-shadow: none;
    }}
}}

@-webkit-keyframes slickgrid-invalid-hilite {{
    from {{
        box-shadow: 0 0 6px red;
    }}
    to {{
        box-shadow: none;
    }}
}}

.bk-root .slick-header-button {{
.bk-root .slick-header-menuitem-disabled {{
    color: silver;
}}

.bk-root .slick-columnpicker {{
    background: #f0f0f0;
}}

.bk-root .slick-columnpicker li {{
    background: none;
}}

.bk-root .slick-columnpicker li a:hover {{
    background: white;
}}

.bk-root .slick-pager .ui-icon-container {{
    border-color: gray;
}}

.bk-root .bk-cell-special-defaults {{
    border-right-color: silver;
    border-right-style: solid;
    background: #f5f5f5;
}}

.bk-root .bk-cell-select {{
    border-right-color: silver;
    border-right-style: solid;
    background: #f5f5f5;
}}

.bk-root .bk-cell-index {{
    border-right-color: silver;
    border-right-style: solid;
    background: #f5f5f5;
    color: gray;
}}

"""

DEFAULT_CSS_GENERATOR = CssGenerator(name="Default")
DARK_CSS_GENERATOR = DarkCssGenerator(name="Dark")

CSS_GENERATORS = [DEFAULT_CSS_GENERATOR, DARK_CSS_GENERATOR]