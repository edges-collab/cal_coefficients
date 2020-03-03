from os import listdir

import numpy as np
from edges_io.io import S1P
from matplotlib import pyplot as plt

from . import reflection_coefficient as rc


def plot_vna_comparison(folders, labels, repeat_num=None):
    assert len(folders) == len(labels)

    vna = {}
    for label, folder in zip(folders, labels):
        fls = listdir(folder)
        vna[label] = {}

        for standard in ["open", "short", "match", "3db", "6db", "10db", "15db"]:
            find_standard = standard
            if repeat_num is not None:
                find_standard += f"0{repeat_num}"

            fl = [fl for fl in fls if find_standard in fl.lower()][0]

            vna[label][standard], f = S1P.read(fl)

    o_a, s_a, m_a = rc.agilent_85033E(f, 50, m=1, md_value_ps=38)

    for label, standards in vna.items():
        for standard, s11 in standards.items():
            if standard.endswith("db"):
                vna[label][standard + "_corrected"] = rc.de_embed(
                    o_a,
                    s_a,
                    m_a,
                    standards["open"],
                    standards["short"],
                    standards["match"],
                    standards[standard],
                )

    fig, ax = plt.subplots(len(folders), 2, sharex=True)

    def angle(x):
        return (180 / np.pi) * np.unwrap(np.angle(x))

    for i, (label, standards) in enumerate(vna.items()):
        for standard, s11 in standards.items():
            if not standard.endswith("corrected"):
                continue

            for j, fnc in enumerate(
                (
                    lambda x: 20 * np.log10(np.abs(x)),
                    lambda x: angle(x) - angle(vna[labels[0]][standard]),
                )
            ):
                ax[i, j].plot(f, fnc(s11), label=label)
                ax[i, j].set_ylabel(f"{standard} Attn [{'degrees' if j else 'dB'}]")
                ax[i, j].set_title(r"$\Delta$ PHASE" if j else "MAGNITUDE")

        ax[i, -1].set_xlabel("frequency [MHz]")
    ax[0, 0].legend()
