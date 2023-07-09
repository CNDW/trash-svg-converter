from os import path
import os
from rich import pretty
from rich import print
from rich.segment import Segment
from rich.color import Color as RichColor
from rich.style import Style
from rich.measure import Measurement
from dataclasses import dataclass
from functools import cached_property
from lxml import etree
import webbrowser
from colour import Color, HSL_equivalence

pretty.install()

"""
red -> primary
blue -> secondary
lime green -> liner
purple -> webbing
yellow -> stitching
dark green -> trim
turquoise -> buckle
orange -> velcro
"""


@dataclass
class DataColor:
    hex_code: str
    selector: str = "none"
    tolorance: float = 0.15

    @cached_property
    def color(self):
        return Color(self.hex_code)

    def __eq__(self, other: "DataColor"):
        blue_diff = abs(self.color.get_blue() - other.color.get_blue())
        if blue_diff > self.tolorance:
            return False

        red_diff = abs(self.color.get_red() - other.color.get_red())
        if red_diff > self.tolorance:
            return False

        green_diff = abs(self.color.get_green() - other.color.get_green())
        if green_diff > self.tolorance:
            return False

        return True

    def __rich_console__(self, console, options):
        color = RichColor.from_rgb(
            self.color.get_red() * 255,
            self.color.get_green() * 255,
            self.color.get_blue() * 255,
        )
        yield Segment("▄▄", Style(color=color, bgcolor=color))

    def __rich_measure__(self, console, options):
        return Measurement(1, options.max_width)


PRIMARY = DataColor("#ff0200", selector="primary")  # red
SECONDARY = DataColor("#0a24f7", selector="secondary")  # blue
LINER = DataColor("#00c600", selector="liner")  # lime green
WEBBING = DataColor("#ff00ff", selector="webbing")  # purple
STITCHING = DataColor("#fff200", selector="stitching")  # yellow
TRIM = DataColor("#009e78", selector="trim")  # dark green
BUCKLE = DataColor("#00ffff", selector="buckle")  # turquoise
VELCRO = DataColor("#ffa600", selector="velcro")  # orange

IGNORED_COLORS = {"#ffffff", "#a3a3a3"}

COLORS = {
    "PRIMARY": PRIMARY,
    "SECONDARY": SECONDARY,
    "LINER": LINER,
    "WEBBING": WEBBING,
    "STITCHING": STITCHING,
    "TRIM": TRIM,
    "BUCKLE": BUCKLE,
    "VELCRO": VELCRO,
}
LINE_CLASS = "line-style"
FILL_CLASS = "fill-style"


@dataclass
class DynamicElement:
    element: etree.Element
    namespace: str

    @cached_property
    def styles(self):
        styles_str = self.element.attrib.get("style")
        if not styles_str:
            return {}

        style_list = styles_str.split(";")

        return dict(style.split(":") for style in style_list)

    @property
    def tag(self):
        return self.element.tag.replace(self.namespace, "")

    @property
    def classname(self):
        base_class = FILL_CLASS
        if self.type == "STITCHING":
            base_class = LINE_CLASS
        return f"{base_class} {self.type_color.selector}"

    @property
    def fill(self):
        return self.styles.get("fill") or "none"

    @property
    def stroke(self):
        return self.styles.get("stroke") or "#000000"

    @property
    def color_hex(self):
        if self.fill == "none":
            return self.stroke
        return self.fill

    @property
    def type_color(self):
        return COLORS[self.type]

    @cached_property
    def data_color(self):
        return DataColor(self.color_hex)

    @cached_property
    def type(self):
        color = self.data_color
        for type, type_color in COLORS.items():
            if color == type_color:
                return type

        raise Exception(f"Couldn't match color {color}")


@dataclass
class SVGFile:
    name: str
    in_path: str
    out_path: str

    @cached_property
    def tree(self) -> etree.Element:
        with open(self.in_path, "rb") as file:
            data = file.read()

        return etree.fromstring(data)

    @cached_property
    def namespace(self):
        namespace = self.tree.nsmap.get("svg")
        if not namespace:
            return ""
        return f"{{{namespace}}}"

    def normalize_size(self, width=792):
        original_width = self.tree.attrib.get("width")
        if not original_width or original_width.endswith("%"):
            original_width = self.tree.attrib["viewbox"].split(" ")[2]

        original_height = self.tree.attrib.get("height")
        if not original_height or original_height.endswith("%"):
            original_height = self.tree.attrib["viewbox"].split(" ")[3]

        ratio = width / float(original_width)
        self.tree.attrib["width"] = "100%"
        self.tree.attrib["height"] = "100%"
        self.tree.attrib["viewbox"] = f"0 0 {width} {float(original_height) * ratio}"
        self.tree.attrib["x"] = "0px"
        self.tree.attrib["y"] = "0px"

    def iter_dynamic_elements(self):
        for _element in self.tree.iter():
            element = DynamicElement(element=_element, namespace=self.namespace)
            if element.tag != "path" or not element.styles:
                continue

            if element.fill == "none" and element.stroke == "#000000":
                continue

            if element.fill == "#000000" and element.stroke == "none":
                continue

            if element.color_hex in IGNORED_COLORS:
                continue

            yield element

    def add_style_element(self):
        tree: etree.Element = self.tree
        """

        """
        style_element = etree.Element(f"{self.namespace}style")
        parent_class = f"{self.name.replace('_', '-')}-svg"
        self.tree.attrib["class"] = parent_class
        style_element.text = "\n".join(
            [
                f".{parent_class} .{LINE_CLASS}{{fill:none;stroke:#000000;stroke-miterlimit:10;stroke-dasharray:10, 5;}}",
                f".{parent_class} .{FILL_CLASS}{{fill:#FFFFFF;stroke:#000000;stroke-miterlimit:10;}}",
            ]
        )
        tree.insert(0, style_element)

    def normalize_colors(self):
        for element in self.iter_dynamic_elements():
            # print(element.data_color, end=" ")
            # print(" -", end=" ")
            # print(COLORS[element.type], end=" ")
            # print(f" {element.type} ")
            element.element.attrib.pop("style", None)
            element.element.attrib["class"] = element.classname
        self.add_style_element()

    def save(self, open_saved=False):
        with open(self.out_path, "wb") as file:
            out = etree.tostring(
                self.tree,
                xml_declaration=True,
                standalone=True,
                pretty_print=True,
            )
            file.write(out)
        if open_saved:
            self.open(self.out_path)

    def open(self, file_path=None):
        if not file_path:
            file_path = self.in_path
        browser = webbrowser.get()
        browser.open_new_tab(file_path)


file_path = path.realpath(path.join("svgs", "TRASH_duffel1(clown).svg"))
out_path = path.realpath(path.join("svgs", "TRASH_duffel1(clown)-resized.svg"))


def convert(filename):
    svg_file = SVGFile(
        name=filename.replace(".svg", ""),
        in_path=path.realpath(path.join("svgs", filename)),
        out_path=path.realpath(path.join("clean", filename)),
    )

    svg_file.open()
    svg_file.normalize_size()
    svg_file.normalize_colors()
    svg_file.save(open_saved=True)


for filename in os.listdir("svgs"):
    convert(filename)
