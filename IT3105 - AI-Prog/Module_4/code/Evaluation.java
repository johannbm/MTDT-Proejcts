package sample;

import com.sun.webkit.dom.DOMWindowImpl;
import org.apache.commons.lang3.ArrayUtils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Objects;

/**
 * Created by Johannes on 14.10.2015.
 */
public class Evaluation {

    /**
     * How each heuristic is weighted
     * 0 : Smoothness weight
     * 1 : Monotonicity weight
     * 2 : Free tiles weight
     */
    public static final float[] heuristicWeights = new float[] {0.1f, 2.7f, 3.0f, 1.0f};


    /**
     * Alternative evaluation that prioritizes boards whose values.
     * descends in a snake like formation.
     * @param board board to evaluate.
     * @return  Evaluation score.
     */
    public static float evaluate2(Board board) {
        double[][] snake = new double[][] {
                new double[] {10,8,7,6.5},
                new double[] {0.5,0.7,1,3},
                new double[] {-0.5,-1.5,-1.8,-2},
                new double[] {-3.8,-3.7,-3.5,-3}
        };

        float totalSum = 0;
        for (int x = 0; x  < 4; x++) {
            for (int y = 0; y < 4; y++) {
                totalSum += snake[x][y] * board.getBoard()[y][x];
            }
        }

        totalSum += Math.pow(Util.getEmptySlots(board.getBoard()).size(),2);

        return totalSum;
    }

    /**
     * Evaluates the board according to the following criterias:
     * Monotonicity: The tiles decreases diagonally
     * Smoothness: How far away in log2 space tiles are from merging
     * Open slots: how many open tiles there are
     * Max tile: Value of highest tile. 2048 and above are given special values
     * Highest corner value: Bonus if highest tile is in a corner
     * @param board The board to evaluate
     * @return  The score of the board.
     */
    public static float evaluate(Board board) {

        float heuristicSum = 0;
        heuristicSum += heuristicWeights[0] * getBoardSmoothness(board.getBoard());
        heuristicSum += heuristicWeights[1] * getBoardMonotonicity(board.getBoard());
        heuristicSum += heuristicWeights[2] * getEmptyScore(board);
        heuristicSum += heuristicWeights[3] * getMaxTile(board.getBoard());
        heuristicSum += Util.getLog2(getHighestCornerTile(board.getBoard())) * 1.5f;

        if (board.isGameOver())
            heuristicSum -= 10000;
        if (getMaxTile(board.getBoard()) > 10)
            heuristicSum += 10000;
        else if (getMaxTile(board.getBoard()) > 11)
            heuristicSum += 10000;

        return heuristicSum;
    }

    /**
     * The score given based off the amount of free tiles in log10 space.
     * @param board The board.
     * @return  score.
     */
    public static double getEmptyScore(Board board) {
        int emptySlots = Util.getEmptySlots(board.getBoard()).size();
        if (emptySlots == 0)
            return 0;
        return Math.log(emptySlots);
    }

    /** Returns the value in log2 space of highest corner tile
     * @param board board to evaluate
     * @return  score.
     */
    public static int getHighestCornerTile(Integer[][] board) {
        ArrayList<Integer> values = new ArrayList<>();
        values.add(board[0][0]);
        values.add(board[0][3]);
        values.add(board[3][0]);
        values.add(board[3][3]);

        int maxCorner = Util.getLog2(Collections.max(values));
        int trueMax = getMaxTile(board);
        return (maxCorner == trueMax) ? trueMax : 0;

    }


    /**
     * Returns the highest value on the board in log2 space.
     * @param board board to look at
     * @return  What I said.
     */
    public static int getMaxTile(Integer[][] board) {
        int max = 0;
        for (int x = 0; x < board.length; x++) {
            for (int y = 0; y < board.length; y++) {
                if (board[x][y] > max)
                    max = board[x][y];
            }
        }

        return Util.getLog2(max);
    }


    /**
     * Returns the smoothness of the board
     * @param board board to evaluate
     * @return  smoothness
     */
    public static int getBoardSmoothness(Integer[][] board) {
        int smoothness = 0;

        Integer[][] transposedBoard = Util.transposeBoard(board);
        for (int x = 0; x < board.length; x++) {
            smoothness -= getUnitSmoothness(board[x]);
            smoothness -= getUnitSmoothness(transposedBoard[x]);
        }
        return smoothness;
    }

    public static int getUnitSmoothness(Integer [] unit) {
        Integer[] newUnit = Util.filterList(unit);
        int difference = 0;
        for (int i = 1; i < newUnit.length; i++) {
            difference += Math.abs((Math.log(newUnit[i]) / Math.log(2)) - (Math.log(newUnit[i - 1]) / Math.log(2)));
        }
        return difference;
    }

    public static int getBoardMonotonicity(Integer[][] board) {
        ArrayList<Integer> directionScore = new ArrayList<>();
        directionScore.add(getBoardMonotonicity(board, new Direction[]{Direction.UP, Direction.LEFT}));
        directionScore.add(getBoardMonotonicity(board, new Direction[]{Direction.UP, Direction.RIGHT}));
        directionScore.add(getBoardMonotonicity(board, new Direction[]{Direction.DOWN, Direction.RIGHT}));
        directionScore.add(getBoardMonotonicity(board, new Direction[]{Direction.DOWN, Direction.LEFT}));


        return Collections.max(directionScore);
    }

    public static int getBoardMonotonicity(Integer[][] board, Direction[] assumedCorner) {
        Integer[][] transposedBoard = Util.transposeBoard(board);
        int score = 0;

        //Check monotonicity horizontally
        for (Integer[] unit : board) {
            if (assumedCorner[1] == Direction.RIGHT) {
                ArrayUtils.reverse(unit);
            }
            int unitScore = getUnitMonotonicity(unit);
            score += unitScore;

            if (assumedCorner[1] == Direction.RIGHT) {
                ArrayUtils.reverse(unit);
            }
        }

        //Check monotonicity vertically
        for (Integer[] unit : transposedBoard) {
            if (assumedCorner[0] == Direction.DOWN) {
                ArrayUtils.reverse(unit);
            }
            int unitScore = getUnitMonotonicity(unit);
            score += unitScore;

            if (assumedCorner[0] == Direction.DOWN) {
                ArrayUtils.reverse(unit);
            }
        }

        return score;
    }

    public static int getUnitMonotonicity(Integer[] unit) {
        Integer[] filteredUnit = unit.clone();
        int monotonicity = 0;
        for (int i = 0; i < filteredUnit.length-1; i++) {
            if (filteredUnit[i+1] > filteredUnit[i]) {
                monotonicity -= Math.abs((Util.getLog2(filteredUnit[i+1])-Util.getLog2(filteredUnit[i])));
            }
        }

        return monotonicity;
    }








}
