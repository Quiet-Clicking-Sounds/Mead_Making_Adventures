import datetime
import re
from pathlib import Path
from typing import NamedTuple

import matplotlib.pyplot
import matplotlib.pyplot as plt

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
        self.date.__gt__(other.date)

    def __lt__(self, other):
        self.date.__lt__(other.date)

    def __eq__(self, other):
        self.date.__eq__(other.date)

    def __str__(self):
        temp_text = f'{self.temp:.2f}' if self.temp is not None else "N/A"
        grav_text = f'{self.grav:.3f}' if self.grav is not None else "N/A"
        return f"FermentationDataPoint(date = {self.date.isoformat()}, temp = {temp_text}, grav = {grav_text})"


def get_recipe_list() -> list[Path]:
    # get every recipe in the recipe list
    return [p for p in Path("Recipe List").iterdir() if p.is_file() and p.suffix == ".md"]


def get_recipe_fermentation_data(tar: Path) -> list[FermentDataPoint]:
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
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots()
    fig: matplotlib.pyplot.Figure
    ax1: matplotlib.pyplot.Axes
    data = ([], [], [])
    for d in data_:
        data[0].append(d.date)
        data[1].append(d.temp)
        data[2].append(d.grav)
    c1 = "tab:purple"
    ax1.plot(data[0], data[1], color=c1)
    ax1.tick_params(axis='y', labelcolor=c1)
    ax1.set_ylabel("Temperature °C", color=c1)
    ax1.set(
        xlabel="Date",
        ylim=[10, 30],
    )

    ax1.tick_params(axis='x', rotation=45)

    c2 = "tab:blue"
    ax2 = ax1.twinx()
    ax2.plot(data[0], data[2], color=c2)
    ax2.tick_params(axis='y', labelcolor=c2)
    ax2.set_ylabel("Gravity", color=c2)
    ax2.set(ylim=[0.9, 1.25], )
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
