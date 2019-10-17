package solvers;

import org.apache.commons.lang3.tuple.Pair;
import org.chocosolver.solver.Model;
import org.chocosolver.solver.search.strategy.Search;
import org.chocosolver.solver.variables.IntVar;
import plot.SquarePlacementPanel;

import javax.swing.*;
import java.util.Arrays;

public class ChocoSolver implements Solver {

    private static final int window_size = 650;

    @Override
    public void solve(Pair<Integer, Integer[]> data, boolean searchAll) {
        int N = data.getLeft();
        Integer[] S = data.getRight();
        int nsquares = S.length;

        Model model = new Model("perfect square placement " + N);
        IntVar[] X = new IntVar[nsquares];
        IntVar[] Y = new IntVar[nsquares];
        IntVar[] W = new IntVar[nsquares];
        IntVar[] H = new IntVar[nsquares];

        int[] durations = Arrays.stream(S).mapToInt(x -> x).toArray();

        IntVar L = model.intVar(N);

        for (int i = 0; i < nsquares; i++) {
            X[i] = model.intVar("x" + i, 0, N - S[i]);
            Y[i] = model.intVar("y" + i, 0, N - S[i]);

            W[i] = model.intVar("w" + i, S[i], S[i]);
            H[i] = model.intVar("h" + i, S[i], S[i]);
        }

        model.diffN(X, Y, W, H, false).post();
        model.cumulative(X, durations, durations, N);
        model.cumulative(Y, durations, durations, N);

        org.chocosolver.solver.Solver solver = model.getSolver();
        solver.setSearch(Search.minDomLBSearch(X));

        if (solver.solve()) {
            System.out.println("Solved");

            for (int i = 0; i < nsquares; i++) {
                System.out.printf("%d <%d> \n", X[i].getValue(), Y[i].getValue());
            }
        }

        SwingUtilities.invokeLater(new SquarePlacementPanel(1, window_size, N, Arrays.stream(X).map(IntVar::getValue).toArray(), Arrays.stream(Y).map(IntVar::getValue).toArray(), S));
    }
}
