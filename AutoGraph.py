"""
AutoGraph, a small utility to create recipe graphs, this should be run when a recipe is updated
AutoGraph will create, or update the .png graphs for each recipe in the /Recipe List/ folder

fermentation data to be graphed within the Recipe List markdown files should be formed as below
    Date format should be YYYY-MM-DD and is required
    Temperature only in C as a float or integer or may be left blank
    Gravity must be a float  or may be left blank
    Standard Markdown table formatting should be used, see previous recipe lists for working examples
... "| Date       | Temperature  °C | Gravity |...More can be placed here..."
"""

import datetime
import re
from pathlib import Path
from typing import NamedTuple

import matplotlib.pyplot
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator

# Regex should be used with great care, this is not being used in that way
FementDataRegex = re.compile(r"\|(|[^\|]+)\|(|[^\|]+)\|(|[^\|]+)\|(?:.+)")


class FermentDataPoint(NamedTuple):
    date: datetime.date
    temp: float | None
    grav: float | None

    @property
    def temp(self) -> float | None:
        return self.temp

    @temp.setter
    def temp(self, value):
        self.temp = value

    @property
    def grav(self) -> float | None:
        return self.grav

    @grav.setter
    def grav(self, value):
        self.grav = value

    def __gt__(self, other):
        if isinstance(other, FermentDataPoint):
            self.date.__gt__(other.date)
        else:
            self.date.__gt__(other)

    def __lt__(self, other):
        if isinstance(other, FermentDataPoint):
            self.date.__lt__(other.date)
        else:
            self.date.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, FermentDataPoint):
            self.date.__eq__(other.date)
        else:
            self.date.__eq__(other)

    def __str__(self):
        temp_text = f'{self.temp:.2f}' if self.temp is not None else "N/A"
        grav_text = f'{self.grav:.3f}' if self.grav is not None else "N/A"
        return f"FermentationDataPoint(date = {self.date.isoformat()}, temp = {temp_text}, grav = {grav_text})"


def get_recipe_list() -> list[Path]:
    # get every recipe in the recipe list
    return [p for p in Path("Recipe List").iterdir() if p.is_file() and p.suffix == ".md"]


def get_recipe_fermentation_data(tar: Path) -> list[FermentDataPoint]:
    """ Extracts data from a .md file, this is not a smart method, I should be doing better here"""
    with open(tar, 'r') as f:
        md_text = f.read()
    ferm_list = []
    for (a, b, c) in FementDataRegex.findall(md_text):
        a: str = a.strip()
        b: str = b.strip()
        c: str = c.strip()
        temp = None
        grav = None
        try:
            date = datetime.date.fromisoformat(a.strip())
        except Exception as _:
            continue
        try:
            temp = float(b)
        except ValueError as _:
            pass
        try:
            grav = float(c)
        except ValueError as _:
            pass

        ferm_list.append(FermentDataPoint(date, temp, grav))

    return ferm_list


def make_graph(tar, data_: list[FermentDataPoint]):
    """ I should not be allowed to use PyPlot """

    plt.style.use('dark_background')
    # plot setup
    fig, ax1 = plt.subplots()
    fig: matplotlib.pyplot.Figure
    ax1: matplotlib.pyplot.Axes
    # data needs to be in a different layout, should have planne for this earlier
    data = ([], [], [])
    date_list = [d.date for d in data_ if d.grav is not None or d.temp is not None]

    date_min = min(date_list)
    date_max = max(date_list)

    data_temp_t: list[int]= []
    data_temp:list[float] = []

    data_grav_t: list[int]= []
    data_grav:list[float] = []

    for d in data_:
        # Dates are less useful
        if d.temp is not None:
            data_temp_t.append((d.date - date_min).days)
            data_temp.append(d.temp)
        if d.grav is not None:
            data_grav_t.append((d.date - date_min).days)
            data_grav.append(d.grav)

    colour_1 = "tab:purple"
    colour_2 = "tab:blue"

    # ax1.plot(data[0], data[1], color=colour_1)
    ax1.plot(data_temp_t, data_temp, color=colour_1)
    ax1.tick_params(axis='y', labelcolor=colour_1)
    ax1.set_ylabel("Temperature °C", color=colour_1)
    ax1.set(
        xlabel="Days since start",
        ylim=[max(15, int(min(data_temp))-2), max(30, int(min(data_temp))+1)],
    )

    ax2 = ax1.twinx()
    # ax2.plot(data[0], data[2], color=colour_2)
    ax2.plot(data_grav_t, data_grav, color=colour_2)
    ax2.tick_params(axis='y', labelcolor=colour_2)
    ax2.set_ylabel("Gravity", color=colour_2)
    ax2.set(
        ylim=[
            0.95,  # I don't think we'll be going below 0.950, might have to modify later
            (max(data_grav) + 0.02) or 1.5  # crop the top of gravity if not used
        ], )

    # formatters
    ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

    ax1.set_title(
        f"#{tar.name.rsplit('.', 1)[0].replace('_',' ')} was started on {date_min.isoformat()}, last update {date_max.isoformat()}"
    )
    ax1.set_xlim(left=0)
    ax1.xaxis.set_ticks(range(0,(date_max-date_min).days,7))
    ax1.xaxis.set_minor_locator(MultipleLocator(1))

    fig.tight_layout()
    fig.savefig(tar)


def apply_over_recipes():

    for target in get_recipe_list():
        data = get_recipe_fermentation_data(target)
        if len(data) < 2:
            print("err")
            continue
        out_tar = target.with_suffix(".png")
        make_graph(out_tar, data)


if __name__ == '__main__':
    apply_over_recipes()
