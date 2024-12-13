"""Convenience functions for showing user facing options and their descriptions."""

import functools
from typing import Literal

from cogent3 import _Table, make_table

from piqtree.model._freq_type import FreqType
from piqtree.model._rate_type import ALL_BASE_RATE_TYPES, get_description
from piqtree.model._substitution_model import (
    ALL_MODELS_CLASSES,
    AaModel,
    DnaModel,
    SubstitutionModel,
)


@functools.cache
def _make_models(model_type: type[SubstitutionModel]) -> dict[str, list[str]]:
    data: dict[str, list[str]] = {
        "Model Type": [],
        "Abbreviation": [],
        "Description": [],
    }

    model_classes = (
        ALL_MODELS_CLASSES if model_type == SubstitutionModel else [model_type]
    )

    for model_class in model_classes:
        for model in model_class:
            data["Model Type"].append(model.model_type())
            data["Abbreviation"].append(model.value)
            data["Description"].append(model.description)

    return data


def available_models(
    model_type: Literal["dna", "protein"] | None = None,
    *,
    show_all: bool = True,
) -> _Table:
    """Return a table showing available substitution models.

    Parameters
    ----------
    model_type : Literal["dna", "protein"] | None, optional
        The models to fetch, by default None (all models).
    show_all : bool, optional
        if True, the representation of the table shows all records, by default True.

    Returns
    -------
    _Table
        Table with all available models.

    """
    template = "Available {}substitution models"
    if model_type == "dna":
        table = make_table(
            data=_make_models(DnaModel),
            title=template.format("nucleotide "),
        )
    elif model_type == "protein":
        table = make_table(
            data=_make_models(AaModel),
            title=template.format("protein "),
        )
    else:
        table = make_table(
            data=_make_models(SubstitutionModel),
            title=template.format(""),
        )

    if show_all:
        table.set_repr_policy(head=table.shape[0])
    return table


def available_freq_type() -> _Table:
    """Return a table showing available freq type options."""
    data: dict[str, list[str]] = {"Freq Type": [], "Description": []}

    for freq_type in FreqType:
        data["Freq Type"].append(freq_type.value)
        data["Description"].append(freq_type.description)

    return make_table(data=data, title="Available frequency types")


def available_rate_type() -> _Table:
    """Return a table showing available rate type options."""
    data: dict[str, list[str]] = {"Rate Type": [], "Description": []}

    for rate_type in ALL_BASE_RATE_TYPES:
        data["Rate Type"].append(rate_type.iqtree_str())
        data["Description"].append(get_description(rate_type))

    return make_table(data=data, title="Available rate heterogeneity types")