"""Small Tkinter/ttk GUI wired to the shared analysis service."""

from __future__ import annotations

import platform
import sys
import tkinter as tk
from collections.abc import Sequence
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ftproductlab.application import (
    AnalysisRequest,
    analyze_and_export,
    fitted_observed_total_fractions,
    parse_cut_specs,
)
from ftproductlab.core import AnalysisResult, InputBasis, Weighting


class MainWindow(ttk.Frame):
    """One-window CSV-to-report workflow."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=12)
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.basis = tk.StringVar(value=InputBasis.MOLAR.value)
        self.fit_minimum = tk.StringVar(value="3")
        self.fit_maximum = tk.StringVar(value="20")
        self.weighting = tk.StringVar(value=Weighting.UNIFORM.value)
        self.cut_specs = tk.StringVar(value="C1:1:1; C2-C4:2:4; C5+:5")
        self.status = tk.StringVar(value="Choose a CSV file and an explicit fit range.")
        self.last_result: AnalysisResult | None = None
        self._build()

    def _build(self) -> None:
        self.grid(sticky="nsew")
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="Input CSV").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.input_path).grid(
            row=0, column=1, sticky="ew", padx=6, pady=4
        )
        ttk.Button(self, text="Browse", command=self._choose_input).grid(row=0, column=2)
        ttk.Label(self, text="Output folder").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.output_path).grid(
            row=1, column=1, sticky="ew", padx=6, pady=4
        )
        ttk.Button(self, text="Browse", command=self._choose_output).grid(row=1, column=2)

        options = ttk.Frame(self)
        options.grid(row=2, column=0, columnspan=3, sticky="ew", pady=8)
        ttk.Label(options, text="Input basis").grid(row=0, column=0, padx=(0, 4))
        ttk.Combobox(
            options,
            textvariable=self.basis,
            values=[item.value for item in InputBasis],
            state="readonly",
            width=10,
        ).grid(row=0, column=1, padx=(0, 12))
        ttk.Label(options, text="Fit C").grid(row=0, column=2)
        ttk.Entry(options, textvariable=self.fit_minimum, width=5).grid(row=0, column=3)
        ttk.Label(options, text="to").grid(row=0, column=4, padx=3)
        ttk.Entry(options, textvariable=self.fit_maximum, width=5).grid(row=0, column=5)
        ttk.Label(options, text="Weighting").grid(row=0, column=6, padx=(12, 4))
        ttk.Combobox(
            options,
            textvariable=self.weighting,
            values=[item.value for item in Weighting],
            state="readonly",
            width=10,
        ).grid(row=0, column=7)
        ttk.Label(self, text="Product cuts").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.cut_specs).grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=6, pady=4
        )
        self.analyze_button = ttk.Button(self, text="Analyze and export", command=self.run_analysis)
        self.analyze_button.grid(row=4, column=0, columnspan=3, sticky="ew", pady=5)

        columns = ("carbon", "observed", "fitted", "deviation")
        self.results = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for column, label in zip(
            columns,
            (
                "C number",
                "Observed molar fraction",
                "Fitted (same denominator)",
                "Relative deviation",
            ),
            strict=True,
        ):
            self.results.heading(column, text=label)
            self.results.column(column, width=145, anchor="e")
        self.results.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=6)
        self.rowconfigure(5, weight=1)
        ttk.Label(self, textvariable=self.status, wraplength=720).grid(
            row=6, column=0, columnspan=3, sticky="w", pady=4
        )

    def _choose_input(self) -> None:
        selected = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if selected:
            self.input_path.set(selected)
            if not self.output_path.get():
                self.output_path.set(
                    str(Path(selected).with_suffix("").with_name("ftproductlab-output"))
                )

    def _choose_output(self) -> None:
        selected = filedialog.askdirectory()
        if selected:
            self.output_path.set(selected)

    def run_analysis(self, *, show_dialog: bool = True) -> AnalysisResult | None:
        """Execute the main workflow; keyword supports deterministic GUI tests."""

        try:
            request = AnalysisRequest(
                input_path=Path(self.input_path.get()),
                basis=InputBasis(self.basis.get()),
                fit_minimum=int(self.fit_minimum.get()),
                fit_maximum=int(self.fit_maximum.get()),
                weighting=Weighting(self.weighting.get()),
                cuts=parse_cut_specs(self.cut_specs.get().split(";")),
            )
            output = Path(self.output_path.get())
            if not self.input_path.get().strip() or not self.output_path.get().strip():
                raise ValueError("Input CSV and output folder are required")
            result = analyze_and_export(request, output)
            from ftproductlab.plotting import export_publication_figures

            export_publication_figures(result, output)
        except (OSError, RuntimeError, ValueError) as error:
            self.status.set(f"Analysis failed: {error}")
            if show_dialog:
                messagebox.showerror("FTProductLab", str(error))
            return None
        self.last_result = result
        for item in self.results.get_children():
            self.results.delete(item)
        fitted_fractions = fitted_observed_total_fractions(result)
        for point, fitted_fraction in zip(result.points, fitted_fractions, strict=True):
            self.results.insert(
                "",
                "end",
                values=(
                    point.carbon_number,
                    f"{point.observed_molar_fraction:.6g}",
                    f"{fitted_fraction:.6g}",
                    f"{point.relative_deviation:+.3%}",
                ),
            )
        self.status.set(
            f"alpha={result.fit.alpha:.5f}; fit C{result.fit_config.minimum_carbon}-"
            f"C{result.fit_config.maximum_carbon}; tables and figures exported to {output}"
        )
        return result


def create_root() -> tk.Tk:
    """Create the application's only Tk root."""

    root = tk.Tk()
    root.title("FTProductLab")
    root.geometry("820x560")
    root.minsize(700, 480)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    return root


def dependency_error_message(error: BaseException) -> str:
    """Return actionable platform information instead of a bare traceback."""

    return (
        "FTProductLab GUI could not start.\n"
        f"Reason: {error}\n"
        f"Python: {platform.python_version()} ({sys.executable})\n"
        f"Platform: {platform.platform()}\n"
        "Install the GUI/plot extras with:\n"
        'pip install "ftproductlab[gui]"\n'
        "Then run: python -m ftproductlab.gui"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Official GUI entry point with normal root lifecycle."""

    del argv
    try:
        root = create_root()
    except (ImportError, RuntimeError, tk.TclError) as error:
        print(dependency_error_message(error), file=sys.stderr)
        return 2
    MainWindow(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
