/*
 *  CSPLib prob009: Perfect Square Placement
 *
 *  - The following code is written in Java using the JaCoP solver library (v4.4.0) and Apache Commons
 *  - The program at the end provides a Window to inspect the solution (+ mouse-wheel zoom)
 *
 *  Arguments: <Problem instance, integer:[0,203]> <Complete Search, boolean>
 *  e.g. $java -classpath .;commons-lang3-*.jar;jacop-4.4.0.jar solvers.Solver 179 true
 *
 *  Author: Theophilus Mouratides (github.com/thmour/)
 *  Date: 7-September-2016
 *  License: MIT
 *
 */

import input.Data;
import solvers.ChocoSolver;
import solvers.JacopoSolver;

public class Main {

    public static void main(String[] args) {
        int id = 0;
        try {
            if (args.length > 0)
                id = Math.min(Math.max(0, Integer.parseInt(args[0])), 203);
        } catch (NumberFormatException e) {
            System.err.println("Invalid first argument, use an integer eg. 0, 1, ..., 203");
            System.exit(1);
        }
        boolean search_all = false;
        if (args.length > 1) {
            search_all = Boolean.parseBoolean(args[1]);
        }
        System.out.println("Searching for " + (search_all ? "all distinct solutions" : "a solution") + " for instance #" + id);
        new JacopoSolver().solve(Data.instances[id], search_all);
    }
}