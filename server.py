import os
import pandas as pd
from typing import Optional

## Add util functions here for reading ranges etc

PATH = os.path.join(os.getcwd(), "drugs.csv")


class Drug:
    def __init__(
        self,
        name: str,
        dose: float,
        df: pd.DataFrame,
        weight: Optional[int] = None,
        rate=None,
    ):
        self.name = name
        self.dose = dose
        self.weight = weight
        self.rate = rate
        self.conc: Optional[float] = None

        try:
            row = df[df["Drug"].str.lower() == name.lower()].iloc[0]
            print(row)
            self.units = row["Units"]
            self.solute = row["Solute"]
            self.solvent = row["Solvent"]
            self.conc_unit = row["Conc_units"]
            self.other_names = row["Other names"]
            self.max_rate = row["Max_rate"]

        except IndexError:
            print("Missing the values asked, please check CSV")
            exit()

    def __str__(self):
        return (
            f"Drug(name={self.name}, dose={self.dose}, units={self.units}, "
            f"conc_unit={self.conc_unit}, solute={self.solute}, solvent={self.solvent}, "
            f"weight={self.weight}, rate={self.rate} {self.units})"
        )

    @classmethod
    def load_data(cls, path: str) -> pd.DataFrame:
        if os.path.isfile(path):
            df = pd.read_csv(path)
            return df
        else:
            raise ValueError("Given invalid file path")

    def concentration(self) -> float:
        if self.solvent > 0:
            return self.solute / self.solvent
        else:
            raise ValueError("Tried to get conc by dividing by 0")

    def get_rate(self, dose):
        solute = self.solute
        self.dose = dose
        dose = self.dose

        if self.units.startswith("mcg") and self.conc_unit.startswith("mg"):
            print("Converting concentration from mg to mcg")
            solute *= 1000  # convert conc to mcg/mL

        if self.units.startswith("mg") and self.conc_unit.startswith("mcg"):
            print("Converting dose from mg to mcg")
            dose *= 1000  # convert dose to mcg

        conc = solute / self.solvent
        self.conc = conc
        self.rate = (dose * self.weight) / conc
        print(f"dose/min : {dose * self.weight}")
        print(f"Concentration: {conc}")
        print(f"Rate (cc/min): {self.rate}")
        print(f"Rate (cc/hr): {self.rate * 60}")


def main():
    df = Drug.load_data(PATH)
    print(df)
    # drug = Drug("propofol", 25, df, 43, 50)
    drug = Drug("levophed", 0, df, 43)
    print()
    print(drug)
    print()
    drug.get_rate(1.25)


if __name__ == "__main__":
    main()
