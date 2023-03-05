class Browser():
    def gaussian():
        fig, ax = plt.subplots(figsize=(9,6))
        plt.style.use('fivethirtyeight')
        ax.plot(x_all,y2)

        ax.fill_between(x,y,0, alpha=0.3, color='b')
        ax.fill_between(x_all,y2,0, alpha=0.1)
        ax.set_xlim([-4,4])
        ax.set_xlabel('# of Standard Deviations Outside the Mean')
        ax.set_yticklabels([])
        ax.set_title('Normal Gaussian Curve')

        plt.savefig('normal_curve.png', dpi=72, bbox_inches='tight')
        plt.show()