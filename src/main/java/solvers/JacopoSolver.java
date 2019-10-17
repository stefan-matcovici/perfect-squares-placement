package solvers;

import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.tuple.Pair;
import org.jacop.constraints.Constraint;
import org.jacop.constraints.Cumulative;
import org.jacop.constraints.Diff2;
import org.jacop.core.IntVar;
import org.jacop.core.Store;
import org.jacop.search.*;
import plot.SquarePlacementPanel;

import javax.swing.*;

public class JacopoSolver implements Solver {

    private static final int WINDOW_SIZE = 650;

    @Override
    public void solve(Pair<Integer, Integer[]> data, boolean searchAll) {
        int N = data.getLeft();
        Integer[] S = data.getRight();
        int nsquares = S.length;
        Store store = new Store();

        IntVar[] X = new IntVar[nsquares];
        IntVar[] Y = new IntVar[nsquares];

        IntVar[] W = new IntVar[nsquares];
        IntVar[] H = new IntVar[nsquares];

        IntVar L = new IntVar(store, N, N);

        ArrayUtils.reverse(S);

        for (int i = 0; i < nsquares; i++) {
            X[i] = new IntVar(store, "X" + i, 0, N - S[i]);
            Y[i] = new IntVar(store, "Y" + i, 0, N - S[i]);

            W[i] = new IntVar(store, S[i], S[i]);
            H[i] = new IntVar(store, S[i], S[i]);
        }

        Constraint ctr1 = new Diff2(X, Y, W, H);
        Constraint ctr2 = new Cumulative(X, W, H, L);
        Constraint ctr3 = new Cumulative(Y, W, H, L);

        ctr1.impose(store);
        ctr2.impose(store);
        ctr3.impose(store);

        Search<IntVar> searchX = new DepthFirstSearch<>();
        Search<IntVar> searchY = new DepthFirstSearch<>();
        SelectChoicePoint<IntVar> labelX = new SimpleSelect<>(X, new SmallestMin<>(), new SmallestDomain<>(), new IndomainMin<>());
        SelectChoicePoint<IntVar> labelY = new SimpleSelect<>(Y, new SmallestMin<>(), new SmallestDomain<>(), new IndomainMin<>());
        searchY.setSelectChoicePoint(labelY);
        searchX.addChildSearch(searchY);

        if (searchAll)
            searchX.getSolutionListener().searchAll(true);

        searchX.getSolutionListener().recordSolutions(true);
        searchY.getSolutionListener().recordSolutions(true);
        searchX.setPrintInfo(false);
        searchY.setPrintInfo(false);
        searchX.labeling(store, labelX);
        for (int sid = 1; sid <= searchX.getSolutionListener().solutionsNo(); sid++) {
            SwingUtilities.invokeLater(new
                    SquarePlacementPanel(sid - 1, WINDOW_SIZE, N, searchX.getSolution(sid), searchY.getSolution(sid), S));
        }
    }
}
