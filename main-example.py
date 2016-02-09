import os

import endomondo
import plot

if __name__ == "__main__":
    endomondo_user = endomondo.EndomondoUser(os.environ["ENDOMONDO_USER_ID"])
    workouts = endomondo_user.workouts()
    plt = plot.plot_all(workouts)
    plt.show()
