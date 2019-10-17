package solvers;

import org.apache.commons.lang3.tuple.Pair;

public interface Solver {
    void solve(Pair<Integer, Integer[]> data, boolean searchAll);
}
