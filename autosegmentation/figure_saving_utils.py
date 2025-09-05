# Define settings for the output figures that will be generated
from pathlib import Path
import matplotlib.pyplot as plt

IMAGES_PATH = Path("/Users/aavelino/PycharmProjects/images/")
IMAGES_PATH_OUTPUT = IMAGES_PATH

# IMAGES_PATH_OUTPUT = IMAGES_PATH / "outputs"

IMAGES_PATH.mkdir(parents=True, exist_ok=True)
IMAGES_PATH_OUTPUT.mkdir(parents=True, exist_ok=True)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=150,):
    path = IMAGES_PATH_OUTPUT / f"{fig_id}.{fig_extension}"
    # Get current figure
    fig = plt.gcf()
    # Set a reasonable figure size (in inches)
    fig.set_size_inches(9, 6)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# Define the default font sizes to make the figures prettier
plt.rc('font', size=12)
plt.rc('axes', labelsize=12, titlesize=12)
plt.rc('legend', fontsize=12)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)

#old plt.rc('font', size=14)
#old plt.rc('axes', labelsize=14, titlesize=14)
#old plt.rc('legend', fontsize=14)
#old plt.rc('xtick', labelsize=10)
#old plt.rc('ytick', labelsize=10)